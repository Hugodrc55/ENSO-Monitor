# ENSO Monitor

Projet individuel de rattrapage HETIC WEB3, développé progressivement avec une
validation personnelle à chaque étape. Début : **4 novembre 2026**.

Dépôt GitHub : [Hugodrc55/ENSO-Monitor](https://github.com/Hugodrc55/ENSO-Monitor),
publié depuis le **10 novembre 2026**. Voir [le suivi Git](docs/GIT.md).

## État au 16 novembre 2026

**Dossier de conception** (livrable B, 15 pages) : source
[`docs/dossier/dossier.html`](docs/dossier/README.md), export PDF par
`docs/dossier/exporter.ps1`. Quatre passages restent à compléter par l'étudiant
avant le rendu.

- **Premier écran (4 novembre)** : une page React/TypeScript appelait
  `GET /api/v1/health` pour vérifier que l'API répondait. Elle a été remplacée le
  15 novembre par l'interface décrite plus bas ; la route de santé reste dans l'API.
- **Source scientifique (9 novembre)** : l'indice retenu est **NOAA ONI, version
  ERSSTv6** ([page NOAA](https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/index.php)).
  Le fichier authentique `oni.ascii.txt` a été téléchargé le 9 novembre 2026 dans
  [`data/raw/`](data/raw/README.md), avec son empreinte SHA-256. Il couvre 921
  saisons, de DJF 1950 à ASO 2026. Format, unités, datation des saisons,
  différence ONI/RONI et limites : voir [DONNEES_NOAA.md](docs/DONNEES_NOAA.md).
- **Transformation (12 novembre)** : [`etl/transform_oni.py`](etl/README.md)
  vérifie le fichier brut, valide chaque ligne, traite les doublons, date chaque
  saison par son mois central et produit `data/processed/oni_clean.csv`. Sur le
  fichier du 9 novembre, les 921 lignes sont valides. 28 tests Pytest couvrent
  la transformation.
- **Base de données (14 novembre)** : PostgreSQL 18.7 tourne en local avec
  Docker Compose. Le schéma `source → climate_index → data_import → observation`
  ([BASE_DE_DONNEES.md](docs/BASE_DE_DONNEES.md)) est défini par des modèles
  SQLAlchemy et créé par une migration Alembic. 15 tests vérifient ses
  contraintes sur une base jetable, dont le refus d'un doublon venant de deux
  imports différents.
- **Import et API (14 novembre)** : les 921 observations du fichier NOAA sont
  importées avec leur provenance ; un second import du même fichier n'ajoute
  rien. `GET /api/v1/observations?start=…&end=…` renvoie les observations d'une
  période, bornes incluses. Démonstration :
  [section dédiée](#démonstration--du-fichier-noaa-à-lapi).
- **Interface (15 novembre)** : la page React recharge les observations de la
  période choisie, trace la courbe ONI (dates, °C, seuils ±0,5 °C, source NOAA)
  et donne les valeurs dans un tableau. Elle compare El Niño 1997-1998 et
  La Niña 1988-1989 à partir des réponses de l'API. 12 tests Vitest, dont le
  changement de période. Démonstration : [section dédiée](#démonstration-de-linterface).

## Prérequis

- Node.js **22 à partir de 22.22.2**, ou **24 à partir de 24.15**, avec npm ; environnement vérifié le 4 novembre : Node 22.18.0, npm 10.9.3 ; les 9 et 15 novembre : Node 22.23.4, npm 10.9.9. Ce minimum vient de jsdom, utilisé par les tests du frontend ; Vite et ESLint en demandent moins.
- Python **3.13** et Git ; environnement vérifié le 4 novembre : Python 3.13.7, Git 2.50.1 ; le 9 novembre : Python 3.13.17, Git 2.56.0.
- PowerShell sous Windows pour les commandes ci-dessous.
- Docker Desktop avec Docker Compose, pour faire tourner PostgreSQL sans l'installer sur la machine ; environnement vérifié le 14 novembre : Docker 29.9.2, Docker Compose v5.6.1, image `postgres:18.7-alpine`.

Les dépendances JavaScript sont figées dans `frontend/package-lock.json`.
Les versions Python directes sont fixées dans `backend/requirements*.txt` (API)
et `etl/requirements*.txt` (traitement des données).
Les dépendances Python transitives sont résolues par pip à l'installation ;
ces fichiers ne constituent pas un verrouillage complet de l'environnement.

## Installation depuis la racine du dépôt

```powershell
python -m venv backend/.venv
.\backend\.venv\Scripts\python.exe -m pip install -r backend/requirements-dev.txt
python -m venv etl/.venv
.\etl\.venv\Scripts\python.exe -m pip install -r etl/requirements-dev.txt
npm.cmd --prefix frontend ci
Copy-Item .env.example .env
```

Dans `.env`, remplacer `remplacer-par-un-mot-de-passe-local` par un mot de passe
local. Ce fichier est exclu de Git. L'API et l'ETL ont chacun leur environnement
Python : l'API n'installe pas pandas. L'appel direct à Python dans `.venv` évite de modifier la politique d'exécution
PowerShell pour activer l'environnement. `npm.cmd` évite le même problème avec
le script `npm.ps1`. Les bibliothèques PDF utilisées par l'assistant pour lire
le sujet ne sont pas des dépendances de l'application.

## Lancement local

L'interface affiche les observations de la base : au premier lancement,
démarrer PostgreSQL, appliquer la migration puis importer les données (étapes 1
à 3 de la [démonstration](#démonstration--du-fichier-noaa-à-lapi)). Sinon, la
page affiche l'erreur renvoyée par l'API : 503 si la base est arrêtée, 404 si
aucune observation n'a été importée.

Ouvrir ensuite deux terminaux à la racine du dépôt.

**Terminal 1 — API :**

```powershell
.\backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 — frontend :**

```powershell
npm.cmd --prefix frontend run dev
```

- Application : <http://127.0.0.1:5173>
- Santé API : <http://127.0.0.1:8000/api/v1/health>
- Documentation OpenAPI interactive : <http://127.0.0.1:8000/docs>

Arrêt : `Ctrl+C` dans chaque terminal. Les serveurs écoutent uniquement sur la
machine locale. Si un port est occupé, arrêter le serveur concerné ; Vite utilise
`strictPort` pour éviter un changement silencieux de port.

## Comment les deux parties communiquent

```text
Navigateur / React
    │ « Afficher » → GET /api/v1/observations?start=…&end=… sur le port 5173
    ▼
Vite : proxy local /api vers 127.0.0.1:8000
    ▼
FastAPI : validation des dates → requête SQLAlchemy → PostgreSQL
    │ {"series": {…}, "start": "…", "end": "…", "observations": […]}
    ▼
React : contrôle du JSON, puis résumé, courbe et tableau des valeurs
```

Le navigateur utilise une URL relative ; il n'est pas nécessaire d'ouvrir une
politique CORS pour ce fonctionnement local. En cible, le routage sera documenté
avec Caddy.

Une période incomplète ou inversée est refusée dans le navigateur, sans requête.
Quand la période change, la requête précédente est annulée et sa réponse ignorée.
Une requête expire après dix secondes, plus que les cinq secondes au bout
desquelles l'API répond 503 si la base est injoignable. React StrictMode peut
provoquer une première requête annulée en développement : le nettoyage de l'effet
permet de le gérer.

## Transformation des données NOAA

Depuis la racine du dépôt :

```powershell
.\etl\.venv\Scripts\python.exe -m etl.transform_oni --input data/raw/noaa-cpc_oni-ersstv6_2026-11-09.txt --output data/processed/oni_clean.csv
```

```text
fichier brut NOAA (data/raw/, jamais modifié)
    │ contrôle SHA-256, lecture pandas en texte, en-tête vérifié
    ▼
validation de chaque ligne (saison, année, nombres finis, bornes physiques)
    │ doublons : copie identique ignorée, versions contradictoires rejetées
    ▼
datation par le mois central (DJF 1950 → 1950-01-01), tri chronologique
    ▼
data/processed/oni_clean.csv (régénéré, non versionné)
```

Les valeurs `TOTAL` et `ANOM` sont reprises telles que publiées par la NOAA, sans
recalcul ni correction. La commande signale chaque ligne ignorée ou rejetée et
se termine avec le code 1 si une ligne est rejetée. Détails : [etl/README.md](etl/README.md)
et [DONNEES_NOAA.md, section 10](docs/DONNEES_NOAA.md#10-transformation-du-fichier-etl).

## Base de données PostgreSQL

PostgreSQL tourne dans un conteneur, décrit par [`compose.yaml`](compose.yaml) et
configuré par `.env`. Il n'écoute que sur `127.0.0.1`. Depuis la racine du dépôt :

```powershell
docker compose up -d --wait db
.\backend\.venv\Scripts\python.exe -m alembic -c backend/alembic.ini upgrade head
.\backend\.venv\Scripts\python.exe -m alembic -c backend/alembic.ini current
```

`upgrade head` crée le schéma ; `current` doit afficher `86057118b37f (head)`.
SQLAlchemy et Alembic lisent la même variable `DATABASE_URL`, définie dans
`.env`. L'API ne se connecte à la base que pour servir les observations :
`/api/v1/health` répond même quand PostgreSQL est arrêté.

Autres commandes utiles :

```powershell
docker compose exec db psql -U enso -d enso_monitor -c "\dt"     # lister les tables
docker compose exec db createdb -U enso enso_monitor_test       # base jetable des tests, une seule fois
.\backend\.venv\Scripts\python.exe -m alembic -c backend/alembic.ini upgrade head --sql   # SQL sans l'exécuter
docker compose stop db                                          # arrêter ; les données restent dans le volume
```

`downgrade` supprime les tables : ne l'utiliser que sur une base de test. Le
schéma, ses contraintes et les règles d'import sont décrits dans
[BASE_DE_DONNEES.md](docs/BASE_DE_DONNEES.md).

## Démonstration : du fichier NOAA à l'API

Commandes exécutées le 14 novembre 2026, depuis la racine du dépôt, avec les
résultats obtenus.

**1. Base et schéma**

```powershell
docker compose up -d --wait db
.\backend\.venv\Scripts\python.exe -m alembic -c backend/alembic.ini upgrade head
```

**2. Transformation du fichier brut** : 921 observations valides, CSV identique
à chaque exécution.

```powershell
.\etl\.venv\Scripts\python.exe -m etl.transform_oni --input data/raw/noaa-cpc_oni-ersstv6_2026-11-09.txt --output data/processed/oni_clean.csv
```

**3. Import dans PostgreSQL**, depuis `backend/` :

```powershell
Push-Location backend
.\.venv\Scripts\python.exe -m app.import_oni --csv ../data/processed/oni_clean.csv --provenance ../data/raw/noaa-cpc_oni-ersstv6_2026-11-09.provenance.json
Pop-Location
```

| Passage | Résultat affiché | Observations en base |
| --- | --- | --- |
| 1er | Import n°1 créé ; 921 ajoutées | 921 |
| 2e, même fichier | Import n°1 déjà enregistré ; 0 ajoutée, 921 déjà présentes à l'identique | 921 |

La fiche [`data/raw/…provenance.json`](data/raw/noaa-cpc_oni-ersstv6_2026-11-09.provenance.json)
apporte l'URL, l'empreinte, la date d'extraction et la version vérifiée. Si une
saison déjà en base arrive avec une autre valeur, l'import affiche le conflit et
se termine avec le code 1, sans rien écrire.

**4. API**, dans un second terminal :

```powershell
.\backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

```powershell
curl.exe "http://127.0.0.1:8000/api/v1/observations?start=2015-07-01&end=2016-03-01"
```

Réponse obtenue (HTTP 200, extrait) : neuf saisons de JJA 2015 à FMA 2016, dans
l'ordre chronologique, dont `{"reference_month":"2015-12-01","season":"NDJ","year":2015,"oni":2.59}`.
La réponse indique aussi la série (`ONI_ERSSTv6`), sa version, l'unité (°C) et la
source NOAA.

| Requête | Résultat obtenu |
| --- | --- |
| `?start=2015-12-01&end=2015-12-01` | 200 : NDJ 2015 seule (bornes incluses) |
| `?start=1940-01-01&end=1949-12-31` | 200 : `"observations":[]` |
| `?start=2015-02-30&end=2016-01-01` | 422 : date invalide sur `start` |
| `?start=2016-01-01&end=2015-01-01` | 422 : « La date de début (2016-01-01) est postérieure à la date de fin (2015-01-01). » |
| `?end=2016-01-01` | 422 : `start` manquant |
| Base arrêtée | 503 « Base de données indisponible. » en 5 s ; `/api/v1/health` reste à 200 |

Documentation interactive des paramètres : <http://127.0.0.1:8000/docs>.
Note pour le dossier : [NOTE_IMPORT_API.md](docs/NOTE_IMPORT_API.md).

## Démonstration de l'interface

Parcours exécuté le 15 novembre 2026 dans Chrome, sur les données réelles, avec
la base démarrée et les observations importées (étapes 1 à 3 ci-dessus).

**Terminal 1 — API**, depuis la racine :

```powershell
.\backend\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

**Terminal 2 — frontend** :

```powershell
npm.cmd --prefix frontend run dev
```

Puis ouvrir <http://127.0.0.1:5173>.

| Action | Résultat obtenu |
| --- | --- |
| Ouverture de la page | Toute la série : 921 saisons, de DJF 1950 à ASO 2026 ; anomalie la plus élevée +2,59 °C (NDJ 2015), la plus basse −2,04 °C (NDJ 1973) |
| Début 01/07/2015, fin 01/03/2016, « Afficher » | 9 saisons, de JJA 2015 à FMA 2016 ; mêmes valeurs que la requête `curl` ci-dessus ; 9 lignes dans le tableau |
| Focus sur la courbe, touche Début puis 5 fois → | Saison NDJ 2015 (nov. 2015 – janv. 2016) : +2,59 °C |
| Début 01/01/2016, fin 01/01/2015 | Message « La date de début (1er janvier 2016) est postérieure à la date de fin (1er janvier 2015). » ; aucune requête ; la courbe précédente reste affichée |
| 01/01/1940 au 31/12/1949 | « Aucune saison ONI du 1er janvier 1940 au 31 décembre 1949. La série commence avec la saison DJF 1950. » |
| API arrêtée, puis relancée et « Réessayer » | « L'API est injoignable ou en erreur (code HTTP 502) » (réponse du proxy Vite), puis retour des valeurs |
| Base arrêtée (`docker compose stop db`), puis redémarrée et « Réessayer » | « Chargement des observations… », puis « L'API répond, mais la base de données est indisponible. », puis retour des valeurs |
| Section de comparaison | 12 saisons par épisode ; El Niño 1997-1998 : de +0,71 °C (AMJ 1997) à +2,37 °C (NDJ 1997) ; La Niña 1988-1989 : de −1,85 °C (NDJ 1988) à −0,85 °C (MAM 1989) ; 12 saisons d'affilée au-delà du seuil pour chacun |
| Page affichée sur 390 px de large | Aucun défilement horizontal ; courbe de 309 px, graduations 1960 à 2020 |

Un point de la courbe représente une saison glissante de trois mois, placée à son
mois central, et non une mesure quotidienne. Les deux fenêtres comparées (mai à
avril) sont un choix du projet, pas des dates officielles d'épisode :
justification dans [DECISIONS.md, D29](docs/DECISIONS.md).

## Vérifications

```powershell
Push-Location backend
.\.venv\Scripts\python.exe -m pytest -q
Pop-Location
.\etl\.venv\Scripts\python.exe -m pytest etl/tests -q
npm.cmd --prefix frontend run lint
npm.cmd --prefix frontend test
npm.cmd --prefix frontend run build
```

Les tests du backend comprennent ceux du schéma, de l'import et de la route des
observations. Ils exigent PostgreSQL démarré et la base `enso_monitor_test`,
désignée par `TEST_DATABASE_URL`, qu'ils vident à chaque exécution. Sans cette
variable, ils sont ignorés.

Les tests du frontend (Vitest) n'ont besoin ni de l'API ni de la base : ils
affichent l'application dans un DOM simulé (jsdom) et remplacent l'API par une
fausse API qui filtre 15 valeurs **fictives** selon `start` et `end`. Ils
vérifient le parcours, pas les données NOAA ; l'intégration avec l'API réelle
est vérifiée par la [démonstration](#démonstration-de-linterface). Pour relancer
seulement le test du changement de période :

```powershell
npm.cmd --prefix frontend test -- -t "quand la période change"
```

Pour relancer seulement le test de la route filtrée (période valide et entrées
invalides) :

```powershell
Push-Location backend
.\.venv\Scripts\python.exe -m pytest tests/test_observations_api.py -v
Pop-Location
```

Dernière exécution complète, le 16 novembre 2026 : transformation **28 passed**,
backend **34 passed** (dont la route filtrée, 10 passed), frontend **12 passed** ;
lint et build sans erreur.

`build` lance d'abord la vérification TypeScript stricte, puis Vite produit `frontend/dist/`.
Pour consulter ce résultat localement, avec l'API toujours lancée :

```powershell
npm.cmd --prefix frontend run preview
```

Adresse : <http://127.0.0.1:4173>. Ce serveur sert à vérifier la compilation ; la
procédure de production sera traitée plus tard.

Avec les deux serveurs lancés, vérifier le chemin direct puis le proxy :

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/observations?start=2015-12-01&end=2015-12-01"
Invoke-RestMethod "http://127.0.0.1:5173/api/v1/observations?start=2015-12-01&end=2015-12-01"
```

Les résultats réellement obtenus sont consignés dans [le journal](docs/JOURNAL.md).

Les trois tests exigés par le sujet :

| Test exigé | État |
| --- | --- |
| Transformation des données NOAA | Réalisé : `etl/tests/test_transform_oni.py`, 28 cas, dont le fichier NOAA réel |
| Route API filtrée par période, avec entrée invalide | Réalisé : `backend/tests/test_observations_api.py`, 10 cas (période, bornes incluses, période vide, dates invalides, début après la fin, OpenAPI, 404, 503) |
| Changement de période dans le frontend | Réalisé : `frontend/src/App.test.tsx`. Après saisie d'une nouvelle période, le test vérifie le résumé, la valeur lue sur la courbe (y compris au clavier) et les lignes du tableau. Quatre autres cas : dates inversées, période vide, erreur réseau, comparaison. `frontend/src/stats.test.ts` : 7 cas sur les calculs et le formatage |

Le test de santé de l'API (`backend/tests/test_health.py`) ne remplace aucun d'eux.
Planification : [PLAN.md](docs/PLAN.md).

## Organisation des fichiers

```text
frontend/                  React, TypeScript strict, Vite, ESLint et Vitest
  src/App.tsx              Page : en-tête, courbe, comparaison
  src/api.ts               Appel GET /api/v1/observations et contrôle du JSON reçu
  src/useObservations.ts   Chargement par période : annulation, délai, nouvelle tentative
  src/format.ts            Dates, saisons et valeurs en °C à la française
  src/stats.ts             Seuil NOAA, résumé d'une période, plus longue suite au-delà du seuil
  src/components/
    PeriodFilter.tsx       Formulaire de période et contrôle des dates
    OniExplorer.tsx        États du chargement, résumé, courbe, source et tableau
    OniChart.tsx           Courbe SVG, sélection à la souris et au clavier
    ObservationsTable.tsx  Tableau des valeurs
    EpisodeComparison.tsx  El Niño 1997-1998 et La Niña 1988-1989 côte à côte
  src/App.test.tsx         Parcours : changement de période, erreurs, comparaison
  src/stats.test.ts        Calculs et formatage
  src/main.tsx             Montage de React
  src/styles.css           Présentation, responsive et focus visible
backend/
  app/main.py              Application FastAPI, route santé, réponse 503 si base injoignable
  app/observations.py      Route GET /api/v1/observations et schémas de réponse
  app/import_oni.py        Import du CSV ONI avec sa provenance, sans doublon
  app/database.py          DATABASE_URL, moteur et session SQLAlchemy, conventions de nommage
  app/models.py            Modèles source, climate_index, data_import, observation
  alembic.ini, alembic/    Configuration et migrations Alembic
  tests/conftest.py        Base PostgreSQL jetable partagée par les tests
  tests/test_health.py     Vérification du contrat HTTP initial
  tests/test_schema.py     Contraintes du schéma
  tests/test_import_oni.py Import : provenance, second import, conflits
  tests/test_observations_api.py  Route filtrée : période, bornes, erreurs
  requirements*.txt        Dépendances de l'API et des tests
etl/
  transform_oni.py         Validation, doublons, datation et export CSV des observations ONI
  tests/                   Tests Pytest de la transformation
  requirements*.txt        Dépendances de l'ETL et des tests
data/
  raw/                     Fichier NOAA brut daté, empreinte SHA-256 et provenance
  processed/               CSV produit par l'ETL (régénéré, non versionné)
compose.yaml               Service PostgreSQL local
.env.example               Modèle de configuration locale (le vrai .env est exclu de Git)
docs/
  DONNEES_NOAA.md          Source ONI ERSSTv6 : colonnes, saisons, limites, règles de transformation
  BASE_DE_DONNEES.md       Schéma relationnel, contraintes, provenance, hypothèses avant import
  EXIGENCES.md             Synthèse des huit pages du sujet officiel
  PLAN.md                  Préparation progressive et planning officiel prévisionnel
  DECISIONS.md             Choix, alternatives, limites et vérifications
  JOURNAL.md               Travail réel, vérifications et apports de l'IA
  GIT.md                   État du dépôt, revue des commits et publication GitHub
  dossier/                 Dossier de conception (source HTML, captures, export PDF)
  sujet/                   Copie locale du PDF officiel, exclue de Git
AGENTS.md                  Consignes pour les prochaines sessions assistées
```

## Git, configuration et données

La configuration locale tient dans `.env`, copié depuis `.env.example`. On y trouve
les variables du service PostgreSQL, `DATABASE_URL` et `TEST_DATABASE_URL`. `.env`
contient un mot de passe : il est exclu de Git et ne doit jamais être commité.
`.env.example` ne contient aucun vrai secret. L'exemple de réponse santé est une
réponse technique, pas une observation scientifique.

Les dépendances, `.venv`, `dist`, données de travail, fichiers temporaires et le PDF
officiel sont ignorés. Ne pas utiliser `git add -f` pour contourner ces exclusions.
Seul `data/raw/` est versionné dans `data/` : il contient la source NOAA brute,
jamais modifiée à la main (décision D11). Les fichiers produits dans `data/`,
comme `data/processed/oni_clean.csv`, restent exclus : ils se régénèrent avec la
commande de transformation.
Voir [les commandes de commits et de premier push](docs/GIT.md).

## Travail personnel et assistance IA

Codex a assisté la lecture du sujet, l'initialisation, le code du Jour 1,
la documentation et les vérifications. Au Jour 2, Claude a assisté la lecture
des sources NOAA, le téléchargement, les contrôles du fichier et la documentation.
Le 12 novembre, Claude a écrit le module de transformation, ses tests et la
documentation associée, à partir du cahier des charges de l'étudiant.
Le 14 novembre, Claude a mis en place PostgreSQL avec Docker Compose et écrit les
modèles, la migration, les tests du schéma et leur documentation, à partir du
cahier des charges de l'étudiant. Le même jour, en fin de journée, Claude a écrit
l'import, la route des observations, leurs tests et cette démonstration.
Le 15 novembre, Claude a écrit l'interface (courbe, filtre, tableau, comparaison),
choisi les deux épisodes et leurs fenêtres, écrit les tests Vitest et exécuté la
démonstration, à partir du cahier des charges de l'étudiant.
Le 16 novembre, Claude a revérifié le MVP sur les données réelles et rédigé le
dossier de conception, ses diagrammes et son script d'export.
Ces contributions sont détaillées dans le journal. La compréhension personnelle
et la validation par l'étudiant restent à confirmer ; elles ne sont pas déduites
du code généré ou des tests réussis.

Exercice du Jour 1 : modifier le texte d'introduction dans `frontend/src/App.tsx`,
observer la mise à jour de Vite et lancer `npm.cmd --prefix frontend run build`.
Puis expliquer pourquoi l'URL utilisée dans `fetchObservations` (`frontend/src/api.ts`)
commence par `/api`.

Exercice du Jour 2 : retrouver dans `data/raw/` la ligne `NDJ 1997`. Indiquer
les trois mois qu'elle couvre et la date `reference_month` prévue par D12. Puis
recalculer l'empreinte avec `Get-FileHash` et la comparer à `SHA256SUMS`.

## Références techniques consultées

- [Démarrer avec Vite](https://vite.dev/guide/) : prérequis et scripts locaux.
- [Premiers pas FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/) : application, serveur et documentation OpenAPI.
- Sujet officiel local, huit pages : voir [sa synthèse](docs/EXIGENCES.md).
- Sources NOAA consultées le 9 novembre 2026 : voir [la liste](docs/DONNEES_NOAA.md#sources-consultées-le-9-novembre-2026).

Étape suivante prévue : compléter les passages personnels du dossier, relire le
PDF, puis préparer l'oral (voir [PLAN.md](docs/PLAN.md)).
