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

## 10 novembre 2026 — Première publication sur GitHub

- Push de `main` vers `origin` (`git push -u origin main`), après l'accord explicite
  de l'étudiant : publication des sept commits des 8 et 9 novembre.
- Contrôle préalable des fichiers suivis : ni PDF du sujet, ni `.env`, ni
  environnement virtuel, ni dépendance installée.
- Vérification : `git rev-parse HEAD` et `git ls-remote origin refs/heads/main`
  renvoient le même SHA, `6c4d9fb`. `main` suit désormais `origin/main`.
- Aucun fichier du projet n'a été modifié ce jour-là.

## 12 novembre 2026 — Transformation des observations ONI

### Périmètre

Session consacrée à la lecture, la validation et la transformation du fichier
NOAA brut en observations datées, avec un premier test automatisé de données.

Exclus : modèle PostgreSQL, migrations, insertion en base, routes d'observations,
graphiques, comparaison d'épisodes et Docker.

### État de départ

- `main` propre et synchronisée avec `origin/main` (`6c4d9fb`).
- Fichier brut présent ; `sha256sum -c SHA256SUMS` : OK.
- Sujet relu (8 pages, rendus PNG de `tmp/pdfs/`). Exigences retenues :
  - ETL : « imports fiables, gestion des doublons, traçabilité NOAA » ;
  - test de données : vérifier une transformation « (ex. doublons ou date invalide) ».
- `README.md` et `docs/GIT.md` décrivaient encore un dépôt distant vide : corrigés
  dans un commit séparé, avec l'entrée du 10 novembre.

### Travail réalisé

- `etl/transform_oni.py` enchaîne les étapes du traitement :
  - contrôle SHA-256 ;
  - lecture pandas en texte ;
  - validation ligne par ligne ;
  - doublons ;
  - datation par le mois central ;
  - signalement des trous ;
  - export CSV.

  Commande : `python -m etl.transform_oni --input … --output …`.
- `etl/tests/test_transform_oni.py` : 16 fonctions de test, 28 cas. Les petits
  fichiers de test ont des valeurs fictives, déclarées comme telles ; un test
  utilise le fichier NOAA réel.
- `etl/requirements.txt` (pandas 3.1.1, NumPy 2.5.4) et `etl/requirements-dev.txt`
  (pytest 9.2.0). Environnement `etl/.venv`, ignoré par Git.
- Documentation : section 10 de `DONNEES_NOAA.md`, `etl/README.md`, README, plan,
  décisions D15 à D18, mise à jour de D12.

### Constats et corrections

- **Comportement de pandas, testé avant d'écrire le module** sur de petits
  fichiers mal formés :
  - avec l'en-tête automatique, une ligne comportant un champ de plus décale
    toutes les colonnes sans erreur ;
  - avec `index_col=False`, la ligne est tronquée avec un simple avertissement.

  D'où la lecture sans en-tête automatique et l'en-tête contrôlé (D16).
- **Conversion numérique** : `pd.to_numeric` accepte `inf` et `1e3`. D'où le
  contrôle `np.isfinite` et les bornes physiques (D18).
- **Codes de valeur manquante** : aucun n'est défini sur les pages NOAA ONI v6,
  RONI et index enregistrées le 9 novembre, ni présent dans le fichier mensuel.
  Aucun code n'est donc interprété.
- **Doublons** : l'approche du 9 novembre (refus du fichier au premier doublon)
  est remplacée par la distinction entre copies et contradictions (D17), comme
  le demande le cahier des charges de la session.
- **Corrections après relecture du code** :
  - un accord grammatical dans le bilan (« 1 doublons ») ;
  - deux lignes de plus de 99 caractères ;
  - un motif de rejet d'année trop étroit (le format invalide n'était pas mentionné).
- **Documentation** : deux références (documentation pandas et Pytest) ont été
  retirées avant commit, car elles n'avaient pas été consultées pendant la session.
- **Affichage** : dans Git Bash, les accents des messages s'affichent mal (console
  non UTF-8), mais correctement sous PowerShell. Le code n'est pas en cause.

### Vérifications réelles

| Vérification exécutée | Résultat observé |
| --- | --- |
| `python -m pytest etl/tests -W error` (Python de `etl/.venv`) | **28 passed** en 0,79 s |
| Transformation du fichier réel, avertissements traités comme des erreurs | 921 lignes lues, 921 valides, 0 doublon, 0 rejet, 0 trou ; code de sortie 0 |
| Contrôle indépendant du CSV (script temporaire, bibliothèque standard) | 921 lignes ; chaque valeur égale au brut (comparaison décimale exacte) ; dates conformes à D12 ; tri strict ; aucun CR ; 0 erreur |
| Deux exécutions successives | CSV identiques octet pour octet (SHA-256 `4b1f7a77…`) |
| Erreurs volontaires introduites puis retirées : mois central décalé, dernière copie gardée, bornes à ±100 | 11, 1 et 1 tests en échec ; module restauré à l'identique (empreinte vérifiée), 28 passed |
| Commande avec fichier absent, page HTML, fichier fictif à doublons et saison inconnue, sans argument | Messages explicites ; codes de sortie 1, 1, 1 et 2 |
| Environnement neuf installé depuis `etl/requirements-dev.txt` | 28 passed |
| `pip check` dans `etl/.venv` | Aucun conflit |
| Pytest de l'API | 1 passed |
| `git status` | `data/processed/` et `etl/.venv` ignorés |

Non effectué ce jour : lint et build du frontend (aucun fichier frontend modifié),
contrôle dans un navigateur, audit npm.

### Git

Quatre commits à la date réelle de la session (détail dans [GIT.md](GIT.md)) :

1. `docs: consigner la première publication GitHub`
2. `feat: ajouter la transformation des observations ONI`
3. `test: ajouter les tests de transformation ONI`
4. `docs: documenter le pipeline de transformation`

Publication : push le 12 novembre, après l'accord explicite de l'étudiant. SHA
local et distant identiques, `17a60c1`.

### Contributions de l'IA

**Fourni par l'étudiant** : le cahier des charges de la session, c'est-à-dire
les étapes, les contrôles attendus, la règle du mois central, la commande et les
cas de test.

**Réalisé par Claude** :
- vérification de l'état du projet ;
- essais du comportement de pandas ;
- écriture du module de transformation, des tests et de cette documentation ;
- installation des dépendances ;
- exécution des vérifications ci-dessus.

### Limites ouvertes

- L'URL, la date d'extraction et le `Last-Modified` ne figurent pas dans le CSV.
  Ils seront enregistrés lors du chargement en base.
- L'année maximale acceptée dépend de l'horloge de la machine.
- Aucune comparaison entre deux extractions NOAA n'existe encore.

## 14 novembre 2026 — Base PostgreSQL, modèles et première migration

### Périmètre

Mise en place de PostgreSQL en local, des modèles SQLAlchemy et de la première
migration Alembic. Exclus : import des observations NOAA, API d'observations,
graphiques.

### État de départ

- `main` propre et synchronisée avec `origin/main` (`17a60c1`) ; aucune
  modification non commitée.
- **Base de données** : aucune configuration existante (ni Compose, ni `.env`, ni
  modèles). Docker Desktop était installé mais arrêté, aucun PostgreSQL n'était
  installé et le port 5432 était libre.
- **CSV de la transformation** : présent et inchangé (SHA-256 `4b1f7a77…`). Ses
  colonnes ont été relues ; `total_c` et `anom_c` ont au plus deux décimales.
- **Provenance** : dans `data/raw/README.md` (URL, dates, `Last-Modified`,
  SHA-256), avec la version ERSSTv6 confirmée le 9 novembre (D10). Rien ne manque,
  mais ces informations ne sont lisibles qu'en Markdown.
- **Sujet** : pages 3 et 5 relues (couche données, entités UML, schéma
  relationnel). Les huit pages avaient été lues le 12 novembre.

### Travail réalisé

- **Service PostgreSQL** : `compose.yaml` décrit un service `postgres:18.7-alpine`
  accessible sur `127.0.0.1`, avec un volume nommé et un contrôle de santé.
  `.env.example` sert de modèle. Le `.env` local, exclu de Git, a été créé depuis
  ce modèle avec un mot de passe aléatoire.
- **Modèles** : `backend/app/database.py` (lecture de `DATABASE_URL`, conventions
  de nommage) et `backend/app/models.py` (quatre tables).
- **Migration** : `86057118b37f`, générée par `alembic revision --autogenerate`,
  puis relue.
- **Tests** : `backend/tests/test_schema.py`, 9 fonctions et 15 cas, sur une base
  jetable.
- **Dépendances de l'API** : SQLAlchemy 2.1.8, Alembic 1.20.1, psycopg 3.3.9
  (`binary`) et python-dotenv 1.2.4.
- **Documentation** :
  - `docs/BASE_DE_DONNEES.md`, nouveau ;
  - README ;
  - décisions D19 à D22 ;
  - plan, guide Git et `DONNEES_NOAA.md`.

### Constats et corrections

- Docker Desktop a été démarré pour la session. Le premier téléchargement de
  l'image (environ 400 Mo) a duré plus de six minutes.
- Pour PostgreSQL 18, l'image officielle range ses données sous `/var/lib/postgresql`
  (`PGDATA=/var/lib/postgresql/18/docker`). Ce point a été vérifié dans la
  configuration de l'image avant de fixer le volume.
- Le script SQL de test du doublon contenait deux erreurs, corrigées avant de
  conclure :
  - des dates traitées comme du texte dans un `UNION ALL`, d'où une conversion
    `::timestamptz` ajoutée ;
  - un second import fictif daté du 9 décembre 2026, c'est-à-dire dans le futur.
    `ck_data_import_imported_after_download` l'a refusé, ce qui est le
    comportement attendu ; la date fictive a été remplacée par le 10 novembre.

  À chaque essai, la transaction a été annulée et aucune ligne n'est restée.
- Relecture : trois lignes de test trop longues et un message de `compose.yaml`
  raccourcis.

### Vérifications réelles

| Vérification exécutée | Résultat observé |
| --- | --- |
| `docker compose config`, puis `docker compose up -d --wait db` | Fichier valide ; service *healthy* ; PostgreSQL 18.7 sur `127.0.0.1:5432` |
| `alembic revision --autogenerate` | 4 tables et 1 index détectés ; révision `86057118b37f` |
| `alembic upgrade head --sql` | SQL relu : une transaction, 4 tables, contraintes nommées |
| Base jetable `enso_monitor_test` : `upgrade head`, puis `current` | `86057118b37f (head)` ; tables, contraintes et index présents (`\dt`, `pg_constraint`, `pg_indexes`) |
| Lignes fictives : même saison chargée par deux imports | Refus par `uq_observation_climate_index_id_year_season` ; transaction annulée, 0 ligne restante |
| `downgrade base`, puis `upgrade head`, sur la base jetable | Seule `alembic_version` reste, puis retour à `head` |
| `python -m pytest -W error` depuis `backend` | **16 passed** (1 test de santé, 15 tests de schéma) en 1,35 s |
| Erreurs volontaires dans une copie de la migration : `data_import_id` ajouté à l'unicité, contrôle de date supprimé | 2 tests en échec dans chaque cas ; migration restaurée à l'identique, 16 passed |
| Base de développement `enso_monitor` : `upgrade head`, puis `current` | `86057118b37f (head)` ; 0 observation |
| `alembic check` | « No new upgrade operations detected » : modèles et migration identiques |
| Base arrêtée : API lancée, puis `GET /api/v1/health` | HTTP 200 ; test de santé : 1 passed |
| Arrêt et redémarrage du service | Révision toujours présente : le volume conserve les données |
| Environnement neuf installé depuis `backend/requirements-dev.txt` | `pip check` sans conflit ; 16 passed |
| `git check-ignore` | `.env` ignoré ; `.env.example` suivi |

Non relancés ce jour : tests de l'ETL, lint et build du frontend (aucun de ces
fichiers n'a été modifié), contrôle dans un navigateur.

### Git

Quatre commits à la date réelle de la session (détail dans [GIT.md](GIT.md)) :

1. `chore: ajouter PostgreSQL local avec Docker Compose`
2. `feat: ajouter le schéma PostgreSQL des observations`
3. `test: vérifier les contraintes du schéma PostgreSQL`
4. `docs: documenter le schéma PostgreSQL et sa migration`

Publication : push le 14 novembre, après l'accord explicite de l'étudiant. SHA
local et distant identiques, `284a0ac`.

### Contributions de l'IA

**Fourni par l'étudiant** : le cahier des charges de la session :
- la stack ;
- la chaîne Source → Indice → Import → Observation ;
- les exigences de provenance et d'intégrité, dont la contrainte d'unicité de départ ;
- les vérifications attendues.

**Réalisé par Claude** :
- vérification de l'environnement et démarrage de Docker Desktop ;
- écriture du service Compose, des modèles, de la migration, des tests et de
  cette documentation ;
- installation des dépendances ;
- exécution des vérifications ci-dessus.

### Avant l'import

Les hypothèses à confirmer sont listées dans
[BASE_DE_DONNEES.md](BASE_DE_DONNEES.md#5-hypothèses-à-confirmer-avant-limport) :
- provenance lisible par un programme ;
- date d'extraction retenue ;
- création des lignes de référence ;
- règle en cas de révision NOAA ;
- refus d'une troisième décimale ;
- emplacement du programme d'import.

## 14 novembre 2026 (fin de journée) — Import des observations et API filtrée

### Périmètre

Démontrer le trajet fichier NOAA → PostgreSQL → API FastAPI filtrée, en vue de la
remise du 22 novembre. Exclus : graphique et comparaison d'épisodes.

### État de départ

- `main` propre et synchronisée avec `origin/main` (`284a0ac`).
- Docker en marche ; migration `86057118b37f (head)` déjà appliquée sur la base de
  développement, qui ne contenait aucune observation.
- Tests de la transformation : 28 passed. Le CSV régénéré est identique au précédent
  (SHA-256 `4b1f7a77…`).
- Seul prérequis manquant : une provenance lisible par un programme.

### Travail réalisé

- `data/raw/noaa-cpc_oni-ersstv6_2026-11-09.provenance.json` : fiche de provenance,
  valeurs reprises de `data/raw/README.md` (D23).
- `backend/app/import_oni.py` : import du CSV avec contrôle de la fiche, de
  l'empreinte et des décimales. Pas de doublon, conflits signalés sans écriture (D24).
- `backend/app/observations.py`, `backend/app/main.py`, `backend/app/database.py` :
  route `GET /api/v1/observations`, réponse 503 si la base est injoignable, session
  par requête et délai de connexion (D25).
- **Tests** :
  - `backend/tests/conftest.py` regroupe la base de test (D26) ;
  - `test_import_oni.py` : 8 cas ;
  - `test_observations_api.py` : 10 cas.
- **Documentation** : démonstration du README, `NOTE_IMPORT_API.md` pour le dossier,
  décisions D23 à D26, et mises à jour du plan, de `BASE_DE_DONNEES.md` (hypothèses
  tranchées), de `DONNEES_NOAA.md`, d'`etl/README.md` et du guide Git.

### Constats et corrections

- **Test « base indisponible » lent** : il durait 130 s, car sous Windows une
  connexion vers un port fermé insiste environ deux minutes. Un délai de connexion
  le ramène à 2 s.
- **Même problème pendant la démonstration réelle** : base arrêtée, la route ne
  répondait pas en 60 s (curl a abandonné, code 000). Correctif :
  `connect_timeout` de 5 s dans `create_db_engine`. Ensuite, réponse 503 en 5,1 s,
  puis 200 après le redémarrage de la base.
- **Relecture du code** : dix lignes trop longues ont été reformatées, et le conflit
  est maintenant construit avec des arguments nommés. Les tests et la démonstration
  d'import ont été relancés après ces changements.

### Vérifications réelles

| Vérification exécutée | Résultat observé |
| --- | --- |
| `alembic upgrade head`, `current`, `check` (base de développement) | `86057118b37f (head)` ; « No new upgrade operations detected » |
| `python -m pytest etl/tests` | 28 passed |
| `python -m pytest -W error` depuis `backend` | **34 passed** en 3,5 s (santé 1, import 8, route 10, schéma 15) |
| Erreurs volontaires : conflit ignoré, borne de fin exclue, contrôle début/fin supprimé | 1 test en échec dans chaque cas ; fichiers restaurés à l'identique, 34 passed |
| Import réel, 1er passage | « Import n°1 : créé » ; 921 ajoutées ; 921 observations et 1 import en base |
| Import réel, 2e passage du même fichier | « déjà enregistré (même empreinte) » ; 0 ajoutée, 921 identiques ; 921 observations et 1 import |
| Requête SQL sur NDJ 2015 | Ligne 793 du fichier brut, extraction le 2026-11-09 13:42:35 UTC, série `ONI_ERSSTv6`, source `NOAA_CPC` |
| Import d'une copie modifiée (NDJ 2015 : 2.59 → 2.60, hors du dépôt) | Conflit affiché, code 1 ; toujours 921 observations, NDJ 2015 = 2.59 |
| `GET /api/v1/observations?start=2015-07-01&end=2016-03-01` (API locale) | 200 ; 9 saisons de JJA 2015 à FMA 2016 ; NDJ 2015 = 2.59, DJF 2016 = 2.5 |
| `?start=2015-12-01&end=2015-12-01` | 200 ; NDJ 2015 seule (bornes incluses) |
| `?start=1940-01-01&end=1949-12-31` | 200 ; liste vide |
| `?start=2015-02-30&…`, début après la fin, `start` manquant | 422, 422 (message en français), 422 |
| Base arrêtée | `/api/v1/health` 200 ; `/api/v1/observations` 503 en 5,1 s |

Non relancés : lint et build du frontend (aucun fichier frontend modifié),
contrôle dans un navigateur.

### Git

Six commits à la date réelle de la session (détail dans [GIT.md](GIT.md)) :
1. `chore: ajouter la fiche de provenance du fichier NOAA`
2. `feat: importer les observations ONI dans PostgreSQL`
3. `feat: ajouter la route GET /api/v1/observations`
4. `refactor: partager la base de test entre les fichiers de tests`
5. `test: tester l'import et la route des observations`
6. `docs: documenter l'import et l'API des observations`

### Contributions de l'IA

**Fourni par l'étudiant** : le cahier des charges de la session :
- le trajet à démontrer ;
- la règle « deux imports, aucun ajout au second » ;
- le signalement des conflits sans écrasement ;
- le contrat de la route : bornes incluses, liste vide, erreurs claires ;
- les tests attendus.

**Réalisé par Claude** :
- fiche de provenance ;
- import, route, tests et documentation ;
- exécution des vérifications et de la démonstration ;
- correction du délai de connexion.

### Limites ouvertes

- Un fichier NOAA révisé sera refusé : la règle d'acceptation des révisions reste
  à définir.
- L'import fait confiance au CSV : il vérifie le fichier brut que le CSV désigne,
  mais pas que le CSV en dérive.
- Restent : l'interface, la courbe, le test frontend, la comparaison et le dossier.

### Publication

Après accord de l'étudiant, `git push` a publié les six commits
(`284a0ac..12c1652 main -> main`). `git rev-parse HEAD` et
`git ls-remote origin refs/heads/main` renvoyaient tous deux
`12c165214adb97a8ed2fc47785e765bf6adc6023`.

## 15 novembre 2026 — Interface : courbe filtrable, comparaison et test frontend

### Périmètre

Terminer l'interface du MVP : courbe ONI filtrable par période, comparaison de
deux épisodes historiques, test frontend exigé par le sujet. API et base inchangées.

### État de départ

- `main` propre et synchronisée avec `origin/main` (`12c1652`) ; conteneur
  PostgreSQL en marche, 921 observations en base.
- Contrat de l'API vérifié par des requêtes réelles avant toute modification :
  - paramètres `start` et `end` ;
  - réponse : `series` (`code`, `name`, `version`, `unit`, `source`), `start`,
    `end`, et `observations` (`reference_month`, `season`, `year`, `oni`) ;
  - en cas de 422, `detail` est une phrase (début après la fin) ou une liste
    Pydantic (date invalide).

  Aucun blocage à corriger côté API.

### Travail réalisé

- **Outils de test** : Vitest, jsdom et Testing Library, script `test` (D30). jsdom
  impose Node 22.22.2 au minimum : champ `engines` et prérequis du README mis à jour.
- **Appels et état** : `api.ts` (`fetchObservations`, contrôle du JSON) et
  `useObservations.ts` (annulation, délai de 10 s, nouvelle tentative) (D28).
- **Composants** : `PeriodFilter`, `OniChart` (SVG, D27), `ObservationsTable`,
  `OniExplorer` et `EpisodeComparison` (D29).
- **Calculs et formatage** : `format.ts` et `stats.ts`.
- **Page** : `App.tsx` et `styles.css`. La carte « État du service » est retirée
  (D28).
- **Tests** : `App.test.tsx` (5 cas de parcours) et `stats.test.ts` (7 cas).

### Constats et corrections

- **Espaces insécables** : l'outil d'édition de l'assistant a écrit le caractère
  lui-même à la place de son échappement. ESLint l'a refusé
  (`no-irregular-whitespace`). Correction : une constante `NBSP` dans `format.ts`.
- **Clé React inutile** : une erreur volontaire (courbe non recréée au changement
  de période) n'a fait échouer aucun test. La cause est que la courbe n'est pas
  affichée pendant le chargement : elle est donc toujours recréée. La clé a été
  retirée, avec un commentaire qui l'explique.
- **Code mort** : `countWhere` n'était utilisée nulle part ; elle a été supprimée.
- **`npm audit`** : 9 alertes modérées, toutes dues à `minimatch` via ESLint et
  typescript-eslint. Les outils de test ajoutés n'y sont pour rien ; non traitées.
- **Vérification mobile** : Chrome headless ne descend pas à 390 px de large, la
  première capture était donc trompeuse. La mesure a été refaite dans un cadre
  (iframe) de 390 px. L'extension Chrome ne parvenait pas non plus à faire de
  capture d'écran : ses vérifications ont été faites par lecture du DOM.

### Vérifications réelles

| Vérification exécutée | Résultat observé |
| --- | --- |
| Requêtes réelles avant modification | 200 sur 2015-07-01 → 2016-03-01 (9 saisons) ; 422 sur début après la fin et sur 2015-02-30 |
| `npm run typecheck`, `npm run lint` | Sans erreur |
| `npm test` | **12 passed** (2 fichiers) en 3,4 s |
| Erreur volontaire : le formulaire ne transmet plus la période | Test principal en échec ; fichier restauré à l'identique, 12 passed |
| `npm run build` | Réussi ; JavaScript 237,93 kB (75,28 kB gzip), CSS 4,79 kB |
| Commits de code compilés chacun dans un `git worktree` | Build et lint réussis à chaque commit ; 12 passed sur le commit des tests |
| Chrome, API et PostgreSQL réels : ouverture | 921 saisons, DJF 1950 → ASO 2026 ; +2,59 °C (NDJ 2015) et −2,04 °C (NDJ 1973) |
| Période 2015-07-01 → 2016-03-01 | 9 saisons, JJA 2015 → FMA 2016, mêmes valeurs que `curl` ; 9 lignes au tableau |
| Courbe au clavier : Début puis 5 fois → | NDJ 2015 : +2,59 °C ; contour de focus de 3 px visible |
| Dates inversées | Message, aucune requête, valeurs précédentes conservées |
| 1940-01-01 → 1949-12-31 | Message « Aucune saison ONI… » ; pas de courbe, source affichée |
| API arrêtée | « L'API est injoignable ou en erreur (code HTTP 502) » ; les valeurs reviennent après relance et « Réessayer » |
| Base arrêtée | « Chargement des observations… », puis « L'API répond, mais la base de données est indisponible. » ; les valeurs reviennent après redémarrage |
| Comparaison | 12 saisons chacune ; +0,71 à +2,37 °C ; −1,85 à −0,85 °C ; 12 saisons d'affilée au-delà du seuil pour chacune |
| Cadre de 390 px | Aucun défilement horizontal ; courbe de 309 px ; graduations 1960 à 2020 |
| Contrastes (formule WCAG) | Textes de 5,30:1 à 12,17:1 ; bordure des champs 4,06:1 ; seuils et focus de 5,37:1 à 6,13:1 |
| Commandes `Invoke-RestMethod` du README, direct et par le proxy | NDJ 2015, 2.59, par les deux chemins |

Non vérifiés : affichage sur un vrai téléphone et lecture avec un lecteur d'écran.

### Git

Cinq commits à la date réelle de la session (détail dans [GIT.md](GIT.md)) :
1. `chore: ajouter Vitest et Testing Library au frontend`
2. `feat: afficher la courbe ONI filtrable par période`
3. `feat: comparer un épisode El Niño et un épisode La Niña`
4. `test: tester le changement de période dans l'interface`
5. `docs: documenter l'interface et le test frontend`

### Contributions de l'IA

**Fourni par l'étudiant** : le cahier des charges de la session :
- une courbe filtrable, avec dates, °C et source visibles ;
- les valeurs consultables sans souris ;
- un épisode El Niño et un épisode La Niña comparés à partir de l'API, sans bornes présentées comme officielles ;
- les états à vérifier ;
- un test qui vérifie l'affichage ;
- les consignes Git.

**Réalisé par Claude** :
- le choix des épisodes et des fenêtres ;
- le code, les tests et la documentation ;
- l'exécution de la démonstration et des vérifications.

La compréhension et la validation personnelles de l'étudiant restent à confirmer.

### Limites ouvertes

- La date d'extraction n'est pas affichée dans l'interface : l'API ne la renvoie pas.
- Aucun test automatisé de bout en bout (navigateur, API et base) : l'intégration
  repose sur la démonstration manuelle.
- La période choisie n'est pas conservée dans l'URL.
- Restent : la documentation du déploiement et le dossier de conception.

### Publication

Après accord de l'étudiant, `git push` a publié les cinq commits
(`12c1652..60a1941 main -> main`). `git rev-parse HEAD` et
`git ls-remote origin refs/heads/main` renvoyaient tous deux
`60a1941ef835fd6e37c3ec983283e08c217cf49b`.

## 16 novembre 2026 — Revérification du MVP et dossier de conception

### Périmètre

Vérifier les quatre fonctionnalités du MVP sur les vraies données, relancer les
trois tests exigés, puis rédiger le dossier de conception de 15 pages au plus.
Aucune mise en ligne.

### État de départ

`main` propre et synchronisée avec `origin/main` (`60a1941`) ; conteneur
PostgreSQL en marche ; sujet officiel relu (8 pages).

### Vérifications réelles du MVP

| Vérification exécutée | Résultat observé |
| --- | --- |
| `pytest etl/tests -q` | **28 passed** en 4,2 s |
| `pytest -q -W error` depuis `backend` | **34 passed** en 4,8 s |
| `pytest tests/test_observations_api.py -v` depuis `backend` | **10 passed** en 3,2 s (période, bornes, période vide, 4 dates invalides, début après la fin, OpenAPI, 404, 503) |
| `npm.cmd --prefix frontend test` | **12 passed** en 5,8 s |
| `npm run lint`, `npm run build` | Sans erreur ; JavaScript 237,93 kB (75,28 kB gzip) |
| Base jetable `enso_monitor_verif` : migration, transformation, deux imports | `86057118b37f (head)` ; 921 lignes valides, CSV identique (`4b1f7a77…`) ; import 1 : 921 ajoutées ; import 2 : 0 ajoutée, 921 identiques, 1 seul import ; base supprimée ensuite |
| API réelle sur la base de développement | 200 sur 2015-07-01 → 2016-03-01 (9 saisons, NDJ 2015 = 2.59) ; 422 sur début après la fin et sur 2015-02-30 ; 921 saisons sur toute la série |
| Chrome, période 1997-05-01 → 1998-04-01 | 12 saisons, AMJ 1997 → MAM 1998, de +0,71 à +2,37 °C ; mêmes valeurs que la comparaison |
| `pg_dump -Fc` puis `pg_restore` dans une base jetable | Fichier de 43 812 octets ; 921 observations, 1 import, NDJ 2015 = 2.59, migration `86057118b37f` ; base et fichier supprimés ensuite |
| `npm audit --omit=dev` | 0 vulnérabilité |

Aucun blocage du MVP. Étape manquante relevée dans le README : le lancement local
ne rappelait pas qu'il faut démarrer, migrer et remplir la base avant d'ouvrir
l'interface. Elle a été ajoutée.

### Dossier de conception

- `docs/dossier/dossier.html` : couverture, sommaire et les huit sections du sujet ;
  sept figures, dont cinq diagrammes en SVG (cas d'utilisation, domaine, séquence,
  architecture, déploiement), des maquettes et une capture réelle (D31).
- `docs/dossier/captures/` : deux extraits d'une capture de l'interface prise le
  16 novembre avec Chrome sans interface, sur les données réelles.
- `docs/dossier/exporter.ps1` : export PDF, comptage des pages et des passages
  à compléter. `.editorconfig` : scripts PowerShell en UTF-8 avec BOM, pour que
  Windows PowerShell 5.1 lise les accents. `.gitignore` : PDF du dossier exclu.

### Constats et corrections

- **Premier export à 16 pages** : la section 7 débordait, car le bloc des
  extraits de configuration ne peut pas être coupé. Les sous-sections ont été
  réordonnées, l'extrait Compose raccourci et un saut de page forcé supprimé :
  15 pages.
- **Lecture des pages du PDF** : l'outil de lecture de l'assistant exigeait
  poppler, absent. Les pages ont été rendues en images par le moteur PDF de
  Windows (`Windows.Data.Pdf`), avec un script temporaire hors du dépôt. Ce moteur
  a aussi compté les pages : le même nombre que le script d'export.
- **Schémas relus page par page** : étiquettes collées aux flèches, libellé du
  réseau interne coupé et note débordant sur une ligne de vie, corrigés. La boîte
  ETL du schéma de déploiement suggérait un accès à la base, contrairement à
  l'extrait Compose (ETL sans réseau) : elle a été corrigée.
- **Chemin avec espace** : la première capture a échoué (« Multiple targets »),
  car le chemin du dépôt contient une espace ; les arguments sont maintenant
  entre guillemets, y compris dans `exporter.ps1`.

### Git

Quatre commits à la date réelle de la session (détail dans [GIT.md](GIT.md)) :
1. `chore: exporter le dossier de conception en PDF`
2. `docs: ajouter le dossier de conception`
3. `docs: consigner la revérification du MVP et le dossier`
4. `docs: préciser l'usage des captures du dossier`, ajouté après coup : la
   capture de la comparaison était versionnée sans être insérée dans le dossier.

### Contributions de l'IA

**Fourni par l'étudiant** : le cahier des charges :
- la vérification du MVP sur les vraies données ;
- les huit sections et leur contenu attendu ;
- la limite de 15 pages ;
- la séparation entre ce qui est testé et ce qui est proposé ;
- le marquage des passages personnels.

**Réalisé par Claude** :
- les vérifications et la démonstration ;
- la rédaction du dossier, les diagrammes, les captures et le script d'export.

La compréhension et la validation personnelles de l'étudiant restent à confirmer.

### Limites ouvertes

- Quatre passages du dossier restent à compléter par l'étudiant : nom, arbitrages
  personnels, vérifications personnelles, retour d'expérience.
- Le déploiement est proposé, non testé : Dockerfiles, `compose.prod.yaml` et
  Caddyfile n'existent qu'à l'état d'extraits dans le dossier.
- Le sommaire est numéroté à la main : à revérifier après toute modification.

### Publication

Après accord de l'étudiant, `git push` a publié les quatre commits
(`60a1941..d7aa6b6 main -> main`). `git rev-parse HEAD` et
`git ls-remote origin refs/heads/main` renvoyaient tous deux
`d7aa6b69ebb626d0da9d2388a4d0dd10039cc693`.

## 17 novembre 2026 — Rejeu complet depuis un clone propre et version à rendre

### Périmètre

Rejouer le projet comme un correcteur à partir d'une copie propre, sans
utiliser l'espace de travail de l'étudiant ; relancer les trois tests et le
build ; finaliser et contrôler le PDF du dossier ; vérifier qu'aucun secret ni
PDF du sujet n'est exposé. Aucune fonctionnalité ajoutée.

### État de départ

`main` propre et identique à `origin/main` (`d7aa6b6`). Les quatre passages
« À compléter » du dossier n'étaient pas encore remplis.

### Rejeu depuis un clone propre

Clone de `https://github.com/Hugodrc55/ENSO-Monitor.git` dans un dossier
temporaire, hors de l'espace de travail. Le clone contient 70 fichiers suivis,
dont le fichier NOAA brut, son empreinte et sa fiche de provenance ; il ne
contient ni `.env`, ni PDF, ni `data/processed/`.

| Étape du README | Résultat observé |
| --- | --- |
| Empreinte du fichier brut | Identique à `SHA256SUMS` (`118c5633…0f7f`) |
| Python 3.13.17, Node 22.23.4, npm 10.9.9, Docker 29.9.2, Compose v5.6.1 | Conformes aux prérequis |
| `pip install` des deux environnements, `npm ci` | Codes de sortie 0 |
| `.env` copié de `.env.example`, mot de passe remplacé | Seul ajustement : `POSTGRES_PORT=5433` |
| `docker compose up -d --wait db` | Conteneur sain, écoute sur `127.0.0.1:5433` |
| `alembic upgrade head`, `current`, `check` | `86057118b37f (head)` ; aucun écart |
| Transformation | 921 observations valides ; CSV identique (`4b1f7a77…`) |
| Import, 1er puis 2e passage | 921 ajoutées, puis 0 ajoutée et 921 identiques ; 1 import en base |
| `createdb enso_monitor_test` puis `pytest etl/tests -q` | **28 passed** (1,1 s) |
| `pytest tests/test_observations_api.py -q` depuis `backend` | **10 passed** (3,1 s) |
| `pytest -q -W error -rs` depuis `backend` | **34 passed** (3,4 s), aucun test ignoré |
| `npm.cmd --prefix frontend test` | **12 passed** (4,4 s) |
| `npm run lint`, `npm run build` | Sans erreur ; JavaScript 237,93 kB (75,28 kB gzip) |
| `npm audit --omit=dev` | 0 vulnérabilité |
| API et Vite lancés depuis le clone, Chrome | Toute la série : 921 saisons ; axe « Anomalie ONI (°C) », seuils en °C, source NOAA CPC avec série et version |
| Période 2015-07-01 → 2016-03-01 | La courbe passe de 921 à 9 points, graduations mensuelles ; résumé, valeur lue et tableau (9 lignes) mis à jour |
| Comparaison | 12 saisons par épisode ; +2,37 °C (NDJ 1997) et −1,85 °C (NDJ 1988) ; texte construit à partir de ces valeurs |
| `exporter.ps1` exécuté dans le clone | PDF de 15 pages |

Écart avec le README : la base de l'étudiant tournait en même temps, sur le port
5432 et sous le même nom de projet Compose. Le clone a donc utilisé
`docker compose -p enso-verif` et le port 5433. Ce cas ne se pose pas sur une
machine sans projet existant ; le README précise maintenant comment changer de
port. Le conteneur et le volume de vérification ont été supprimés après coup.

### Sécurité du dépôt

- Aucun `.env` ni aucun PDF n'a jamais été ajouté dans l'historique (70 fichiers
  ajoutés au total ; `docs/sujet/` ne contient que son README).
- Le mot de passe du `.env` local, lu sans être affiché, n'apparaît dans aucune
  version d'aucun fichier.
- Aucun motif de clé ou de secret dans les fichiers suivis.

### Dossier

- Dates mises à jour pour les vérifications refaites le 17 novembre ; les preuves
  datées du 16 (capture, sauvegarde) gardent leur date.
- Un premier export est remonté à 16 pages : une cellule rallongée de la section 7
  repoussait le bloc de la procédure. Après raccourcissement de la cellule :
  **15 pages**, comptées par le script et par le moteur PDF de Windows.
- Les 15 pages ont été affichées : aucun tableau ni schéma coupé, chaque section
  commence à la page du sommaire.

### README

- Les données NOAA nécessaires sont versionnées : aucun téléchargement à faire.
  Renvoi vers la procédure d'une nouvelle extraction.
- Changement du port PostgreSQL si 5432 est occupé.

### Git

Trois commits à la date réelle de la session (détail dans [GIT.md](GIT.md)) :
1. `docs: dater le dossier du rejeu sur un clone propre`
2. `docs: préciser les données versionnées et le port PostgreSQL`
3. `docs: consigner le rejeu et la version à rendre`

### Contributions de l'IA

**Fourni par l'étudiant** : le cahier des charges de la session :
- le rejeu depuis une copie propre ;
- les trois tests et le build ;
- le contrôle du PDF ;
- la sécurité du dépôt ;
- l'interdiction d'ajouter une fonctionnalité.

**Réalisé par Claude** : le rejeu, les vérifications, les mises à jour du dossier,
du README et de ce journal.

La compréhension et la validation personnelles de l'étudiant restent à confirmer.

### Reste avant le rendu

Les quatre passages « À compléter » du dossier, que seul l'étudiant peut écrire :
nom, arbitrages personnels, vérifications personnelles, retour d'expérience.
Ensuite : réexporter, contrôler le nombre de pages et remettre le PDF.
