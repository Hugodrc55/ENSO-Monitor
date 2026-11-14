# Note pour le dossier : du fichier NOAA à l'API

Travail du 14 novembre 2026, réalisé avec l'assistance de Claude. Fichiers
principaux : [`backend/app/import_oni.py`](../backend/app/import_oni.py) (import) et
[`backend/app/observations.py`](../backend/app/observations.py) (route).

## Chaîne de traitement

```text
data/raw/noaa-cpc_oni-ersstv6_2026-11-09.txt     fichier NOAA brut, jamais modifié
  │ etl/transform_oni.py (pandas, NumPy)          validation, doublons, dates
  ▼
data/processed/oni_clean.csv                      921 observations
  │ backend/app/import_oni.py (+ fiche .provenance.json)
  ▼
PostgreSQL : source → climate_index → data_import → observation
  │ backend/app/observations.py (FastAPI, SQLAlchemy)
  ▼
GET /api/v1/observations?start=AAAA-MM-JJ&end=AAAA-MM-JJ
```

## Provenance

- **Fiche de provenance.** Elle accompagne le fichier brut :
  [`data/raw/…provenance.json`](../data/raw/noaa-cpc_oni-ersstv6_2026-11-09.provenance.json).
  On y trouve l'URL NOAA, le SHA-256, la date d'extraction (9 novembre 2026,
  13:42:35 UTC, d'après l'en-tête `Date` du serveur), le `Last-Modified` NOAA et
  la preuve de la version ERSSTv6.
- **Contrôle à l'import.** L'import refuse un fichier brut dont l'empreinte diffère
  de la fiche, ainsi qu'un CSV qui désigne un autre fichier source.
- **Retrouver l'origine d'une observation.** Chaque observation est reliée à
  l'import qui l'a chargée (fichier, empreinte, date d'extraction, date de
  chargement), puis à la série et à sa version, puis à la source.
  `source_line` donne la ligne du fichier brut : NDJ 2015 → ligne 793.

## Doublons : trois niveaux

1. **Transformation** : à l'intérieur d'un même fichier, les copies identiques
   sont ignorées et les versions contradictoires rejetées (D17).
2. **Import** :
   - une saison déjà en base avec les mêmes valeurs n'est pas réinsérée ;
   - une valeur différente est un **conflit**, qui est affiché. L'import entier
     est alors refusé : rien n'est écrit, rien n'est écrasé (D24) ;
   - un même fichier n'est enregistré qu'une fois.
3. **Base** : `UNIQUE (climate_index_id, year, season)` refuse un doublon quel
   que soit le programme qui écrit, même s'il vient d'un autre import (D22).

## Vérifié le 14 novembre 2026

| Vérification | Résultat |
| --- | --- |
| Migration sur PostgreSQL local (`upgrade head`, `current`, `alembic check`) | `86057118b37f (head)` ; modèles et migration identiques |
| Tests de la transformation (`etl/tests`) | 28 passed |
| Tests du backend : santé, schéma, import, route | 34 passed (1 + 15 + 8 + 10) |
| Erreurs volontaires dans le code (conflit ignoré, borne de fin exclue, contrôle début/fin supprimé) | Chacune fait échouer un test ; code restauré à l'identique |
| Import réel, 1er passage | 921 observations ajoutées ; 921 en base |
| Import réel, 2e passage du même fichier | 0 ajoutée, 921 identiques ; toujours 921 en base et 1 import |
| Copie du CSV modifiée volontairement (NDJ 2015 : 2.59 → 2.60) | Conflit affiché, code 1 ; NDJ 2015 reste à 2.59 en base |
| Requête réelle `?start=2015-07-01&end=2016-03-01` | 200 ; 9 saisons dans l'ordre, dont NDJ 2015 = 2.59 |
| Bornes, période vide, dates invalides, début après la fin | 200 (bornes incluses), 200 avec liste vide, 422, 422 |
| Base arrêtée | `/api/v1/observations` : 503 en 5 s ; `/api/v1/health` : 200 |

Les tests de l'import et de la route utilisent des données fictives, déclarées
comme telles. Les valeurs réelles ne sont vérifiées que par la démonstration
ci-dessus.

## Reste à faire

- Interface React : courbe, choix de la période, unité et source affichées.
- Test frontend du changement de période, troisième test exigé par le sujet.
- Comparaison de deux épisodes historiques.
- Révisions NOAA : un fichier plus récent dont les valeurs ont été révisées sera
  refusé (conflits). La règle d'acceptation d'une révision reste à décider.
- L'import vérifie le fichier brut désigné par le CSV, mais pas que le CSV en
  dérive bien : il fait confiance à la transformation, relancée juste avant.
- Déploiement cible (Docker Compose complet, Caddy, VPS) : à documenter.
