# ENSO Monitor

Projet individuel de rattrapage HETIC WEB3, développé progressivement avec une
validation personnelle à chaque étape. Début : **4 novembre 2026**.

Dépôt GitHub : [Hugodrc55/ENSO-Monitor](https://github.com/Hugodrc55/ENSO-Monitor),
publié depuis le **10 novembre 2026**. Voir [le suivi Git](docs/GIT.md).

## État au 12 novembre 2026

- **Application (4 novembre)** : une page React/TypeScript appelle
  `GET /api/v1/health` et affiche si l'API FastAPI répond. Elle gère l'attente,
  l'échec et une nouvelle tentative.
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

Aucune observation n'est encore stockée en base ni affichée. PostgreSQL, l'API
d'observations, le graphique et la comparaison historique seront développés aux
étapes prévues dans [PLAN.md](docs/PLAN.md).

## Prérequis

- Node.js **22 à partir de 22.13**, ou **24 et supérieur**, avec npm ; environnement vérifié le 4 novembre : Node 22.18.0, npm 10.9.3 ; le 9 novembre : Node 22.23.4, npm 10.9.9. Ce minimum tient compte d'ESLint, en plus de Vite.
- Python **3.13** et Git ; environnement vérifié le 4 novembre : Python 3.13.7, Git 2.50.1 ; le 9 novembre : Python 3.13.17, Git 2.56.0.
- PowerShell sous Windows pour les commandes ci-dessous.
- Ni PostgreSQL ni Docker ne sont nécessaires à ce stade.

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
```

L'API et l'ETL ont chacun leur environnement Python : l'API n'installe pas
pandas. L'appel direct à Python dans `.venv` évite de modifier la politique d'exécution
PowerShell pour activer l'environnement. `npm.cmd` évite le même problème avec
le script `npm.ps1`. Les bibliothèques PDF utilisées par l'assistant pour lire
le sujet ne sont pas des dépendances de l'application.

## Lancement local

Ouvrir deux terminaux à la racine du dépôt.

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
    │ GET /api/v1/health sur le port 5173
    ▼
Vite : proxy local /api vers 127.0.0.1:8000
    ▼
FastAPI : route health() → réponse contrôlée par Pydantic
    │ {"status":"ok","service":"enso-monitor-api"}
    ▼
React : vérification du JSON, puis affichage « Service accessible »
```

Ce statut vérifie seulement la disponibilité HTTP de l'API. Il ne vérifie ni une
base de données, ni la fraîcheur des données NOAA. Le navigateur utilise une URL
relative ; il n'est pas nécessaire d'ouvrir une politique CORS pour ce fonctionnement
local. En cible, le routage sera documenté avec Caddy au Jour 13.

La requête expire après cinq secondes. Au démontage du composant, elle est annulée
et sa réponse est ignorée. React StrictMode peut provoquer une première requête
annulée en développement : le nettoyage de l'effet permet de le gérer.

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

## Vérifications

```powershell
Push-Location backend
.\.venv\Scripts\python.exe -m pytest -q
Pop-Location
.\etl\.venv\Scripts\python.exe -m pytest etl/tests -q
npm.cmd --prefix frontend run lint
npm.cmd --prefix frontend run build
```

`build` lance d'abord la vérification TypeScript stricte, puis Vite produit `frontend/dist/`.
Pour consulter ce résultat localement, avec l'API toujours lancée :

```powershell
npm.cmd --prefix frontend run preview
```

Adresse : <http://127.0.0.1:4173>. Ce serveur sert à vérifier la compilation ; la
procédure de production sera traitée plus tard.

Avec les deux serveurs lancés, vérifier le chemin direct puis le proxy :

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/health
Invoke-RestMethod http://127.0.0.1:5173/api/v1/health
```

Dans le navigateur : vérifier l'état accessible, arrêter l'API, cliquer sur
« Vérifier à nouveau », constater l'état indisponible, relancer l'API et réessayer.
Les résultats réellement obtenus sont consignés dans [le journal](docs/JOURNAL.md).

Les trois tests exigés par le sujet :

| Test exigé | État |
| --- | --- |
| Transformation des données NOAA | Réalisé : `etl/tests/test_transform_oni.py`, 28 cas, dont le fichier NOAA réel |
| Route API filtrée par période, avec entrée invalide | À développer |
| Changement de période dans le frontend | À développer |

Le test de santé de l'API (`backend/tests/test_health.py`) ne remplace aucun d'eux.
Planification : [PLAN.md](docs/PLAN.md).

## Organisation des fichiers

```text
frontend/                  React, TypeScript strict, Vite et ESLint
  src/App.tsx              Affichage et état de la connexion
  src/api.ts               Appel HTTP et contrôle du JSON reçu
  src/main.tsx             Montage de React
  src/styles.css           Présentation minimale
backend/
  app/main.py              Application FastAPI, schéma Pydantic et route santé
  tests/test_health.py     Vérification du contrat HTTP initial
  requirements*.txt        Dépendances de l'API et des tests
etl/
  transform_oni.py         Validation, doublons, datation et export CSV des observations ONI
  tests/                   Tests Pytest de la transformation
  requirements*.txt        Dépendances de l'ETL et des tests
data/
  raw/                     Fichier NOAA brut daté, empreinte SHA-256 et provenance
  processed/               CSV produit par l'ETL (régénéré, non versionné)
docs/
  DONNEES_NOAA.md          Source ONI ERSSTv6 : colonnes, saisons, limites, règles de transformation
  EXIGENCES.md             Synthèse des huit pages du sujet officiel
  PLAN.md                  Préparation progressive et planning officiel prévisionnel
  DECISIONS.md             Choix, alternatives, limites et vérifications
  JOURNAL.md               Travail réel, vérifications et apports de l'IA
  GIT.md                   État du dépôt, revue des commits et publication GitHub
  sujet/                   Copie locale du PDF officiel, exclue de Git
AGENTS.md                  Consignes pour les prochaines sessions assistées
```

## Git, configuration et données

Aucune variable d'environnement ou clé n'est requise aujourd'hui. Ne pas créer
de `.env` contenant des secrets dans Git. L'exemple de réponse santé est une réponse
technique, pas une observation scientifique.

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
Ces contributions sont détaillées dans le journal. La compréhension personnelle
et la validation par l'étudiant restent à confirmer ; elles ne sont pas déduites
du code généré ou des tests réussis.

Exercice du Jour 1 : modifier le texte d'introduction dans `frontend/src/App.tsx`,
observer la mise à jour de Vite et lancer `npm.cmd --prefix frontend run build`.
Puis expliquer pourquoi l'URL utilisée dans `fetchHealth` commence par `/api`.

Exercice du Jour 2 : retrouver dans `data/raw/` la ligne `NDJ 1997`. Indiquer
les trois mois qu'elle couvre et la date `reference_month` prévue par D12. Puis
recalculer l'empreinte avec `Get-FileHash` et la comparer à `SHA256SUMS`.

## Références techniques consultées

- [Démarrer avec Vite](https://vite.dev/guide/) : prérequis et scripts locaux.
- [Premiers pas FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/) : application, serveur et documentation OpenAPI.
- Sujet officiel local, huit pages : voir [sa synthèse](docs/EXIGENCES.md).
- Sources NOAA consultées le 9 novembre 2026 : voir [la liste](docs/DONNEES_NOAA.md#sources-consultées-le-9-novembre-2026).

Étape suivante prévue : modèle PostgreSQL, SQLAlchemy et migrations Alembic
(voir [PLAN.md](docs/PLAN.md)).
