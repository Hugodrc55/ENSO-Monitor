"""Tests de GET /api/v1/observations (base jetable, voir conftest.py).

Les observations insérées sont FICTIVES : valeurs inventées pour les tests,
enregistrées sous le code de la série servie par l'API.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import database
from app.database import get_session
from app.main import app
from app.models import ClimateIndex, DataImport, Observation, Source
from app.observations import SERIES_CODE

URL = "/api/v1/observations"


@contextmanager
def use_session(session: Session) -> Iterator[TestClient]:
    """Client HTTP dont les requêtes utilisent la session fournie."""
    app.dependency_overrides[get_session] = lambda: session
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    """Série fictive de quatre saisons, insérée dans le désordre."""
    index = ClimateIndex(
        source=Source(code="SRC_TEST", name="Source fictive", url="https://example.org/"),
        code=SERIES_CODE,
        name="Indice fictif",
        version="version fictive",
        unit="°C",
        reference_url="https://example.org/indice",
    )
    data_import = DataImport(
        climate_index=index,
        file_name="fictif.txt",
        source_url="https://example.org/fictif.txt",
        sha256="a" * 64,
        downloaded_at=datetime(2026, 11, 9, 13, 42, 35, tzinfo=UTC),
        version_evidence="Preuve fictive",
    )
    fictive = [  # saison, année, date de référence, ANOM
        ("FMA", 2000, date(2000, 3, 1), "0.00"),
        ("NDJ", 1999, date(1999, 12, 1), "0.30"),
        ("JFM", 2000, date(2000, 2, 1), "-0.05"),
        ("DJF", 2000, date(2000, 1, 1), "-0.10"),
    ]
    session.add_all(
        Observation(data_import=data_import, season=season, year=year, reference_month=ref,
                    total_c=Decimal("26.00"), anom_c=Decimal(anom), source_line=2 + position)
        for position, (season, year, ref, anom) in enumerate(fictive)
    )
    session.flush()
    with use_session(session) as client:
        yield client


def test_period_returns_observations_in_order_with_bounds_included(client: TestClient) -> None:
    # Début = date de NDJ 1999, fin = date de JFM 2000 : les deux bornes sont incluses.
    response = client.get(URL, params={"start": "1999-12-01", "end": "2000-02-01"})

    assert response.status_code == 200
    body = response.json()
    assert body["observations"] == [
        {"reference_month": "1999-12-01", "season": "NDJ", "year": 1999, "oni": 0.3},
        {"reference_month": "2000-01-01", "season": "DJF", "year": 2000, "oni": -0.1},
        {"reference_month": "2000-02-01", "season": "JFM", "year": 2000, "oni": -0.05},
    ]
    assert body["series"]["code"] == SERIES_CODE
    assert body["series"]["unit"] == "°C"
    assert (body["start"], body["end"]) == ("1999-12-01", "2000-02-01")


def test_period_without_data_returns_empty_list(client: TestClient) -> None:
    response = client.get(URL, params={"start": "1960-01-01", "end": "1960-12-31"})

    assert response.status_code == 200
    assert response.json()["observations"] == []


@pytest.mark.parametrize(
    "params",
    [
        {"start": "2000-13-01", "end": "2000-12-31"},  # mois inexistant
        {"start": "2000-02-30", "end": "2000-12-31"},  # jour inexistant
        {"start": "hier", "end": "2000-12-31"},
        {"end": "2000-12-31"},  # début manquant
    ],
)
def test_invalid_date_is_rejected(client: TestClient, params: dict[str, str]) -> None:
    response = client.get(URL, params=params)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "start"]


def test_start_after_end_is_rejected(client: TestClient) -> None:
    response = client.get(URL, params={"start": "2000-03-01", "end": "2000-01-01"})

    assert response.status_code == 422
    assert response.json() == {
        "detail": "La date de début (2000-03-01) est postérieure à la date de fin (2000-01-01)."
    }


def test_openapi_documents_inclusive_bounds() -> None:
    parameters = TestClient(app).get("/openapi.json").json()["paths"][URL]["get"]["parameters"]
    descriptions = {parameter["name"]: parameter["description"] for parameter in parameters}

    assert "**inclus**" in descriptions["start"]
    assert "**incluse**" in descriptions["end"]


def test_missing_series_returns_404(session: Session) -> None:
    with use_session(session) as client:  # base vide : aucune série importée
        response = client.get(URL, params={"start": "2000-01-01", "end": "2000-12-31"})

    assert response.status_code == 404
    assert SERIES_CODE in response.json()["detail"]


def test_unavailable_database_returns_503(monkeypatch: pytest.MonkeyPatch) -> None:
    # Aucun serveur n'écoute sur le port 1. Sans le délai de connexion de
    # create_db_engine, Windows insiste environ deux minutes avant d'abandonner ;
    # le délai est réduit à 1 s pour ce test.
    monkeypatch.setattr(database, "CONNECT_TIMEOUT_SECONDS", 1)
    engine = database.create_db_engine("postgresql+psycopg://nobody:none@127.0.0.1:1/absente")
    with Session(engine) as session, use_session(session) as client:
        response = client.get(URL, params={"start": "2000-01-01", "end": "2000-12-31"})
    engine.dispose()

    assert response.status_code == 503
    assert response.json() == {"detail": "Base de données indisponible."}
