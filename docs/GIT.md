# Git et publication GitHub

## État de la publication

- Dépôt : <https://github.com/Hugodrc55/ENSO-Monitor>.
- Distant `origin` : `https://github.com/Hugodrc55/ENSO-Monitor.git`.
- Branche `main`, qui suit `origin/main`.
- L'initialisation du 4 novembre a été organisée en commits le 8 novembre ; l'étude
  des données NOAA a été commitée le 9 novembre.
- Une première tentative de push, le 8 novembre, a été refusée faute
  d'autorisation explicite de publication.
- **Premier push le 10 novembre 2026** : les sept commits des 8 et 9 novembre ont
  été publiés. `git rev-parse HEAD` et `git ls-remote origin refs/heads/main`
  renvoyaient le même SHA, `6c4d9fb`.
- **Push du 12 novembre 2026** : les quatre commits de la transformation ont été
  publiés ; SHA local et distant identiques, `17a60c1`.
- **Push du 14 novembre 2026** : les quatre commits du schéma PostgreSQL ont été
  publiés ; SHA local et distant identiques, `284a0ac`.
- **Push du 14 novembre 2026 (soir)** : les six commits de l'import et de l'API
  ont été publiés (`284a0ac..12c1652`) ; SHA local et distant identiques, `12c1652`.
- **Push du 15 novembre 2026** : les cinq commits de l'interface ont été publiés
  (`12c1652..60a1941`) ; SHA local et distant identiques, `60a1941`.
- Chaque publication suit un accord explicite de l'étudiant.

## Commits du Jour 1

| Ensemble cohérent | Message |
| --- | --- |
| Conventions Git et structure | `chore: initialiser le dépôt et ses conventions` |
| API et test de santé | `feat: ajouter la route de santé FastAPI et son test` |
| Accueil React et communication API | `feat: relier l'accueil React à l'API` |
| Documentation et préparation de la publication | `docs: documenter le jour 1 et préparer sa publication` |

Ces commits correspondent au travail réel du Jour 1 et à son suivi. Ils ne
représentent pas quatre journées différentes et ne sont pas antidatés.
L'identité Git préexistante a été conservée.

## Commits du Jour 2 (9 novembre 2026)

| Ensemble cohérent | Fichiers | Message |
| --- | --- | --- |
| Fichier NOAA brut, empreinte, provenance et règles Git | `.gitignore`, `.gitattributes`, `data/raw/*` | `chore: ajouter les données NOAA ONI brutes et leur provenance` |
| Documentation scientifique | `docs/DONNEES_NOAA.md`, `etl/README.md` | `docs: documenter la source scientifique NOAA ONI` |
| Suivi du projet | `README.md`, `docs/PLAN.md`, `docs/DECISIONS.md`, `docs/JOURNAL.md`, `docs/GIT.md` | `docs: actualiser le suivi du jour 2` |

Ils sont créés à la date réelle de la session, sans modification des dates Git.

Revue des commits du Jour 2 :

```powershell
git log --oneline -3
git show --stat HEAD~2 HEAD~1 HEAD
git diff 83b875e HEAD
```

Contrôle du fichier brut tel qu'il est enregistré dans Git (Git Bash) :

```bash
git show HEAD:data/raw/noaa-cpc_oni-ersstv6_2026-11-09.txt | sha256sum
```

L'empreinte doit être `118c563331335c8649cdc2677e6be7ae89d1259d901345fcddbc2857af280f7f`.

## Commits du 12 novembre 2026

| Ensemble cohérent | Fichiers | Message |
| --- | --- | --- |
| État de la publication du 10 novembre | `README.md`, `docs/GIT.md`, `docs/JOURNAL.md` | `docs: consigner la première publication GitHub` |
| Transformation et ses dépendances | `etl/__init__.py`, `etl/transform_oni.py`, `etl/requirements.txt` | `feat: ajouter la transformation des observations ONI` |
| Tests de la transformation | `etl/tests/`, `etl/requirements-dev.txt` | `test: ajouter les tests de transformation ONI` |
| Documentation du traitement | `README.md`, `etl/README.md`, `docs/` | `docs: documenter le pipeline de transformation` |

## Commits du 14 novembre 2026

| Ensemble cohérent | Fichiers | Message |
| --- | --- | --- |
| Service PostgreSQL local | `compose.yaml`, `.env.example` | `chore: ajouter PostgreSQL local avec Docker Compose` |
| Modèles, configuration et première migration | `backend/requirements.txt`, `backend/app/database.py`, `backend/app/models.py`, `backend/alembic.ini`, `backend/alembic/` | `feat: ajouter le schéma PostgreSQL des observations` |
| Tests du schéma | `backend/tests/test_schema.py` | `test: vérifier les contraintes du schéma PostgreSQL` |
| Documentation | `README.md`, `docs/` | `docs: documenter le schéma PostgreSQL et sa migration` |

`.env`, qui contient le mot de passe local, est exclu de Git.

Import et API, le même jour en fin de journée :

| Ensemble cohérent | Fichiers | Message |
| --- | --- | --- |
| Provenance lisible par l'import | `data/raw/*.provenance.json`, `data/raw/README.md` | `chore: ajouter la fiche de provenance du fichier NOAA` |
| Import | `backend/app/import_oni.py` | `feat: importer les observations ONI dans PostgreSQL` |
| Route filtrée | `backend/app/observations.py`, `backend/app/main.py`, `backend/app/database.py` | `feat: ajouter la route GET /api/v1/observations` |
| Fixtures communes | `backend/tests/conftest.py`, `backend/tests/test_schema.py` | `refactor: partager la base de test entre les fichiers de tests` |
| Tests | `backend/tests/test_import_oni.py`, `backend/tests/test_observations_api.py` | `test: tester l'import et la route des observations` |
| Documentation | `README.md`, `etl/README.md`, `docs/` | `docs: documenter l'import et l'API des observations` |

## Commits du 15 novembre 2026

| Ensemble cohérent | Fichiers | Message |
| --- | --- | --- |
| Outils de test du frontend | `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.ts` | `chore: ajouter Vitest et Testing Library au frontend` |
| Courbe filtrable | `frontend/src/api.ts`, `useObservations.ts`, `format.ts`, `stats.ts`, `components/` (sauf la comparaison), `App.tsx`, `styles.css` | `feat: afficher la courbe ONI filtrable par période` |
| Comparaison d'épisodes | `frontend/src/components/EpisodeComparison.tsx`, `App.tsx`, `format.ts`, `stats.ts` | `feat: comparer un épisode El Niño et un épisode La Niña` |
| Tests | `frontend/src/App.test.tsx`, `frontend/src/stats.test.ts` | `test: tester le changement de période dans l'interface` |
| Documentation | `README.md`, `docs/` | `docs: documenter l'interface et le test frontend` |

Chaque commit de code a été compilé et vérifié par le lint dans une copie de
travail isolée (`git worktree`), à son propre état ; les tests ont été exécutés
sur le commit des tests.

## Commits du 16 novembre 2026

| Ensemble cohérent | Fichiers | Message |
| --- | --- | --- |
| Export du dossier | `docs/dossier/exporter.ps1`, `.editorconfig`, `.gitignore` | `chore: exporter le dossier de conception en PDF` |
| Dossier de conception | `docs/dossier/dossier.html`, `docs/dossier/captures/`, `docs/dossier/README.md` | `docs: ajouter le dossier de conception` |
| Suivi et lancement | `README.md`, `docs/` | `docs: consigner la revérification du MVP et le dossier` |

Le PDF du dossier (`docs/dossier/*.pdf`) est exclu de Git : il se régénère avec
`exporter.ps1`.

Revue des commits non publiés :

```powershell
git log --oneline origin/main..HEAD
git show --stat origin/main..HEAD
```

## Consulter le travail avant publication

Depuis la racine du projet :

```powershell
git status --short --branch
git remote -v
git log --oneline origin/main..HEAD
git diff --stat origin/main HEAD
git diff origin/main HEAD
git ls-tree -r --name-only HEAD
git check-ignore -v docs/sujet/HETIC_WEB3_Projet_ENSO_Monitor.pdf backend/.venv frontend/node_modules
```

`origin/main..HEAD` désigne les commits locaux qui ne sont pas encore publiés.
`git show --root d2fc989` permet de relire le commit initial. Le PDF officiel,
`.env`, les dépendances installées, les environnements virtuels, les fichiers
temporaires et les données produites dans `data/` (hors `data/raw/`) sont exclus.

## Publier de nouveaux commits, après autorisation explicite

`origin` est configuré et `main` suit `origin/main` : ne pas refaire
`git remote add origin` ni `git push -u`.

```powershell
git push
```

Cette commande envoie les commits et les fichiers suivis vers GitHub, où leur
accès dépend de la visibilité et des permissions du dépôt. Cela inclut la copie
brute du fichier NOAA dans `data/raw/`. Le PDF du sujet reste exclu. Git peut
demander une authentification. Ne jamais placer un jeton dans l'URL ou dans un
fichier du projet.

Si le distant a reçu d'autres commits entre-temps, examiner l'historique avant de
poursuivre. Aucun force-push, aucune réécriture d'historique.

## Vérifier le résultat du push

```powershell
git status --short --branch
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Le SHA local doit être identique à celui de `refs/heads/main` sur GitHub. Ne
déclarer la publication réussie qu'après cette vérification et consigner le
résultat réel dans le journal.

## Pour une prochaine modification autorisée

```powershell
git status --short
git diff
```

Ajouter uniquement les fichiers concernés, puis examiner l'index :

```powershell
git diff --cached --check
git diff --cached
```

Après revue et vérification, créer un commit précis avec `git commit -m`, puis
pousser seulement dans le périmètre autorisé. Ne pas recréer les commits initiaux.
