"""Tests du schéma PostgreSQL créé par la migration Alembic.

Ils utilisent une base jetable, désignée par TEST_DATABASE_URL (nom terminé par
« _test »), qu'ils vident avant et après leur exécution. Sans cette variable, ils
sont ignorés. Les lignes insérées sont FICTIVES : ce ne sont pas des observations NOAA.
"""

from collections.abc import Iterator
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import Engine, inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import create_db_engine, read_setting
from app.models import ClimateIndex, DataImport, Observation, Source

TEST_DATABASE_URL = read_setting("TEST_DATABASE_URL")
ALEMBIC_INI = Path(__file__).resolve().parents[1] / "alembic.ini"

pytestmark = pytest.mark.skipif(
    TEST_DATABASE_URL is None, reason="TEST_DATABASE_URL non définie : pas de base de test"
)


def alembic_config() -> Config:
    config = Config(str(ALEMBIC_INI))
    config.attributes["database_url"] = TEST_DATABASE_URL
    return config


@pytest.fixture(scope="module")
def engine() -> Iterator[Engine]:
    """Base de test vidée, puis créée par la migration (et non par create_all)."""
    if not make_url(TEST_DATABASE_URL).database.endswith("_test"):
        pytest.fail("TEST_DATABASE_URL doit désigner une base jetable, nommée en _test")
    config = alembic_config()
    command.downgrade(config, "base")
    command.upgrade(config, "head")
    engine = create_db_engine(TEST_DATABASE_URL)
    yield engine
    engine.dispose()
    command.downgrade(config, "base")


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    """Session dont rien n'est enregistré : tout est annulé à la fin du test."""
    with Session(engine) as session:
        yield session
        session.rollback()


# --- Données fictives ----------------------------------------------------------


def add_index(session: Session, code: str = "TEST_INDEX") -> ClimateIndex:
    source = Source(code=f"SRC_{code}", name="Source fictive", url="https://example.org/")
    index = ClimateIndex(
        source=source,
        code=code,
        name="Indice fictif",
        version="version fictive",
        unit="°C",
        reference_url="https://example.org/indice",
    )
    session.add(index)
    return index


def add_import(session: Session, index: ClimateIndex, sha256: str) -> DataImport:
    data_import = DataImport(
        climate_index=index,
        file_name="fichier-fictif.txt",
        source_url="https://example.org/fichier-fictif.txt",
        sha256=sha256,
        downloaded_at=datetime(2026, 11, 9, 13, 42, tzinfo=timezone.utc),
        version_evidence="Fichier fictif créé par les tests",
    )
    session.add(data_import)
    session.flush()
    return data_import


def new_observation(data_import: DataImport, **changes: object) -> Observation:
    """Observation fictive valide (DJF 2000), modifiable champ par champ."""
    values = {
        "reference_month": date(2000, 1, 1),
        "season": "DJF",
        "year": 2000,
        "total_c": Decimal("26.00"),
        "anom_c": Decimal("-0.10"),
        "source_line": 2,
    } | changes
    return Observation(data_import=data_import, **values)


def assert_rejected(session: Session, observation: Observation, constraint: str) -> None:
    session.add(observation)
    with pytest.raises(IntegrityError) as error:
        session.flush()
    assert constraint in str(error.value)


# --- Migration ---------------------------------------------------------------


def test_migration_creates_schema(engine: Engine) -> None:
    head = ScriptDirectory.from_config(alembic_config()).get_current_head()
    schema = inspect(engine)

    tables = set(schema.get_table_names())
    assert {"source", "climate_index", "data_import", "observation"} <= tables
    unique = {c["name"]: c["column_names"] for c in schema.get_unique_constraints("observation")}
    assert unique["uq_observation_climate_index_id_year_season"] == [
        "climate_index_id", "year", "season"
    ]
    indexes = {i["name"]: i["column_names"] for i in schema.get_indexes("observation")}
    assert indexes["ix_observation_climate_index_id_reference_month"] == [
        "climate_index_id", "reference_month"
    ]
    with engine.connect() as connection:
        current = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
    assert current == head


# --- Observations valides ------------------------------------------------------


def test_valid_observation_keeps_exact_decimals(session: Session) -> None:
    data_import = add_import(session, add_index(session), "a" * 64)
    session.add(new_observation(data_import))
    session.flush()

    query = text("SELECT total_c, anom_c, climate_index_id FROM observation")
    stored = session.execute(query).one()
    assert stored.total_c == Decimal("26.00")
    assert stored.anom_c == Decimal("-0.10")
    assert stored.climate_index_id == data_import.climate_index_id  # repris de l'import


def test_load_date_is_set_by_database(session: Session) -> None:
    data_import = add_import(session, add_index(session), "a" * 64)
    session.refresh(data_import)

    assert data_import.imported_at >= data_import.downloaded_at


def test_same_season_is_allowed_for_another_index(session: Session) -> None:
    first = add_import(session, add_index(session, "TEST_A"), "a" * 64)
    second = add_import(session, add_index(session, "TEST_B"), "b" * 64)
    session.add_all([new_observation(first), new_observation(second)])
    session.flush()


# --- Doublons et intégrité --------------------------------------------------------


def test_same_season_from_two_imports_is_rejected(session: Session) -> None:
    index = add_index(session)
    first = add_import(session, index, "a" * 64)
    second = add_import(session, index, "b" * 64)
    session.add(new_observation(first))
    session.flush()

    duplicate = new_observation(second, anom_c=Decimal("0.40"))
    assert_rejected(session, duplicate, "uq_observation_climate_index_id_year_season")


def test_same_file_cannot_be_imported_twice(session: Session) -> None:
    index = add_index(session)
    add_import(session, index, "a" * 64)

    with pytest.raises(IntegrityError, match="uq_data_import_sha256"):
        add_import(session, index, "a" * 64)


def test_observation_must_share_the_index_of_its_import(session: Session) -> None:
    data_import = add_import(session, add_index(session, "TEST_A"), "a" * 64)
    other_index = add_index(session, "TEST_B")
    session.flush()

    mismatched = Observation(
        data_import_id=data_import.id,
        climate_index_id=other_index.id,
        reference_month=date(2000, 1, 1),
        season="DJF",
        year=2000,
        total_c=Decimal("26.00"),
        anom_c=Decimal("-0.10"),
        source_line=2,
    )
    assert_rejected(session, mismatched, "fk_observation_data_import_id_data_import")


@pytest.mark.parametrize(
    ("changes", "constraint"),
    [
        ({"season": "XYZ"}, "ck_observation_season_code"),
        ({"year": 1949, "reference_month": date(1949, 1, 1)}, "ck_observation_year_min"),
        ({"reference_month": date(2000, 2, 1)}, "ck_observation_reference_month_central"),
        ({"season": "NDJ"}, "ck_observation_reference_month_central"),  # NDJ 2000 = décembre
        ({"total_c": Decimal("45.00")}, "ck_observation_total_physical_range"),
        ({"anom_c": Decimal("-12.00")}, "ck_observation_anom_physical_range"),
        ({"source_line": 1}, "ck_observation_source_line_after_header"),
    ],
)
def test_invalid_observation_is_rejected(
    session: Session, changes: dict[str, object], constraint: str
) -> None:
    data_import = add_import(session, add_index(session), "a" * 64)
    assert_rejected(session, new_observation(data_import, **changes), constraint)


# --- Retour arrière de la migration ---------------------------------------------


def test_downgrade_then_upgrade(engine: Engine) -> None:
    config = alembic_config()

    command.downgrade(config, "base")
    assert "observation" not in inspect(engine).get_table_names()

    command.upgrade(config, "head")
    assert "observation" in inspect(engine).get_table_names()
