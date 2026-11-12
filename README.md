# ENSO Monitor

Projet individuel de rattrapage HETIC WEB3, développé progressivement avec une
validation personnelle à chaque étape. Début : **4 novembre 2026**.

Dépôt GitHub : [Hugodrc55/ENSO-Monitor](https://github.com/Hugodrc55/ENSO-Monitor),
publié depuis le **10 novembre 2026**. Voir [le suivi Git](docs/GIT.md).

## État actuel : Jour 2

**Jour 1** : une page React/TypeScript appelle `GET /api/v1/health` et affiche
si l'API FastAPI répond. Elle gère l'attente, l'échec et une nouvelle tentative.

**Jour 2** : la source scientifique a été étudiée et documentée. L'indice choisi
par l'étudiant est **NOAA ONI, version ERSSTv6**
([page NOAA](https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/index.php)).
Le fichier authentique `oni.ascii.txt` a été téléchargé le 9 novembre 2026 dans
[`data/raw/`](data/raw/README.md), avec son empreinte SHA-256. Il couvre 921
saisons, de DJF 1950 à ASO 2026. Format, unités, datation des saisons, différence
ONI/RONI et limites : voir [DONNEES_NOAA.md](docs/DONNEES_NOAA.md).

Aucune observation climatique n'est encore affichée ni importée. La transformation
(Jour 3), PostgreSQL, le graphique et la comparaison historique seront développés
aux journées prévues.

## Prérequis

- Node.js **22 à partir de 22.13**, ou **24 et supérieur**, avec npm ; environnement vérifié le 4 novembre : Node 22.18.0, npm 10.9.3 ; le 9 novembre : Node 22.23.4, npm 10.9.9. Ce minimum tient compte d'ESLint, en plus de Vite.
- Python **3.13** et Git ; environnement vérifié le 4 novembre : Python 3.13.7, Git 2.50.1 ; le 9 novembre : Python 3.13.17, Git 2.56.0.
- PowerShell sous Windows pour les commandes ci-dessous.
- Ni PostgreSQL ni Docker ne sont nécessaires aux Jours 1 et 2.

Les dépendances JavaScript sont figées dans `frontend/package-lock.json`.
Les versions Python directes sont fixées dans `backend/requirements*.txt`.
Les dépendances Python transitives sont résolues par pip à l'installation ;
ces fichiers ne constituent pas un verrouillage complet de l'environnement.

## Installation depuis la racine du dépôt

```powershell
python -m venv backend/.venv
.\backend\.venv\Scripts\python.exe -m pip install -r backend/requirements-dev.txt
npm.cmd --prefix frontend ci
```

L'appel direct à Python dans `.venv` évite de modifier la politique d'exécution
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

## Vérifications

```powershell
Push-Location backend
.\.venv\Scripts\python.exe -m pytest -q
Pop-Location
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

Le test de santé du Jour 1 ne couvre pas les trois tests finaux exigés :
transformation NOAA, route filtrée avec entrée invalide, changement de période
dans le frontend. Leur réalisation est planifiée dans [PLAN.md](docs/PLAN.md).

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
etl/README.md              Emplacement réservé ; aucune transformation
data/raw/                  Fichier NOAA brut daté, empreinte SHA-256 et provenance
docs/
  DONNEES_NOAA.md          Source ONI ERSSTv6 : colonnes, saisons, limites, plan du Jour 3
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
jamais modifiée à la main (décision D11). Les futurs fichiers produits dans
`data/` restent exclus.
Voir [les commandes de commits et de premier push](docs/GIT.md).

## Travail personnel et assistance IA

Codex a assisté la lecture du sujet, l'initialisation, le code du Jour 1,
la documentation et les vérifications. Au Jour 2, Claude a assisté la lecture
des sources NOAA, le téléchargement, les contrôles du fichier et la documentation.
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

La prochaine session est le Jour 3, consacré à la transformation du fichier
avec Pandas et NumPy, uniquement après validation de l'étudiant.
