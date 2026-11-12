"""Transformer le fichier NOAA ONI (ERSSTv6) en observations validées et datées.

Étapes : contrôle d'intégrité, lecture, validation ligne par ligne, traitement
des doublons, datation des saisons, puis export CSV. Les valeurs scientifiques
TOTAL et ANOM sont reprises telles que publiées par la NOAA, sans recalcul.

Utilisation, depuis la racine du dépôt :
    python -m etl.transform_oni --input data/raw/<fichier>.txt \
        --output data/processed/oni_clean.csv
"""

import argparse
import hashlib
import logging
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# En-tête exact du fichier oni.ascii.txt.
NOAA_COLUMNS = ["SEAS", "YR", "TOTAL", "ANOM"]

# Les 12 saisons glissantes NOAA, rangées selon leur mois central :
# DJF (déc.-janv.-févr.) est centrée sur janvier, JFM sur février, ..., NDJ sur décembre.
SEASONS = ("DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ")
CENTRAL_MONTH = {season: month for month, season in enumerate(SEASONS, start=1)}

# Première année de la série ONI publiée par la NOAA.
FIRST_YEAR = 1950

# Bornes physiques larges, très au-delà des valeurs observées (TOTAL de 24,39 à
# 29,23 °C et ANOM de -2,04 à +2,59 °C dans le fichier du 9 novembre 2026).
# Elles ne jugent pas un extrême climatique : elles écartent une valeur
# impossible, comme un code de remplissage ou une erreur d'unité.
# L'eau de mer gèle vers -2 °C.
TOTAL_LIMITS_C = (-2.0, 40.0)
ANOM_LIMITS_C = (-10.0, 10.0)

OUTPUT_COLUMNS = [
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


@dataclass(frozen=True)
class TransformResult:
    """Résultat complet : chaque ligne lue se retrouve dans exactement un des trois tableaux."""

    observations: pd.DataFrame  # observations valides, triées chronologiquement
    identical_duplicates: pd.DataFrame  # copies exactes ignorées (source_line, season, year)
    rejected: pd.DataFrame  # lignes écartées et motif (source_line, reason)
    missing_seasons: list[str]  # trous dans la série, signalés sans être comblés


def check_integrity(path: Path) -> str:
    """Calculer l'empreinte SHA-256 du fichier brut et la comparer à SHA256SUMS.

    Le fichier de référence est cherché dans le même dossier que le fichier brut.
    Une différence signifie que le fichier a été modifié : le traitement s'arrête.
    """
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = read_checksums(path.with_name("SHA256SUMS")).get(path.name)
    if expected is None:
        logger.warning("Empreinte non vérifiée : %s absent de SHA256SUMS", path.name)
    elif expected != digest:
        raise ValueError(
            f"Empreinte SHA-256 différente de SHA256SUMS pour {path.name} : "
            f"attendue {expected}, obtenue {digest}. Le fichier brut a été modifié."
        )
    else:
        logger.info("Empreinte SHA-256 conforme à SHA256SUMS : %s", digest)
    return digest


def read_checksums(path: Path) -> dict[str, str]:
    """Lire un fichier au format `sha256sum` : « empreinte  nom_du_fichier » par ligne."""
    if not path.exists():
        return {}
    checksums = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) == 2:
            digest, name = parts
            checksums[name.lstrip("*")] = digest.lower()
    return checksums


def read_oni(path: Path) -> pd.DataFrame:
    """Lire le fichier NOAA sous forme de texte brut, avec le numéro de ligne d'origine.

    Tout est lu comme du texte, pour que la conversion numérique soit contrôlée
    ensuite ligne par ligne. L'en-tête n'est pas interprété automatiquement :
    avec ses réglages par défaut, pandas décalerait silencieusement les colonnes
    si une ligne contenait un champ de trop. Ici, une telle ligne provoque une erreur.
    """
    try:
        table = pd.read_csv(
            path,
            sep=r"\s+",  # colonnes séparées par un ou plusieurs espaces
            header=None,
            dtype=str,
            keep_default_na=False,  # « NA » ou « null » restent du texte, signalé ensuite
            skip_blank_lines=False,  # garde la correspondance avec les numéros de ligne
            encoding="utf-8",
        )
    except pd.errors.EmptyDataError as error:
        raise ValueError(f"{path.name} est vide.") from error
    except pd.errors.ParserError as error:
        raise ValueError(f"Structure inattendue dans {path.name} : {error}".strip()) from error
    except UnicodeDecodeError as error:
        raise ValueError(f"{path.name} n'est pas un fichier texte lisible.") from error

    header = table.iloc[0].tolist()
    if header != NOAA_COLUMNS:
        missing = [column for column in NOAA_COLUMNS if column not in header]
        raise ValueError(
            f"En-tête inattendu dans {path.name} : {header}. Attendu : {NOAA_COLUMNS} "
            f"(colonnes manquantes : {missing}). Le fichier n'est peut-être pas l'ONI NOAA."
        )

    rows = table.iloc[1:].set_axis(NOAA_COLUMNS, axis=1)
    if rows.empty:
        raise ValueError(f"{path.name} ne contient aucune observation.")
    # La ligne d'index 0 du tableau est la ligne 1 du fichier (l'en-tête).
    return rows.assign(source_file=path.name, source_line=rows.index + 1).reset_index(drop=True)


def parse_values(raw: pd.DataFrame, max_year: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Convertir les champs texte en nombres et séparer les lignes valides des rejetées.

    Une valeur non convertible devient NaN : elle n'est jamais remplacée, la
    ligne est rejetée avec son motif.
    """
    year_is_four_digits = raw["YR"].str.fullmatch(r"\d{4}", na=False)
    values = pd.DataFrame(
        {
            "season": raw["SEAS"],
            "year": pd.to_numeric(raw["YR"].where(year_is_four_digits), errors="coerce"),
            "total_c": pd.to_numeric(raw["TOTAL"], errors="coerce"),
            "anom_c": pd.to_numeric(raw["ANOM"], errors="coerce"),
            "source_file": raw["source_file"],
            "source_line": raw["source_line"],
        }
    )
    reasons = describe_problems(values, max_year)
    is_valid = reasons == ""
    valid = values[is_valid].astype({"year": "int64"})
    rejected = values.loc[~is_valid, ["source_line"]].assign(reason=reasons[~is_valid])
    return valid, rejected


def describe_problems(values: pd.DataFrame, max_year: int) -> pd.Series:
    """Décrire les problèmes de chaque ligne ; une chaîne vide signifie « ligne valide »."""
    # np.isfinite est faux pour NaN (absent ou non numérique) et pour ±infini.
    total_is_finite = np.isfinite(values["total_c"])
    anom_is_finite = np.isfinite(values["anom_c"])
    checks = {
        "saison absente ou inconnue": ~values["season"].isin(SEASONS),
        f"année absente, invalide ou hors de {FIRST_YEAR}-{max_year}": ~values["year"].between(
            FIRST_YEAR, max_year
        ),
        "TOTAL manquant, non numérique ou infini": ~total_is_finite,
        "ANOM manquante, non numérique ou infinie": ~anom_is_finite,
        "TOTAL hors des limites physiques": total_is_finite
        & ~values["total_c"].between(*TOTAL_LIMITS_C),
        "ANOM hors des limites physiques": anom_is_finite
        & ~values["anom_c"].between(*ANOM_LIMITS_C),
    }
    failed = pd.DataFrame(checks)  # une colonne booléenne par contrôle
    reasons = ["; ".join(failed.columns[row]) for row in failed.to_numpy()]
    return pd.Series(reasons, index=values.index, dtype="str")


def remove_identical_duplicates(valid: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Garder une seule ligne parmi des copies exactes : la première du fichier.

    « Exacte » signifie même saison, même année, même TOTAL et même ANOM. Le
    tri par numéro de ligne rend le choix déterministe.
    """
    ordered = valid.sort_values("source_line")
    is_copy = ordered.duplicated(subset=["season", "year", "total_c", "anom_c"], keep="first")
    return ordered[~is_copy], ordered.loc[is_copy, ["source_line", "season", "year"]]


def reject_conflicting_duplicates(unique: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Écarter toutes les versions d'une saison publiée avec des valeurs différentes.

    Aucune version n'est préférée à une autre : choisir serait arbitraire.
    """
    in_conflict = unique.duplicated(subset=["season", "year"], keep=False)
    conflicts = unique[in_conflict]
    season_label = conflicts["season"] + " " + conflicts["year"].astype(str)
    reason = "doublon contradictoire pour " + season_label
    rejected = conflicts[["source_line"]].assign(reason=reason)
    return unique[~in_conflict], rejected


def add_dates(observations: pd.DataFrame) -> pd.DataFrame:
    """Ajouter les dates dérivées de la saison, sans modifier les colonnes d'origine.

    reference_month est le 1er jour du mois central. YR étant l'année de ce mois
    central (vérifié sur les données mensuelles NOAA), aucune exception n'est
    nécessaire pour les saisons à cheval sur deux années :
    - DJF 2000 : référence 2000-01-01, période du 1999-12-01 au 2000-02-29 ;
    - NDJ 1999 : référence 1999-12-01, période du 1999-11-01 au 2000-01-31.
    Ces dates servent au tri, au filtrage et à l'affichage. Elles ne
    correspondent pas à une mesure faite ce jour-là : la valeur couvre trois mois.
    """
    reference = pd.to_datetime(
        pd.DataFrame(
            {
                "year": observations["year"],
                "month": observations["season"].map(CENTRAL_MONTH),
                "day": 1,
            }
        )
    )
    return observations.assign(
        reference_month=reference,
        period_start=reference - pd.DateOffset(months=1),
        # Veille du 1er jour du mois qui suit la saison, donc dernier jour du 3e mois.
        period_end=reference + pd.DateOffset(months=2) - pd.Timedelta(days=1),
    )


def find_missing_seasons(observations: pd.DataFrame) -> list[str]:
    """Repérer les saisons absentes entre deux observations consécutives.

    La série étant triée et sans doublon, deux saisons successives sont séparées
    d'un mois exactement. Un écart plus grand est signalé, jamais comblé.
    """
    months = observations["reference_month"]
    month_numbers = (months.dt.year * 12 + months.dt.month).to_numpy()
    steps = np.diff(month_numbers)
    gaps = []
    for position in np.flatnonzero(steps > 1):
        before = observations.iloc[position]
        after = observations.iloc[position + 1]
        gaps.append(
            f"{steps[position] - 1} saison(s) manquante(s) entre "
            f"{before['season']} {before['year']} et {after['season']} {after['year']}"
        )
    return gaps


def transform(raw: pd.DataFrame, max_year: int) -> TransformResult:
    """Enchaîner validation, doublons et datation sur le tableau lu par read_oni."""
    valid, invalid = parse_values(raw, max_year)
    unique, copies = remove_identical_duplicates(valid)
    consistent, conflicts = reject_conflicting_duplicates(unique)
    observations = (
        add_dates(consistent)
        .sort_values("reference_month")
        .reset_index(drop=True)[OUTPUT_COLUMNS]
    )
    rejected = pd.concat([invalid, conflicts]).sort_values("source_line").reset_index(drop=True)
    return TransformResult(
        observations=observations,
        identical_duplicates=copies.reset_index(drop=True),
        rejected=rejected,
        missing_seasons=find_missing_seasons(observations),
    )


def write_csv(observations: pd.DataFrame, path: Path) -> None:
    """Écrire le CSV nettoyé, octet pour octet identique d'une exécution à l'autre.

    Les dates sont au format ISO (AAAA-MM-JJ) et les fins de ligne en LF, quel que
    soit le système. Les nombres sont écrits sans arrondi : « -0.20 » devient « -0.2 »,
    c'est la même valeur.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    observations.to_csv(
        path, index=False, date_format="%Y-%m-%d", lineterminator="\n", encoding="utf-8"
    )


def log_report(result: TransformResult) -> None:
    """Journaliser chaque ligne ignorée ou rejetée, puis le bilan chiffré."""
    for duplicate in result.identical_duplicates.itertuples():
        logger.info(
            "Ligne %d ignorée : doublon identique de %s %d",
            duplicate.source_line, duplicate.season, duplicate.year,
        )
    for line in result.rejected.itertuples():
        logger.warning("Ligne %d rejetée : %s", line.source_line, line.reason)
    for gap in result.missing_seasons:
        logger.warning("Série discontinue : %s", gap)

    observations = result.observations
    if not observations.empty:
        first, last = observations.iloc[0], observations.iloc[-1]
        logger.info(
            "Période couverte : %s %d à %s %d",
            first["season"], first["year"], last["season"], last["year"],
        )
    logger.info(
        "Bilan : %d observation(s) valide(s), %d doublon(s) identique(s) ignoré(s), "
        "%d ligne(s) rejetée(s)",
        len(observations), len(result.identical_duplicates), len(result.rejected),
    )


def parse_arguments(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valider et dater les observations NOAA ONI (ERSSTv6) d'un fichier brut."
    )
    parser.add_argument("--input", type=Path, required=True, help="fichier brut oni.ascii.txt")
    parser.add_argument("--output", type=Path, required=True, help="CSV nettoyé à produire")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Lancer la transformation.

    Code de sortie : 0 si tout est valide ; 1 si le fichier est illisible ou si
    au moins une ligne est rejetée.
    """
    arguments = parse_arguments(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    try:
        check_integrity(arguments.input)
        raw = read_oni(arguments.input)
    except (OSError, ValueError) as error:
        logger.error("Lecture impossible : %s", error)
        return 1
    logger.info("%d lignes d'observation lues dans %s", len(raw), arguments.input.name)

    result = transform(raw, max_year=date.today().year)
    log_report(result)
    write_csv(result.observations, arguments.output)
    logger.info("Observations écrites dans %s", arguments.output)

    # Le CSV contient les observations valides même en cas de rejet. Le code 1
    # empêche toutefois un enchaînement automatique, comme l'import en base,
    # de continuer sans qu'une personne ait examiné les lignes rejetées.
    return 1 if len(result.rejected) else 0


if __name__ == "__main__":
    sys.exit(main())
