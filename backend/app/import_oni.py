"""Charger dans PostgreSQL les observations ONI produites par la transformation.

Entrées :
- le CSV nettoyé par etl/transform_oni.py (data/processed/oni_clean.csv) ;
- la fiche de provenance JSON du fichier brut (data/raw/*.provenance.json).

Règles :
- le fichier brut désigné par la fiche doit avoir l'empreinte SHA-256 annoncée ;
- une saison déjà en base avec les mêmes valeurs n'est pas ajoutée une seconde fois ;
- une saison déjà en base avec d'autres valeurs est un conflit : chaque conflit est
  signalé et l'import entier est refusé, sans rien écrire ni écraser ;
- un même fichier (même empreinte) n'est enregistré qu'une fois comme import.

Utilisation, depuis le dossier backend/ :
    python -m app.import_oni --csv ../data/processed/oni_clean.csv \
        --provenance ../data/raw/noaa-cpc_oni-ersstv6_2026-11-09.provenance.json
"""

import argparse
import csv
import hashlib
import logging
import sys
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import create_db_engine
from app.models import ClimateIndex, DataImport, Observation, Source

logger = logging.getLogger(__name__)

# Colonnes du CSV écrit par etl/transform_oni.py (OUTPUT_COLUMNS).
CSV_COLUMNS = [
    "reference_month",
    "period_start",
    "period_end",
    "season",
    "year",
    "total_c",
    "anom_c",
    "source_file",
    "source_line",
]


# --- Fiche de provenance -------------------------------------------------------


class SourceInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    name: str
    url: str


class IndexInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    name: str
    version: str  # version vérifiée de la série
    unit: str
    reference_url: str


class Provenance(BaseModel):
    """Contenu attendu d'un fichier data/raw/*.provenance.json ; tout champ inconnu est refusé."""

    model_config = ConfigDict(extra="forbid")

    file_name: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_url: str
    downloaded_at: AwareDatetime  # date d'extraction, avec fuseau horaire
    source_last_modified: AwareDatetime | None = None
    version_evidence: str = Field(min_length=1)
    source: SourceInfo
    climate_index: IndexInfo


# --- Résultats -----------------------------------------------------------------


@dataclass(frozen=True)
class CsvObservation:
    reference_month: date
    season: str
    year: int
    total_c: Decimal
    anom_c: Decimal
    source_line: int  # ligne dans le fichier brut NOAA


@dataclass(frozen=True)
class Conflict:
    """Une saison déjà en base avec d'autres valeurs que celles du CSV."""

    season: str
    year: int
    stored_total: Decimal
    stored_anom: Decimal
    stored_file: str
    new_total: Decimal
    new_anom: Decimal
    new_line: int

    def describe(self) -> str:
        return (
            f"{self.season} {self.year} : en base TOTAL {self.stored_total} / ANOM "
            f"{self.stored_anom} (fichier {self.stored_file}) ; à importer TOTAL "
            f"{self.new_total} / ANOM {self.new_anom} (ligne {self.new_line} du fichier brut)"
        )


@dataclass(frozen=True)
class ImportReport:
    data_import_id: int
    new_import: bool  # False si ce fichier avait déjà été importé
    rows_read: int
    inserted: int
    unchanged: int  # saisons déjà en base avec les mêmes valeurs
    total_in_database: int  # observations de la série après l'import


class ImportRefused(Exception):
    """Import refusé avant toute écriture en base."""

    def __init__(self, message: str, conflicts: list[Conflict] | None = None) -> None:
        super().__init__(message)
        self.conflicts = conflicts or []


# --- Lecture et contrôle des entrées -----------------------------------------------


def load_provenance(path: Path) -> Provenance:
    """Lire la fiche de provenance et vérifier l'empreinte du fichier brut qu'elle décrit."""
    try:
        provenance = Provenance.model_validate_json(path.read_bytes())
    except ValidationError as error:
        raise ImportRefused(f"Fiche de provenance invalide ({path.name}) :\n{error}") from error

    raw_file = path.with_name(provenance.file_name)
    digest = hashlib.sha256(raw_file.read_bytes()).hexdigest()
    if digest != provenance.sha256:
        raise ImportRefused(
            f"Empreinte SHA-256 de {raw_file.name} différente de la fiche de provenance : "
            f"attendue {provenance.sha256}, obtenue {digest}."
        )
    return provenance


def two_decimals(text: str) -> Decimal:
    """Convertir sans arrondir : NUMERIC(4, 2) arrondirait une 3e décimale sans erreur."""
    value = Decimal(text)
    if not value.is_finite() or value.as_tuple().exponent < -2:
        raise ValueError(f"valeur {text!r} non finie ou avec plus de deux décimales")
    return value


def parse_row(row: dict[str, str], csv_line: int, expected_file: str) -> CsvObservation:
    if row["source_file"] != expected_file:
        raise ImportRefused(
            f"Ligne {csv_line} du CSV : fichier source {row['source_file']!r}, alors que la "
            f"fiche de provenance décrit {expected_file!r}."
        )
    try:
        return CsvObservation(
            reference_month=date.fromisoformat(row["reference_month"]),
            season=row["season"],
            year=int(row["year"]),
            total_c=two_decimals(row["total_c"]),
            anom_c=two_decimals(row["anom_c"]),
            source_line=int(row["source_line"]),
        )
    except (ValueError, InvalidOperation) as error:
        raise ImportRefused(f"Ligne {csv_line} du CSV invalide : {error}") from error


def read_clean_csv(path: Path, expected_file: str) -> list[CsvObservation]:
    """Lire le CSV de la transformation ; il doit provenir du fichier brut de la fiche."""
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != CSV_COLUMNS:
            raise ImportRefused(f"Colonnes inattendues dans {path.name} : {reader.fieldnames}")
        rows = [parse_row(row, line, expected_file) for line, row in enumerate(reader, start=2)]

    if not rows:
        raise ImportRefused(f"{path.name} ne contient aucune observation.")
    keys = [(row.season, row.year) for row in rows]
    if len(set(keys)) != len(keys):
        raise ImportRefused(f"{path.name} contient plusieurs fois la même saison.")
    return rows


# --- Comparaison avec la base, puis écriture ---------------------------------------


def stored_observations(
    session: Session, index: ClimateIndex | None
) -> dict[tuple[str, int], tuple[Decimal, Decimal, str]]:
    """Valeurs déjà en base : (saison, année) → (TOTAL, ANOM, fichier d'origine)."""
    if index is None:
        return {}
    query = (
        select(
            Observation.season,
            Observation.year,
            Observation.total_c,
            Observation.anom_c,
            DataImport.file_name,
        )
        .join(Observation.data_import)
        .where(Observation.climate_index_id == index.id)
    )
    return {
        (season, year): (total, anom, file_name)
        for season, year, total, anom, file_name in session.execute(query)
    }


def compare(
    rows: list[CsvObservation], stored: dict[tuple[str, int], tuple[Decimal, Decimal, str]]
) -> tuple[list[CsvObservation], int, list[Conflict]]:
    """Classer chaque ligne : nouvelle, déjà présente à l'identique, ou en conflit."""
    new_rows: list[CsvObservation] = []
    unchanged = 0
    conflicts: list[Conflict] = []
    for row in rows:
        known = stored.get((row.season, row.year))
        if known is None:
            new_rows.append(row)
        elif (known[0], known[1]) == (row.total_c, row.anom_c):
            unchanged += 1
        else:
            stored_total, stored_anom, stored_file = known
            conflicts.append(
                Conflict(
                    season=row.season,
                    year=row.year,
                    stored_total=stored_total,
                    stored_anom=stored_anom,
                    stored_file=stored_file,
                    new_total=row.total_c,
                    new_anom=row.anom_c,
                    new_line=row.source_line,
                )
            )
    return new_rows, unchanged, conflicts


def import_observations(session: Session, csv_path: Path, provenance_path: Path) -> ImportReport:
    """Importer le CSV dans la session, sans valider la transaction (fait par l'appelant).

    Tous les contrôles ont lieu avant la première écriture : un import refusé ne
    laisse aucune trace en base.
    """
    provenance = load_provenance(provenance_path)
    rows = read_clean_csv(csv_path, provenance.file_name)

    index = session.scalar(
        select(ClimateIndex).where(ClimateIndex.code == provenance.climate_index.code)
    )
    if index is not None and index.version != provenance.climate_index.version:
        raise ImportRefused(
            f"La série {index.code} est enregistrée en version « {index.version} », "
            f"le fichier annonce « {provenance.climate_index.version} »."
        )
    data_import = session.scalar(
        select(DataImport).where(DataImport.sha256 == provenance.sha256)
    )
    if data_import is not None and index is not None and data_import.climate_index_id != index.id:
        raise ImportRefused(
            f"Le fichier {provenance.file_name} est déjà importé pour une autre série."
        )

    new_rows, unchanged, conflicts = compare(rows, stored_observations(session, index))
    if conflicts:
        raise ImportRefused(
            f"{len(conflicts)} saison(s) déjà en base avec d'autres valeurs : "
            "rien n'a été écrit.",
            conflicts,
        )

    # Écritures, uniquement après tous les contrôles.
    if index is None:
        source = session.scalar(select(Source).where(Source.code == provenance.source.code))
        index = ClimateIndex(
            source=source or Source(**provenance.source.model_dump()),
            **provenance.climate_index.model_dump(),
        )
        session.add(index)
    new_import = data_import is None
    if data_import is None:
        data_import = DataImport(
            climate_index=index,
            file_name=provenance.file_name,
            source_url=provenance.source_url,
            sha256=provenance.sha256,
            downloaded_at=provenance.downloaded_at,
            source_last_modified=provenance.source_last_modified,
            version_evidence=provenance.version_evidence,
        )
        session.add(data_import)
    session.add_all(
        Observation(
            data_import=data_import,
            reference_month=row.reference_month,
            season=row.season,
            year=row.year,
            total_c=row.total_c,
            anom_c=row.anom_c,
            source_line=row.source_line,
        )
        for row in new_rows
    )
    session.flush()

    total = session.scalar(
        select(func.count())
        .select_from(Observation)
        .where(Observation.climate_index_id == index.id)
    )
    return ImportReport(
        data_import_id=data_import.id,
        new_import=new_import,
        rows_read=len(rows),
        inserted=len(new_rows),
        unchanged=unchanged,
        total_in_database=total,
    )


# --- Commande ---------------------------------------------------------------------


def parse_arguments(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Importer dans PostgreSQL le CSV ONI nettoyé.")
    parser.add_argument(
        "--csv", type=Path, required=True, help="CSV produit par etl/transform_oni.py"
    )
    parser.add_argument(
        "--provenance", type=Path, required=True, help="fiche JSON du fichier brut (data/raw/)"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Lancer l'import.

    Code de sortie : 0 si l'import est validé, même sans nouvelle observation ;
    1 s'il est refusé ou impossible ; 2 si les arguments sont invalides.
    """
    arguments = parse_arguments(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    engine = create_db_engine()
    try:
        with Session(engine) as session:
            report = import_observations(session, arguments.csv, arguments.provenance)
            session.commit()
    except ImportRefused as error:
        for conflict in error.conflicts:
            logger.error("Conflit %s", conflict.describe())
        logger.error("Import refusé : %s", error)
        return 1
    except (OSError, SQLAlchemyError) as error:
        logger.error("Import impossible : %s", error)
        return 1
    finally:
        engine.dispose()

    status = "créé" if report.new_import else "déjà enregistré (même empreinte)"
    logger.info("Import n°%d : %s", report.data_import_id, status)
    logger.info(
        "%d lignes lues : %d observation(s) ajoutée(s), %d déjà présente(s) à l'identique",
        report.rows_read, report.inserted, report.unchanged,
    )
    logger.info("Observations de la série en base : %d", report.total_in_database)
    return 0


if __name__ == "__main__":
    sys.exit(main())
