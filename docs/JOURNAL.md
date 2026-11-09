# Journal réel du projet

Les dates correspondent aux sessions réellement effectuées. Le planning n'est
pas un historique prérempli. Les contributions de l'IA et la validation personnelle
de l'étudiant sont distinguées.

## 4 novembre 2026 — Jour 1

### Périmètre autorisé et travail produit

- Lecture complète du sujet officiel (huit pages), puis vérification de son rendu.
- Analyse des exigences et distinction entre préparation sur un mois et planning officiel sur cinq jours.
- Dépôt Git initialisé sur `main` ; conventions, exclusions et préparation du premier push.
- Accueil React/Vite, TypeScript strict, linting, communication HTTP isolée dans `api.ts`.
- Route FastAPI `GET /api/v1/health`, schéma Pydantic et test de son contrat HTTP.
- Proxy local Vite, états attente/succès/erreur, délai de cinq secondes et bouton de nouvelle tentative.
- Documentation du lancement, des décisions, du planning et des exigences.
- `etl/` réservé ; aucune donnée NOAA importée, aucun modèle PostgreSQL, graphique ou comparaison.

### Difficultés et corrections

- Le répertoire était vide et le PDF absent à la première demande. Aucune modification n'a été faite avant que l'étudiant indique sa copie dans `Downloads`.
- Les outils PDF manquaient. Ils ont été installés temporairement hors des dépendances applicatives ; le réseau et leur exécution ont nécessité une autorisation technique.
- La première création de `.venv` a échoué pendant `ensurepip` dans l'exécution restreinte. La création a été relancée avec l'autorisation technique et l'installation a pu aboutir.
- Sous PowerShell, les commandes utilisent `npm.cmd` et le Python de `.venv` directement pour éviter la dépendance à l'activation de scripts.
- ESLint 9 a été signalé non maintenu pendant l'installation : passage à ESLint 10. Les contraintes de `typescript-eslint` imposent TypeScript <6.1 : la version 6.0.3 remplace la dernière version 7 proposée par npm. Les types de Node correspondent à Node 22.
- Le premier test backend a réussi avec un avertissement de dépréciation `httpx` et un accès refusé au cache Pytest. Passage à `httpx2`, client attendu par Starlette, puis relance autorisée : test réussi sans ces avertissements.
- La compilation Vite a initialement échoué sur `spawn EPERM`, après réussite du typage et du lint. Relancée avec autorisation des sous-processus : compilation réussie, sans modification du code applicatif.
- Le contrôle navigateur n'a pas pu aboutir : connecteur navigateur indisponible, puis demande d'accès à Chrome expirée. Aucun contrôle visuel ou clic dans l'application n'est présenté comme effectué.
- Limite ouverte : 11 alertes npm modérées dans les dépendances de développement, liées à `minimatch`. Aucune alerte dans `npm audit --omit=dev`. Pas de `npm audit fix --force` ; suivre un correctif compatible (décision D09).

### Vérifications réelles

| Vérification exécutée | Résultat observé |
| --- | --- |
| `python -m pytest -q` depuis `backend`, avec le Python de `.venv` | **1 passed**, dernière exécution en 0,43 s, sans avertissement |
| Python de `.venv` : `-m pip check` | `No broken requirements found` |
| `npm.cmd run lint` depuis `frontend` | Code de sortie 0 |
| `npm.cmd run build` depuis `frontend` | TypeScript strict puis Vite réussis ; 17 modules transformés ; `dist/` généré et ignoré |
| `npm.cmd audit` | Code de sortie 1 : 11 alertes modérées dans l'outillage de développement, aucune haute ou critique |
| `npm.cmd audit --omit=dev` | Code de sortie 0 : zéro vulnérabilité signalée |
| GET réel `http://127.0.0.1:8000/api/v1/health` | HTTP 200, `{"status":"ok","service":"enso-monitor-api"}` |
| GET réel `http://127.0.0.1:5173/api/v1/health` | HTTP 200, JSON identique via le proxy Vite |
| GET réel `http://127.0.0.1:5173/` | HTTP 200 ; cela ne prouve pas le rendu dans un navigateur |
| GET réel `/openapi.json` | La route `/api/v1/health` est présente |
| Arrêt de l'API puis GET via Vite | HTTP 502 ; panne de connexion reproduite |
| Redémarrage de l'API puis GET via Vite | Retour HTTP 200 et JSON attendu |
| Inspection navigateur | Non effectuée : accès indisponible/autorisation expirée |
| `git check-ignore -v` | PDF officiel, `.env` (racine et backend), `.venv`, `node_modules`, `dist` et `tmp/` exclus |
| Relecture des 28 fichiers publiables par script | UTF-8, fin de ligne finale et absence d'espaces de fin : OK |
| `git status --short --branch` et `git remote -v` | Branche `main`, aucun commit, fichiers non suivis, aucun distant |

Les deux serveurs temporaires ont été arrêtés après vérification. La procédure de
lancement et le scénario de vérification visuelle restent disponibles dans le README.
Le responsive, les clics de nouvelle tentative et l'affichage réel des états restent
à vérifier dans un navigateur ; aucun test frontend automatisé n'a été créé au Jour 1.
Les trois tests minimaux du sujet restent planifiés pour les étapes correspondantes.

### Inventaire des fichiers créés

28 fichiers de code, configuration et documentation proposés à Git :

```text
.editorconfig
.gitattributes
.gitignore
AGENTS.md
README.md
backend/app/__init__.py
backend/app/main.py
backend/pytest.ini
backend/requirements.txt
backend/requirements-dev.txt
backend/tests/test_health.py
frontend/package.json
frontend/package-lock.json
frontend/index.html
frontend/tsconfig.json
frontend/vite.config.ts
frontend/eslint.config.js
frontend/src/main.tsx
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/styles.css
etl/README.md
docs/EXIGENCES.md
docs/PLAN.md
docs/DECISIONS.md
docs/JOURNAL.md
docs/GIT.md
docs/sujet/README.md
```

Copie locale supplémentaire : `docs/sujet/HETIC_WEB3_Projet_ENSO_Monitor.pdf`,
ignorée. `.git/` contient les métadonnées du dépôt. Les fichiers générés dans
`.venv`, `node_modules`, `dist`, les caches et `tmp/pdfs` sont locaux et ignorés.

### Git et validation personnelle

Dépôt local créé sur `main`, fichiers à relire avant commit. Aucun commit, distant
ou push effectué par l'assistant. Quatre commits proposés dans `GIT.md`.

### Contributions de l'IA

Codex a lu et synthétisé le sujet, proposé l'organisation, généré le code initial,
la configuration, le test de santé et les documents, installé les dépendances et
effectué les vérifications consignées ci-dessus. Le workflow Sites est limité
au travail local. Des outils PDF temporaires servent uniquement à lire l'épreuve.

La compréhension personnelle de l'étudiant, sa capacité à modifier ce code et
son accord pour le Jour 2 restent à confirmer. Exercice proposé : modifier
l'introduction de la page, reconstruire le frontend puis expliquer le trajet de
`/api/v1/health` entre React, Vite et FastAPI.

### Suite proposée, non commencée

Jour 2 : lecture et documentation de la source NOAA ONI ERSSTv6, format, unités,
périodes et limites. Attendre la validation de l'étudiant avant de commencer.

## 8 novembre 2026 — Préparation de la publication du Jour 1

### Demande et périmètre

L'étudiant a fourni `https://github.com/Hugodrc55/ENSO-Monitor.git` pour relier
son projet à GitHub. Cette session porte sur Git et la documentation du travail
déjà réalisé. Le Jour 2 n'a pas été commencé et aucune fonctionnalité n'a changé.

### Travail réalisé

- Consultation du dépôt distant par `git ls-remote --symref` : commande réussie,
  aucune référence retournée, dépôt vide.
- Configuration d'`origin` avec l'URL fournie. L'identité Git existante est conservée.
- Revue des 28 fichiers à publier et contrôle des exclusions et de motifs usuels
  de secrets : aucun fichier exclu ni motif détecté parmi les candidats.
- Création de commits séparant conventions, backend, frontend et documentation.
  Les commits sont créés à la date réelle de cette session, sans antidater le
  travail du 4 novembre ni simuler plusieurs journées.
- Mise à jour du README et du guide Git avec le dépôt exact et les commandes
  adaptées à un distant déjà configuré.

### Vérifications exécutées avant publication

| Commande ou contrôle | Résultat |
| --- | --- |
| Pytest depuis `backend` avec le Python de `.venv` | **1 passed** en 0,99 s ; avertissement d'écriture du cache dans l'environnement restreint |
| `python -m pip check` avec le Python de `.venv` | Aucune incompatibilité détectée |
| `npm.cmd run lint` | Réussi, code de sortie 0 |
| `npm.cmd run build` | Typage strict réussi ; Vite d'abord bloqué par `spawn EPERM`, puis compilation réussie après autorisation technique |
| `git diff --cached --check` avant les commits | Aucun problème d'espacement signalé |
| `git check-ignore -v` | PDF officiel, environnements, dépendances, fichiers de build, `.env` et temporaires exclus |

Aucun nouvel audit npm, test navigateur ou test HTTP avec serveurs lancés n'a été
effectué pendant cette session. Les résultats et limites du 4 novembre restent
datés de leur exécution et ne sont pas présentés comme revérifiés aujourd'hui.

### Publication bloquée

Une tentative de `git push --set-upstream origin main` a été **refusée avant
exécution par le contrôle automatique d'autorisation**. Motif : l'URL fournie
n'autorise pas assez explicitement l'envoi des contenus non publics du projet
vers GitHub. Aucun push n'a donc été exécuté et aucune synchronisation distante
n'est déclarée réussie. Une autorisation explicite de l'étudiant est nécessaire
avant une nouvelle tentative. Aucun contournement ni force-push n'a été effectué.

### Contribution de l'IA et suite

Codex a vérifié le distant, configuré Git, relu les fichiers, relancé les contrôles,
créé les commits locaux et actualisé cette documentation. Cela ne démontre pas
la compréhension personnelle de l'étudiant. Suite : obtenir l'accord pour
publier les commits du Jour 1, pousser, puis comparer le SHA local au SHA distant.
L'autorisation de commencer le Jour 2 reste distincte.

## 9 novembre 2026 — Jour 2 : source NOAA ONI ERSSTv6

### Demande et périmètre

L'étudiant a autorisé le Jour 2 uniquement : étude de la source NOAA, téléchargement
du fichier authentique et documentation. À partir de ce jour, l'assistance est
assurée par Claude (Claude Code), qui reprend le projet existant et son historique.
Exclus : PostgreSQL, SQLAlchemy, Alembic, API d'observations, graphiques,
comparaison d'épisodes et Docker.

### Reprise du Jour 1

- `git status` propre sur `main`, quatre commits du 8 novembre, aucun fichier manquant.
- Aucune branche amont, et `git ls-remote origin refs/heads/main` ne renvoie rien :
  **le Jour 1 n'a jamais été publié** sur GitHub.
- Sujet officiel relu en entier (8 pages). L'outil de lecture PDF exigeait
  `poppler`, absent : la lecture s'est faite sur les rendus PNG des 8 pages produits
  au Jour 1 dans `tmp/pdfs/`. Le PDF déclare bien 8 pages.
- Le Jour 1 fonctionne toujours : voir les vérifications ci-dessous.

### Travail réalisé

- Lecture des pages NOAA ONI v6, ONI v5, RONI, de l'index `/data/indices/` et du
  communiqué NWS 26-05 (13 janvier 2026).
- Téléchargement de `oni.ascii.txt` le 9 novembre 2026 à 13:42 UTC, puis copie
  identique dans `data/raw/noaa-cpc_oni-ersstv6_2026-11-09.txt`, avec `SHA256SUMS`
  et un README de provenance.
- Téléchargement temporaire, hors du dépôt, du fichier mensuel `detrend.nino34.ascii.txt`
  pour vérifier les définitions de `TOTAL`, `ANOM` et `YR`.
- `.gitignore` : seul `data/raw/` est versionné dans `data/`. `.gitattributes` :
  aucune conversion de fin de ligne pour les fichiers bruts.
- Création de `docs/DONNEES_NOAA.md`. Mise à jour d'`etl/README.md`, du README,
  du plan, des décisions (D10 à D14) et du guide Git.

### Constats sur la source

- `oni.ascii.txt` est bien la série **ERSSTv6** : l'index NOAA l'indique, et les
  valeurs concordent avec le tableau v6 (921/921), pas avec le v5 (495 écarts > 0,05).
- Depuis le **1er février 2026**, la NOAA utilise la **RONI** pour la surveillance
  officielle. L'ONI reste mis à jour. Ce point est soumis à la reconfirmation de
  l'étudiant (D13).
- `YR` est l'année du **mois central** de la saison (hypothèse vérifiée, l'autre rejetée).
- La page ONI v6 mentionne « ERSSTv5 » dans une phrase sur le filtrage, alors que
  le reste parle d'ERSSTv6 : incohérence signalée, sans interprétation.

### Difficultés et corrections

- Un `cd backend` dans une commande a changé le répertoire courant : la commande
  `npm --prefix frontend` suivante a échoué (`ENOENT`) dans `backend/`. Relance
  depuis la racine ; aucun fichier n'a été modifié.
- La console Windows (cp1252) a provoqué une `UnicodeEncodeError` à l'affichage
  des pages NOAA. `python -I` ignore `PYTHONIOENCODING` : utilisation de `-X utf8`.
- Bug dans un script de contrôle : les fins de ligne étaient comptées à 0, à cause
  d'un échappement incorrect. Après correction : 922 LF, aucun CR.
- Le sous-agent de lecture web n'a pas pu extraire le texte du PDF NWS 26-05. Le
  texte a été extrait par décompression des flux du PDF avec la bibliothèque
  standard. La première page étant répartie sur plusieurs flux, il a fallu les
  concaténer. Un heredoc altérait les antislashs : le code a été placé dans un fichier.
- Relecture critique de `DONNEES_NOAA.md` avant commit :
  - suppression d'une explication non tirée des sources (réchauffement des tropiques) ;
  - le seuil, formulé différemment selon les pages NOAA, est maintenant signalé ;
  - l'exemple d'arrondi est remplacé par un cas réel (`MAM 2026` : `0.46`, affiché 0,5).
- L'horloge locale indiquait 13:42:23 UTC, contre 13:42:35 GMT pour le serveur
  NOAA : les deux valeurs sont consignées.

### Vérifications réelles

| Vérification exécutée | Résultat observé |
| --- | --- |
| Pytest depuis `backend` (Python de `.venv`, cache désactivé) | **1 passed** en 2,47 s |
| `pip check` | `No broken requirements found.` |
| `npm.cmd --prefix frontend run lint` | Code de sortie 0 |
| `npm.cmd --prefix frontend run build` | Typage strict et Vite réussis ; 17 modules transformés |
| Uvicorn lancé, `GET /api/v1/health` | HTTP 200, `{"status":"ok","service":"enso-monitor-api"}` ; OpenAPI : `/api/v1/health` seule |
| Arrêt de l'API puis nouvel appel | Connexion refusée, comme attendu |
| Téléchargement `oni.ascii.txt` | HTTP 200, `text/plain; charset=utf-8`, 23 050 octets, aucune redirection, `Last-Modified` 3 novembre 2026 |
| Contenu | ASCII, 922 lignes LF, en-tête `SEAS YR TOTAL ANOM`, 921 lignes conformes, pas de HTML |
| Doublons, valeurs manquantes et sentinelles, continuité | Aucun doublon ni valeur manquante ; séquence continue de DJF 1950 à ASO 2026 |
| Comparaison avec les tableaux NOAA v6 et v5 | v6 : 921/921 à ≤ 0,05 ; v5 : 495 écarts > 0,05 |
| Recalcul depuis le fichier mensuel | `ANOM` : 919/921, `TOTAL` : 920/921 à 0,01 près (écart max 0,013) |
| Copie dans `data/raw/` | `cmp` identique ; `sha256sum -c SHA256SUMS` : OK |
| `git check-ignore -v` et `git check-attr` | PDF, `.venv`, `node_modules`, `tmp/`, `.env` et `data/processed/` exclus ; `data/raw/` suivi ; `text` désactivé sur le fichier brut |

Non effectué ce jour : audit npm, contrôle dans un navigateur, appel via le proxy
Vite. Les résultats du 4 novembre sur ces points ne sont pas présentés comme revérifiés.
Les scripts de contrôle étaient temporaires, hors du dépôt (D14). Aucun test
automatisé de données n'existe encore : il est prévu au Jour 5, et la
transformation au Jour 3.

### Git

Trois commits locaux, à la date réelle de la session (détail dans [GIT.md](GIT.md)) :

1. `chore: ajouter les données NOAA ONI brutes et leur provenance`
2. `docs: documenter la source scientifique NOAA ONI`
3. `docs: actualiser le suivi du jour 2`

Aucun push, aucune réécriture d'historique. La publication attend l'autorisation
explicite de l'étudiant.

### Contributions de l'IA

Claude a inspecté le projet, relancé les vérifications du Jour 1, lu les sources
NOAA, téléchargé et contrôlé les fichiers, écrit les scripts temporaires, rédigé
la documentation et préparé les commits. Cela ne démontre ni la compréhension
personnelle de l'étudiant, ni sa validation de D10 à D14 ; elles restent à
confirmer, en particulier la reconfirmation de l'ONI face à la RONI (D13).

Exercice proposé : retrouver la ligne `NDJ 1997`, indiquer ses trois mois et sa
date de référence, puis vérifier l'empreinte du fichier brut avec `Get-FileHash`.

### Suite proposée, non commencée

Jour 3 : transformation du fichier brut avec Pandas et NumPy, selon le plan de
`DONNEES_NOAA.md`. À commencer uniquement après l'accord de l'étudiant.
