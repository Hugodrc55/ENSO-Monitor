"""Tests de l'import du CSV ONI dans PostgreSQL (base jetable, voir conftest.py).

Les fichiers écrits dans tmp_path sont FICTIFS : fichier « brut », fiche de
provenance et CSV inventés pour les tests, pas des observations NOAA.
"""

import csv
import hashlib
import json
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.import_oni import CSV_COLUMNS, ImportRefused, import_observations
from app.models import DataImport, Observation

# Lignes fictives : (saison, année, reference_month, period_start, period_end, TOTAL, ANOM, ligne)
DJF_2000 = ("DJF", "2000", "2000-01-01", "1999-12-01", "2000-02-29", "26.00", "-0.10", "2")
JFM_2000 = ("JFM", "2000", "2000-02-01", "2000-01-01", "2000-03-31", "26.10", "-0.05", "3")
FMA_2000 = ("FMA", "2000", "2000-03-01", "2000-02-01", "2000-04-30", "26.20", "0.00", "4")
MAM_2000 = ("MAM", "2000", "2000-04-01", "2000-03-01", "2000-05-31", "26.30", "0.05", "5")


def write_inputs(folder: Path, rows: list[tuple[str, ...]], raw_text: str = "brut fictif v1\n",
                 **provenance_changes: object) -> tuple[Path, Path]:
    """Écrire un fichier brut fictif, sa fiche de provenance et le CSV correspondant."""
    folder.mkdir(exist_ok=True)
    raw = folder / "fictif.txt"
    raw.write_text(raw_text, encoding="utf-8", newline="\n")
    provenance = {
        "file_name": raw.name,
        "sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
        "source_url": "https://example.org/fictif.txt",
        "downloaded_at": "2026-11-09T13:42:35Z",
        "source_last_modified": "2026-11-03T19:31:48Z",
        "version_evidence": "Preuve fictive",
        "source": {"code": "SRC_TEST", "name": "Source fictive", "url": "https://example.org/"},
        "climate_index": {
            "code": "TEST_INDEX",
            "name": "Indice fictif",
            "version": "version fictive",
            "unit": "°C",
            "reference_url": "https://example.org/indice",
        },
    } | provenance_changes
    provenance_path = folder / "fictif.provenance.json"
    provenance_path.write_text(json.dumps(provenance), encoding="utf-8")

    csv_path = folder / "oni_clean.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(CSV_COLUMNS)
        for season, year, ref, start, end, total, anom, line in rows:
            writer.writerow([ref, start, end, season, year, total, anom, raw.name, line])
    return csv_path, provenance_path


def count(session: Session, model: type) -> int:
    return session.scalar(select(func.count()).select_from(model))


def test_first_import_stores_observations_and_provenance(session: Session, tmp_path: Path) -> None:
    report = import_observations(session, *write_inputs(tmp_path, [DJF_2000, JFM_2000, FMA_2000]))

    assert (report.inserted, report.unchanged, report.new_import) == (3, 0, True)
    data_import = session.get(DataImport, report.data_import_id)
    assert data_import.file_name == "fictif.txt"
    assert data_import.downloaded_at == datetime(2026, 11, 9, 13, 42, 35, tzinfo=timezone.utc)
    assert data_import.climate_index.version == "version fictive"
    first = session.scalar(select(Observation).where(Observation.season == "DJF"))
    assert first.reference_month == date(2000, 1, 1)
    assert first.anom_c == Decimal("-0.10")
    assert first.data_import_id == data_import.id
    assert first.source_line == 2


def test_second_import_of_same_file_adds_nothing(session: Session, tmp_path: Path) -> None:
    inputs = write_inputs(tmp_path, [DJF_2000, JFM_2000, FMA_2000])
    first = import_observations(session, *inputs)
    second = import_observations(session, *inputs)

    assert (second.inserted, second.unchanged, second.new_import) == (0, 3, False)
    assert second.data_import_id == first.data_import_id
    assert count(session, Observation) == 3
    assert count(session, DataImport) == 1


def test_new_file_adds_only_new_seasons(session: Session, tmp_path: Path) -> None:
    first = import_observations(session, *write_inputs(tmp_path / "v1", [DJF_2000, JFM_2000]))
    second = import_observations(
        session, *write_inputs(tmp_path / "v2", [DJF_2000, JFM_2000, FMA_2000], "brut fictif v2\n")
    )

    assert (second.inserted, second.unchanged, second.new_import) == (1, 2, True)
    links = dict(session.execute(select(Observation.season, Observation.data_import_id)).all())
    assert links == {"DJF": first.data_import_id, "JFM": first.data_import_id,
                     "FMA": second.data_import_id}


def test_conflicting_value_is_reported_and_nothing_is_written(
    session: Session, tmp_path: Path
) -> None:
    import_observations(session, *write_inputs(tmp_path / "v1", [DJF_2000, JFM_2000]))
    revised_jfm = JFM_2000[:6] + ("0.40",) + JFM_2000[7:]  # même saison, autre ANOM

    with pytest.raises(ImportRefused) as refusal:
        import_observations(
            session,
            *write_inputs(tmp_path / "v2", [DJF_2000, revised_jfm, FMA_2000], "brut fictif v2\n"),
        )

    [conflict] = refusal.value.conflicts
    assert (conflict.season, conflict.year) == ("JFM", 2000)
    assert (conflict.stored_anom, conflict.new_anom) == (Decimal("-0.05"), Decimal("0.40"))
    # Rien n'est écrit : ni FMA 2000, ni nouvel import, ni valeur écrasée.
    assert count(session, Observation) == 2
    assert count(session, DataImport) == 1
    stored = session.scalar(select(Observation.anom_c).where(Observation.season == "JFM"))
    assert stored == Decimal("-0.05")


def test_modified_raw_file_is_refused(session: Session, tmp_path: Path) -> None:
    inputs = write_inputs(tmp_path, [DJF_2000], sha256="0" * 64)

    with pytest.raises(ImportRefused, match="Empreinte SHA-256"):
        import_observations(session, *inputs)


@pytest.mark.parametrize(
    ("row", "message"),
    [
        (DJF_2000[:6] + ("-0.125",) + DJF_2000[7:], "plus de deux décimales"),
        (DJF_2000[:2] + ("2000-13-01",) + DJF_2000[3:], "Ligne 2 du CSV invalide"),
    ],
)
def test_invalid_csv_value_is_refused(
    session: Session, tmp_path: Path, row: tuple[str, ...], message: str
) -> None:
    with pytest.raises(ImportRefused, match=message):
        import_observations(session, *write_inputs(tmp_path, [row]))
    assert count(session, Observation) == 0


def test_provenance_without_extraction_date_is_refused(session: Session, tmp_path: Path) -> None:
    inputs = write_inputs(tmp_path, [DJF_2000], downloaded_at="2026-11-09")  # sans heure ni fuseau

    with pytest.raises(ImportRefused, match="Fiche de provenance invalide"):
        import_observations(session, *inputs)
