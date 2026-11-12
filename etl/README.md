# ETL — données NOAA ONI ERSSTv6

Traitement Python, séparé de l'API, du fichier NOAA brut versionné dans
[`data/raw/`](../data/raw/README.md). La transformation (lecture, validation,
doublons, datation) est en place. Le chargement dans PostgreSQL n'est pas encore
développé.

| Fichier | Rôle |
| --- | --- |
| `transform_oni.py` | Transformation complète, du fichier brut au CSV nettoyé |
| `tests/test_transform_oni.py` | Tests Pytest de la transformation |
| `requirements.txt` | pandas et NumPy, versions fixées |
| `requirements-dev.txt` | Les mêmes, plus pytest |

## Installation

Depuis la racine du dépôt, sous PowerShell :

```powershell
python -m venv etl/.venv
.\etl\.venv\Scripts\python.exe -m pip install -r etl/requirements-dev.txt
```

L'environnement `etl/.venv` est distinct de celui de l'API (`backend/.venv`) et
ignoré par Git.

## Lancer la transformation

```powershell
.\etl\.venv\Scripts\python.exe -m etl.transform_oni --input data/raw/noaa-cpc_oni-ersstv6_2026-11-09.txt --output data/processed/oni_clean.csv
```

La commande se lance depuis la racine du dépôt (`-m etl.transform_oni`), avec
des chemins relatifs. Elle affiche l'empreinte vérifiée, le nombre de lignes lues,
chaque ligne ignorée ou rejetée avec son motif, puis le bilan.

| Code de sortie | Signification |
| --- | --- |
| 0 | Toutes les lignes sont valides ; CSV écrit |
| 1 | Fichier refusé (absent, modifié, en-tête ou structure inattendus), ou au moins une ligne rejetée. Dans ce second cas, le CSV contient les observations valides et doit être examiné avant tout import |
| 2 | Arguments manquants ou invalides |

## Fonctions principales

| Fonction | Rôle |
| --- | --- |
| `check_integrity` | Compare l'empreinte SHA-256 du fichier à `SHA256SUMS` |
| `read_oni` | Lit le fichier en texte, vérifie l'en-tête, garde le numéro de ligne |
| `parse_values` et `describe_problems` | Convertissent les champs et décrivent les motifs de rejet |
| `remove_identical_duplicates` | Garde la première de plusieurs copies identiques |
| `reject_conflicting_duplicates` | Rejette les versions contradictoires d'une même saison |
| `add_dates` | Calcule `reference_month`, `period_start` et `period_end` |
| `find_missing_seasons` | Signale les trous de la série |
| `transform` | Enchaîne ces étapes et renvoie un `TransformResult` |
| `write_csv` | Écrit un CSV identique d'une exécution à l'autre |

Chaque ligne lue se retrouve dans exactement un des trois tableaux du résultat :
observations valides, doublons identiques ignorés ou lignes rejetées.

## Tests

```powershell
.\etl\.venv\Scripts\python.exe -m pytest etl/tests
```

Les tests écrivent de petits fichiers au format NOAA, aux valeurs **fictives**.
Ils vérifient la conversion d'une ligne valide, la datation de DJF et NDJ au
changement d'année, les doublons, les saisons, années et valeurs invalides, et
le refus d'un fichier modifié ou qui n'est pas l'ONI. Un test transforme aussi le
fichier NOAA réel et vérifie que deux exécutions produisent le même CSV.

Règles de transformation et format du CSV :
[`docs/DONNEES_NOAA.md`, section 10](../docs/DONNEES_NOAA.md#10-transformation-du-fichier-etl).
Justification des choix : décisions D12 et D15 à D18 dans
[`docs/DECISIONS.md`](../docs/DECISIONS.md).
