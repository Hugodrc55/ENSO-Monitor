"""Tests de la transformation ONI.

Les petits fichiers écrits par `write_oni_file` contiennent des valeurs FICTIVES,
inventées pour les tests : ce ne sont pas des observations NOAA. Seul le dernier
test utilise le fichier NOAA authentique versionné dans data/raw/.
"""

from pathlib import Path

import pandas as pd
import pytest

from etl.transform_oni import (
    OUTPUT_COLUMNS,
    SEASONS,
    TransformResult,
    check_integrity,
    main,
    read_oni,
    transform,
)

HEADER = " SEAS  YR   TOTAL   ANOM"
MAX_YEAR = 2026
REAL_FILE = Path(__file__).resolve().parents[2] / "data/raw/noaa-cpc_oni-ersstv6_2026-11-09.txt"


def write_oni_file(folder: Path, *rows: str) -> Path:
    """Écrire un fichier au format NOAA (en-tête + lignes fictives)."""
    path = folder / "oni_fictif.txt"
    path.write_text("\n".join([HEADER, *rows]) + "\n", encoding="ascii", newline="\n")
    return path


def run(path: Path) -> TransformResult:
    return transform(read_oni(path), max_year=MAX_YEAR)


# --- Conversion d'une observation valide -------------------------------------


def test_valid_line_becomes_dated_observation(tmp_path: Path) -> None:
    result = run(write_oni_file(tmp_path, "  JFM 2000  26.00  -0.10"))

    assert result.rejected.empty
    observation = result.observations.iloc[0]
    assert observation["season"] == "JFM"
    assert observation["year"] == 2000
    assert observation["total_c"] == 26.0  # valeurs reprises telles quelles
    assert observation["anom_c"] == -0.1
    assert observation["reference_month"] == pd.Timestamp("2000-02-01")
    assert observation["period_start"] == pd.Timestamp("2000-01-01")
    assert observation["period_end"] == pd.Timestamp("2000-03-31")
    assert observation["source_line"] == 2


# --- Conversion saison/année vers une date ----------------------------------


@pytest.mark.parametrize(
    ("row", "period_start", "reference_month", "period_end"),
    [
        # NDJ 1999 : novembre 1999 à janvier 2000, centrée sur décembre 1999.
        ("  NDJ 1999  26.00  0.10", "1999-11-01", "1999-12-01", "2000-01-31"),
        # DJF 2000 : décembre 1999 à février 2000 (2000 est bissextile).
        ("  DJF 2000  26.00  0.10", "1999-12-01", "2000-01-01", "2000-02-29"),
        ("  DJF 2001  26.00  0.10", "2000-12-01", "2001-01-01", "2001-02-28"),
    ],
)
def test_seasons_crossing_new_year(
    tmp_path: Path, row: str, period_start: str, reference_month: str, period_end: str
) -> None:
    observation = run(write_oni_file(tmp_path, row)).observations.iloc[0]

    assert observation["period_start"] == pd.Timestamp(period_start)
    assert observation["reference_month"] == pd.Timestamp(reference_month)
    assert observation["period_end"] == pd.Timestamp(period_end)


def test_twelve_seasons_give_twelve_consecutive_central_months(tmp_path: Path) -> None:
    rows = [f"  {season} 2000  26.00  0.10" for season in SEASONS]
    result = run(write_oni_file(tmp_path, *rows))

    months = result.observations["reference_month"].dt.month.tolist()
    assert months == list(range(1, 13))
    assert result.missing_seasons == []


def test_observations_are_sorted_chronologically(tmp_path: Path) -> None:
    # Fichier volontairement dans le désordre : DJF 2000 avant NDJ 1999.
    result = run(write_oni_file(tmp_path, "  DJF 2000  26.00  0.10", "  NDJ 1999  26.00  0.20"))

    assert result.observations["season"].tolist() == ["NDJ", "DJF"]


# --- Doublons ---------------------------------------------------------------


def test_identical_duplicate_is_kept_once(tmp_path: Path) -> None:
    result = run(write_oni_file(tmp_path, "  DJF 2000  26.00  -0.10", "  DJF 2000  26.00  -0.10"))

    assert len(result.observations) == 1
    assert result.observations.loc[0, "source_line"] == 2  # la première occurrence est gardée
    assert result.identical_duplicates["source_line"].tolist() == [3]
    assert result.rejected.empty


def test_conflicting_duplicate_is_rejected_without_choosing(tmp_path: Path) -> None:
    result = run(
        write_oni_file(
            tmp_path,
            "  DJF 2000  26.00  -0.10",
            "  DJF 2000  26.00   0.40",  # même saison, autre anomalie
            "  JFM 2000  26.10  -0.05",
        )
    )

    assert result.observations["season"].tolist() == ["JFM"]
    assert result.rejected["source_line"].tolist() == [2, 3]
    assert result.rejected["reason"].str.contains("doublon contradictoire pour DJF 2000").all()


# --- Lignes invalides -------------------------------------------------------


@pytest.mark.parametrize("season", ["XYZ", "djf", "DJ"])
def test_unknown_season_is_rejected(tmp_path: Path, season: str) -> None:
    path = write_oni_file(tmp_path, f"  {season} 2000  26.00  -0.10", "  JFM 2000  26.10  0.05")
    result = run(path)

    assert result.observations["season"].tolist() == ["JFM"]
    assert result.rejected["source_line"].tolist() == [2]
    assert "saison absente ou inconnue" in result.rejected.loc[0, "reason"]


@pytest.mark.parametrize(
    ("anomaly", "expected_reason"),
    [
        ("abc", "ANOM manquante, non numérique ou infinie"),
        ("1,5", "ANOM manquante, non numérique ou infinie"),
        ("NaN", "ANOM manquante, non numérique ou infinie"),
        ("inf", "ANOM manquante, non numérique ou infinie"),
        ("", "ANOM manquante, non numérique ou infinie"),  # ligne à trois champs
        ("-99.90", "ANOM hors des limites physiques"),
    ],
)
def test_invalid_anomaly_is_rejected(tmp_path: Path, anomaly: str, expected_reason: str) -> None:
    result = run(write_oni_file(tmp_path, f"  DJF 2000  26.00  {anomaly}"))

    assert result.observations.empty
    assert result.rejected.loc[0, "reason"] == expected_reason


@pytest.mark.parametrize("year", ["1949", "2027", "20X0", "200"])
def test_invalid_year_is_rejected(tmp_path: Path, year: str) -> None:
    result = run(write_oni_file(tmp_path, f"  DJF {year}  26.00  -0.10"))

    assert result.observations.empty
    assert result.rejected.loc[0, "reason"] == "année absente, invalide ou hors de 1950-2026"


def test_every_line_is_accounted_for(tmp_path: Path) -> None:
    rows = [
        "  DJF 2000  26.00  -0.10",  # valide
        "  DJF 2000  26.00  -0.10",  # doublon identique
        "  XYZ 2000  26.00  -0.10",  # saison inconnue
        "  JFM 2000  26.10  abc",  # anomalie non numérique
        "  FMA 2000  26.20   0.00",  # valide
    ]
    result = run(write_oni_file(tmp_path, *rows))

    accounted = len(result.observations) + len(result.identical_duplicates) + len(result.rejected)
    assert accounted == len(rows)
    assert result.rejected["source_line"].tolist() == [4, 5]


def test_missing_season_is_reported_not_filled(tmp_path: Path) -> None:
    result = run(write_oni_file(tmp_path, "  DJF 2000  26.00  0.10", "  MAM 2000  26.30  0.20"))

    assert len(result.observations) == 2
    assert result.missing_seasons == ["2 saison(s) manquante(s) entre DJF 2000 et MAM 2000"]


# --- Fichier illisible ou modifié --------------------------------------------


def test_file_that_is_not_noaa_oni_is_refused(tmp_path: Path) -> None:
    page = tmp_path / "erreur.html"
    page.write_text("<!DOCTYPE html>\n<html><body>Not Found</body></html>\n", encoding="utf-8")

    with pytest.raises(ValueError, match="En-tête inattendu"):
        read_oni(page)


def test_line_with_extra_field_is_refused(tmp_path: Path) -> None:
    path = write_oni_file(tmp_path, "  DJF 2000  26.00  -0.10  9.99")

    with pytest.raises(ValueError, match="Structure inattendue"):
        read_oni(path)


def test_modified_raw_file_is_refused(tmp_path: Path) -> None:
    path = write_oni_file(tmp_path, "  DJF 2000  26.00  -0.10")
    (tmp_path / "SHA256SUMS").write_text(f"{'0' * 64}  {path.name}\n", encoding="ascii")

    with pytest.raises(ValueError, match="Empreinte SHA-256 différente"):
        check_integrity(path)


# --- Commande complète ------------------------------------------------------


def test_command_signals_rejected_lines_with_exit_code(tmp_path: Path) -> None:
    source = write_oni_file(tmp_path, "  DJF 2000  26.00  -0.10", "  XYZ 2000  26.00  -0.10")
    output = tmp_path / "oni_clean.csv"

    assert main(["--input", str(source), "--output", str(output)]) == 1
    assert len(pd.read_csv(output)) == 1  # seules les observations valides sont écrites


def test_real_noaa_file_is_transformed_reproducibly(tmp_path: Path) -> None:
    """Fichier NOAA authentique du 9 novembre 2026 : 921 saisons, de DJF 1950 à ASO 2026."""
    first, second = tmp_path / "first.csv", tmp_path / "second.csv"

    assert main(["--input", str(REAL_FILE), "--output", str(first)]) == 0
    assert main(["--input", str(REAL_FILE), "--output", str(second)]) == 0
    assert first.read_bytes() == second.read_bytes()

    clean = pd.read_csv(first, dtype=str)
    assert clean.columns.tolist() == OUTPUT_COLUMNS
    assert len(clean) == 921
    # Valeurs lues dans le fichier brut, lignes 2 et 922.
    assert clean.iloc[0, :7].tolist() == [
        "1950-01-01", "1949-12-01", "1950-02-28", "DJF", "1950", "25.01", "-1.32"
    ]
    assert clean.iloc[-1, :7].tolist() == [
        "2026-09-01", "2026-08-01", "2026-10-31", "ASO", "2026", "29.23", "2.46"
    ]
