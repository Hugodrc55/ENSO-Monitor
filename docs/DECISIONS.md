# Décisions du projet

- D01 à D09 : décisions initiales du **4 novembre 2026** (Jour 1), avec l'aide de Codex.
- D10 à D14 : décisions du **9 novembre 2026** (Jour 2, données NOAA), avec l'aide de Claude.
- D15 à D18 : décisions du **12 novembre 2026** (transformation des données), avec l'aide de Claude.
- D19 à D22 : décisions du **14 novembre 2026** (base de données PostgreSQL), avec l'aide de Claude.
- D23 à D26 : décisions du **14 novembre 2026**, en fin de journée (import et API des observations), avec l'aide de Claude.

Ces décisions sont proposées ou mises en œuvre avec l'aide de l'IA, dans le
périmètre demandé. Leur compréhension et leur validation personnelles par l'étudiant
restent à confirmer. Aucune validation orale n'est supposée.

## D01 — Développement par journées validées

- **Besoin** : comprendre le code et conserver une progression authentique.
- **Options** : implémentation complète immédiate ou étapes limitées.
- **Choix** : suivre les 14 journées indicatives demandées ; arrêter après chaque journée.
- **Avantage** : modifications explicables et vérifiables.
- **Limite** : calendrier à ajuster aux difficultés réelles.
- **Vérification** : journal daté, périmètre comparé au plan, commits proposés sur le travail réel.

## D02 — ONI ERSSTv6 (choix de l'étudiant)

- **Besoin** : une série NOAA authentique pour l'import et les comparaisons.
- **Options du sujet** : ONI ou RONI ; une seule série est nécessaire.
- **Choix explicite** : ONI ERSSTv6, URL fournie par l'étudiant et le sujet.
- **Avantage** : un périmètre scientifique unique.
- **Limite** : format, signification temporelle et modalités de révision restent à étudier au Jour 2.
- **Vérification future** : source, version et date d'extraction, sans données inventées.

## D03 — Un dépôt, quatre dossiers

- **Besoin** : rendre les responsabilités visibles et conserver un historique commun.
- **Options** : dépôts séparés ou dépôt unique.
- **Choix** : `frontend/`, `backend/`, `etl/`, `docs/` dans un dépôt Git sur `main`.
- **Avantage** : revue simple d'une évolution traversant plusieurs couches.
- **Limite** : installations JavaScript et Python distinctes.
- **Vérification** : commandes autonomes dans le README, secrets et PDF exclus de Git.

## D04 — Frontend React minimal, sans bibliothèque de composants

- **Besoin** : vérifier une première communication avec TypeScript strict.
- **Options** : grande structure applicative ou un composant et une fonction HTTP dédiée.
- **Choix** : Vite, React, `App.tsx`, `api.ts`, CSS simple, ESLint.
- **Avantage** : peu de code à expliquer ; dépendances applicatives limitées à React.
- **Limite** : les composants de consultation seront introduits au Jour 8 selon le besoin.
- **Vérification** : typage strict, lint, compilation et contrôle navigateur.

## D05 — URL relative et proxy Vite local

- **Besoin** : faire communiquer le navigateur sur 5173 avec FastAPI sur 8000.
- **Options** : URL absolue et CORS dans l'API, ou transfert `/api` par Vite.
- **Choix** : `fetch('/api/v1/health')`, proxy vers `127.0.0.1:8000`.
- **Avantage** : aucune URL d'API publique ni configuration CORS supplémentaire au Jour 1.
- **Limite** : Vite assure ce rôle localement ; il faudra un routage équivalent en cible avec Caddy.
- **Vérification** : même réponse HTTP sur les ports 8000 et 5173 ; serveur `preview` configuré de même sur 4173.

## D06 — Santé HTTP et contrat Pydantic

- **Besoin** : confirmer que le backend répond avant d'ajouter les données.
- **Options** : réponse libre ou schéma explicite.
- **Choix** : `HealthResponse` avec `status: Literal["ok"]` et `service: str`, route `/api/v1/health`.
- **Avantage** : contrat validé côté serveur et exposé dans OpenAPI.
- **Limite** : ce contrôle ne teste pas PostgreSQL, NOAA ou la fraîcheur des observations.
- **Vérification** : Pytest/TestClient et appel HTTP réel ; contrôle du JSON reçu dans le frontend.

## D07 — État de connexion et délai maximal

- **Besoin** : fournir un retour compréhensible lorsque l'API répond ou échoue.
- **Options** : requête sans retour d'état ou trois états explicites.
- **Choix** : attente, succès, erreur, nouvelle tentative ; délai de cinq secondes et annulation au démontage.
- **Avantage** : pas d'attente infinie ni de réponse obsolète appliquée après un démontage.
- **Limite** : message d'échec volontairement simple au Jour 1 ; diagnostic détaillé dans les outils de développement.
- **Vérification** : arrêt de l'API, tentative, redémarrage et nouvelle tentative dans le navigateur.

## D08 — Publication GitHub préparée, déploiement différé

- **Besoin** : publier ensuite un historique réel sans exposer l'épreuve ou les secrets.
- **Options** : publication immédiate ou préparation locale avec commandes relisibles.
- **Choix** : exclusions Git, guide de création d'un dépôt GitHub vide, commits proposés ; aucun push automatique autorisé.
- **Avantage** : l'étudiant peut relire, comprendre et choisir son compte et la visibilité.
- **Limite** : aucun dépôt distant n'est créé tant que cette étape n'est pas effectuée.
- **Vérification** : `git status`, `git check-ignore`, revue de l'index avant commit ; comparaison des SHA après un futur push.

## D09 — Versions compatibles et limites de l'audit initial

- **Besoin** : installer des versions utilisables ensemble, vérifier leurs contraintes réelles.
- **Options** : toutes les dernières versions sans vérification ou versions explicites compatibles.
- **Choix** : TypeScript 6.0.3, car `typescript-eslint` 8.72.1 déclare `<6.1.0` ; ESLint 10.14.0 maintenu ; types de Node 22. Le client `httpx2` remplace `httpx`, déprécié par le TestClient de Starlette installé.
- **Avantage** : typecheck, lint et test backend exécutables sans les avertissements de dépréciation initiaux.
- **Limite constatée** : `npm audit` signale 11 alertes modérées dans la chaîne de développement, à partir de `minimatch <11.0.1` ([avis](https://github.com/advisories/GHSA-g3hv-75wg-m249)). Le rapport propose notamment des changements majeurs ou des retours à de très anciennes versions ; aucune correction forcée n'a été appliquée. Suivre une mise à jour compatible de l'outillage.
- **Vérification** : lint et build réussis ; `pip check` sans incompatibilité ; `npm audit --omit=dev` signale zéro vulnérabilité. Cela ne remplace pas un audit de sécurité complet.

## D10 — Fichier source `oni.ascii.txt`, série ERSSTv6

- **Besoin** : obtenir la série choisie en D02 sous une forme lisible par un script, avec une provenance prouvée.
- **Options** : recopier le tableau HTML de la page v6 (une décimale) ; fichier texte `oni.ascii.txt` (deux décimales) ; fichier mensuel `detrend.nino34.ascii.txt`, puis recalcul des moyennes.
- **Choix** : `oni.ascii.txt`, la série saisonnière publiée par la NOAA, utilisée telle quelle.
- **Avantage** : colonnes stables, deux décimales, aucun recalcul de notre part. Le lien officiel figure sous l'intitulé « Seasonal ERSSTv6 (centered base periods) "Oceanic Niño Index" ».
- **Limite** : le fichier ne documente ni ses colonnes ni son unité, et son nom n'indique pas la version. La même URL peut donc servir une autre version plus tard.
- **Vérification** : intitulé de la page d'index NOAA. Les 921 valeurs sont à 0,05 au plus du tableau v6, contre 495 écarts supérieurs à 0,05 avec le v5. Le recalcul depuis le fichier mensuel retrouve 919 valeurs sur 921 à 0,01 près. Détails : [DONNEES_NOAA.md](DONNEES_NOAA.md).

## D11 — Copie brute versionnée dans `data/raw/`

- **Besoin** : prouver quelles données ont été utilisées, alors que la NOAA révise ses valeurs.
- **Options** : télécharger à chaque exécution sans conserver ; conserver hors de Git ; versionner une copie datée.
- **Choix** : versionner `data/raw/noaa-cpc_oni-ersstv6_2026-11-09.txt` (23 Ko) avec `SHA256SUMS` et un README de provenance. `.gitignore` n'exclut plus `data/raw/`, mais les autres sous-dossiers de `data/` restent exclus. `.gitattributes` empêche la conversion des fins de ligne de ces fichiers.
- **Avantage** : résultats reproductibles pour le jury, même hors ligne ; l'empreinte détecte toute modification.
- **Limite** : la copie vieillit, et chaque nouvelle extraction ajoute un fichier. Raisonnable pour 23 Ko, pas pour de gros jeux de données. Les conditions de réutilisation n'ont pas été vérifiées aujourd'hui ; la source NOAA est citée.
- **Vérification** : `sha256sum -c SHA256SUMS`, `git check-attr`, empreinte du fichier relu depuis le commit.

## D12 — Dater chaque saison par son mois central

- **Besoin** : placer chaque saison sur un axe du temps et la filtrer par période, sans perdre la notation NOAA.
- **Options** : premier mois, dernier mois ou mois central de la saison ; texte seul (`DJF 1950`).
- **Choix** : `reference_month` = premier jour du mois central. `SEAS` et `YR` sont conservés ; le début et la fin de période sont dérivés pour l'affichage.
- **Avantage** : convention adaptée à une moyenne glissante centrée. Comme `YR` est l'année du mois central, la conversion ne demande aucune exception pour DJF et NDJ.
- **Limite** : une date au 1er du mois est une convention, alors que la valeur couvre trois mois. L'interface devra l'indiquer.
- **Vérification** : l'hypothèse « année du mois central » est confirmée sur 919 saisons sur 921 avec le fichier mensuel. L'hypothèse « année du premier mois » est rejetée (écarts jusqu'à 3,72 °C). Mise en œuvre le 12 novembre dans `add_dates` (`etl/transform_oni.py`) ; tests de DJF et NDJ au changement d'année, y compris l'année bissextile 2000.

## D13 — Conserver l'ONI alors que la RONI est officielle

- **Besoin** : rester cohérent avec le choix de l'étudiant (D02) en tenant compte du changement annoncé par la NOAA.
- **Options** : conserver l'ONI ; passer à la RONI ; utiliser les deux (inutile : le sujet demande une seule série).
- **Choix proposé** : conserver l'ONI ERSSTv6, autorisé par le sujet et toujours mis à jour par la NOAA. L'étudiant doit **reconfirmer** ce choix en connaissant ce changement ; sa confirmation n'est pas supposée.
- **Avantage** : série historique longue et plan inchangé.
- **Limite** : l'ONI n'est plus l'indice officiel de surveillance depuis le 1er février 2026, et certaines saisons sont classées différemment (DJF 2026 : ONI −0,4 ; RONI −0,9). L'interface et le dossier devront le dire.
- **Vérification** : communiqué NWS 26-05 et pages ONI v6 et RONI consultés le 9 novembre ; nom de série affiché sans ambiguïté.

## D14 — Aucune nouvelle dépendance au Jour 2

- **Besoin** : contrôler le fichier sans anticiper l'ETL.
- **Options** : installer Pandas dès aujourd'hui, ou utiliser des scripts temporaires avec la bibliothèque standard Python.
- **Choix** : scripts temporaires hors du dépôt (`hashlib`, `re`, `decimal`). Pandas et NumPy seront introduits et justifiés au Jour 3.
- **Avantage** : aucun code non expliqué ni non testé dans le dépôt ; périmètre du Jour 2 respecté.
- **Limite** : ces contrôles ne sont pas rejouables depuis le dépôt. Ils le deviendront au Jour 3, sous forme de code et de tests.
- **Vérification** : aucune dépendance ni aucun fichier de code applicatif modifiés (`git status`).

## D15 — ETL séparé, avec son environnement et ses dépendances

- **Besoin** : transformer les données NOAA sans mêler ce traitement à l'API.
- **Options** : code dans `backend/` ; script isolé sans dépendances déclarées ; paquet `etl/` avec ses propres dépendances.
- **Choix** : paquet Python `etl/`, lancé par `python -m etl.transform_oni` depuis la racine. Environnement `etl/.venv`. `etl/requirements.txt` fixe pandas 3.1.1 et NumPy 2.5.4 ; `requirements-dev.txt` ajoute pytest 9.2.0, la version utilisée par l'API. Tests dans `etl/tests/`.
- **Justification des dépendances** :
  - pandas lit le fichier à colonnes et traite des colonnes entières : conversion, doublons, tri et dates ;
  - NumPy fournit `isfinite`, qui écarte les valeurs absentes ou infinies, et `diff`, qui repère les trous de la série ;
  - pytest exécute les tests, comme pour l'API.
- **Avantage** : séparation frontend / API / ETL demandée par le sujet. L'API n'installe pas pandas.
- **Limite** : deux environnements Python à installer. Le chargement en base partagera le modèle de données avec l'API : cette organisation sera réexaminée à ce moment-là.
- **Vérification** : un environnement neuf, installé uniquement depuis `etl/requirements-dev.txt`, passe les 28 tests. `pip check` ne signale aucun conflit.

## D16 — Lecture en texte, en-tête contrôlé, numéro de ligne conservé

- **Besoin** : repérer chaque valeur non numérique et pouvoir retrouver toute observation dans le fichier NOAA.
- **Options** : `read_csv` avec en-tête et types détectés automatiquement ; lecture en texte, puis conversion contrôlée.
- **Choix** : `read_csv(sep=r"\s+", header=None, dtype=str, keep_default_na=False, skip_blank_lines=False)`, puis vérification de l'en-tête exact. Le numéro de ligne `source_line` est conservé jusqu'au CSV.
- **Avantage** : un essai sur des fichiers fictifs a montré qu'avec l'en-tête automatique, une ligne comportant un champ de trop décale toutes les colonnes sans erreur. Avec `index_col=False`, elle est tronquée avec un simple avertissement. Ici, la lecture s'arrête et indique la ligne fautive. Chaque observation du CSV renvoie à sa ligne d'origine.
- **Limite** : une seule ligne mal formée bloque tout le fichier. C'est voulu : il s'agit d'un problème de format, pas de valeur.
- **Vérification** : tests avec une page HTML, une ligne à cinq champs, et les valeurs `abc`, `1,5`, `NaN`, `inf` ou absentes.

## D17 — Doublons : copies ignorées, contradictions rejetées

- **Besoin** : le sujet demande de contrôler les doublons. Chaque saison doit figurer une seule fois, sans choix arbitraire de valeur scientifique.
- **Options** : refuser tout le fichier au premier doublon (approche envisagée le 9 novembre) ; garder la première ou la dernière version ; distinguer copies et contradictions.
- **Choix** :
  - copie strictement identique (mêmes `SEAS`, `YR`, `TOTAL` et `ANOM`) : la première ligne du fichier est gardée, les suivantes sont signalées ;
  - versions différentes d'une même saison : toutes sont rejetées, avec leur motif.
- **Avantage** : le traitement des copies est déterministe, et aucune valeur contradictoire n'est retenue au hasard.
- **Limite** : une saison contradictoire disparaît du CSV. Le trou est signalé et la commande se termine avec le code 1.
- **Vérification** : tests du doublon identique et du doublon contradictoire, et contrôle que chaque ligne lue est comptée une seule fois.

## D18 — Bornes physiques larges et code de sortie

- **Besoin** : ne pas importer une valeur impossible, sans prétendre juger les extrêmes climatiques.
- **Options** : aucune borne ; bornes proches des valeurs observées ; bornes physiques larges.
- **Choix** : `TOTAL` entre −2 et 40 °C, `ANOM` entre −10 et +10 °C. Une ligne hors bornes est rejetée, jamais corrigée. La commande renvoie le code 1 dès qu'une ligne est rejetée, tout en écrivant les observations valides.
- **Avantage** : un code de remplissage (−99,90 par exemple) ou une erreur d'unité est arrêté, alors que `NDJ 2015` (+2,59 °C), maximum de la série, reste valide. Le code 1 empêche un traitement automatique suivant, comme l'import, de continuer sans examen.
- **Limite** : les bornes résultent d'un raisonnement physique (l'eau de mer gèle vers −2 °C), pas d'une source NOAA. Aucune des pages NOAA consultées ne définit de code de valeur manquante pour ce fichier.
- **Vérification** : un test rejette `-99.90`. Si les bornes sont élargies volontairement à ±100, ce test échoue.

## D19 — PostgreSQL local dans Docker Compose

- **Besoin** : une base PostgreSQL de développement et de test, simple à démarrer et à effacer.
- **Options** : installer PostgreSQL sous Windows ; service PostgreSQL seul dans Docker Compose ; base hébergée.
- **Choix** : service `db` dans `compose.yaml`, avec l'image officielle `postgres:18.7-alpine` (version exacte fixée). Le service n'écoute que sur `127.0.0.1`. Un volume nommé conserve les données et un contrôle de santé `pg_isready` est configuré. Les identifiants viennent de `.env`, et le mot de passe est obligatoire.
- **Avantage** :
  - Docker Desktop était déjà installé sur la machine ;
  - aucune installation système, version identique pour toute personne qui clone le dépôt ;
  - point de départ du Compose de déploiement à documenter.
- **Limite** : Docker Desktop doit être lancé. L'image fait 400 Mo environ ; son premier téléchargement a pris plusieurs minutes.
- **Vérification** :
  - `docker compose config` et `docker compose up -d --wait db` : service à l'état *healthy*, PostgreSQL 18.7 ;
  - après un arrêt et un redémarrage, la révision Alembic est toujours présente : le volume conserve les données.

## D20 — Modèles et migrations dans `backend/`, une seule `DATABASE_URL`

- **Besoin** : définir le schéma une seule fois, pour l'API et pour le futur import.
- **Options** : modèles dans `etl/` ; dans `backend/` ; paquet partagé séparé.
- **Choix** : `backend/app/models.py` et `backend/alembic/`. L'API sera le principal lecteur de la base, et le backend contient déjà Pydantic et pytest.
  - `app/database.py` lit `DATABASE_URL`, depuis l'environnement ou le `.env` de la racine. `alembic/env.py` utilise la même fonction.
  - Le pilote est psycopg 3 : URL `postgresql+psycopg://…`.
- **Justification des dépendances** :
  - SQLAlchemy 2.1.8 : modèles et requêtes ;
  - Alembic 1.20.1 : migrations versionnées ;
  - psycopg 3.3.9 avec l'extra `binary` : pilote PostgreSQL, fourni avec sa bibliothèque cliente sous Windows ;
  - python-dotenv 1.2.4 : lecture de `.env`, avec reprise des variables `${POSTGRES_…}` pour ne pas écrire le mot de passe deux fois.
- **Avantage** : un seul endroit pour le schéma et une seule variable de connexion. L'API n'importe pas encore la base et démarre sans elle.
- **Limite** : le futur import devra utiliser ces modèles alors que la transformation est dans `etl/`. Son emplacement reste à décider (voir D15).
- **Vérification** :
  - `alembic check` ne détecte aucune différence entre les modèles et la migration ;
  - base arrêtée, `GET /api/v1/health` renvoie toujours HTTP 200 ;
  - un environnement neuf installé depuis `backend/requirements-dev.txt` passe les 16 tests.

## D21 — Chaîne de provenance Source → Indice → Import → Observation

- **Besoin** : retrouver pour chaque observation sa source, son indice et l'import d'origine (sujet, page 5). Ne pas attribuer de version à un fichier non confirmé, et distinguer la date d'extraction de la date de chargement.
- **Options** : une table d'observations avec des colonnes de provenance répétées ; quatre tables reliées.
- **Choix** : `source` → `climate_index` → `data_import` → `observation`.
  - La version confirmée de la série est dans `climate_index.version`.
  - Chaque import enregistre `file_name`, `source_url`, `sha256` (unique), `downloaded_at` (date d'extraction), `source_last_modified`, `version_evidence` (obligatoire) et `imported_at` (date du chargement, fixée par PostgreSQL).
  - Chaque observation garde `source_line`.
- **Avantage** : la provenance est enregistrée une fois par fichier, pas 921 fois. Les quatre entités correspondent à celles demandées pour l'UML.
- **Limite** : `source` et `climate_index` sont encore vides ; l'import devra les créer. La provenance n'existe aujourd'hui qu'en Markdown (`data/raw/README.md`).
- **Vérification** : tests sur la base jetable. Un même SHA-256 est refusé, et la date de chargement est fixée par la base et postérieure à l'extraction. Un import fictif daté dans le futur a été refusé par `ck_data_import_imported_after_download`.

## D22 — Intégrité : unicité sans l'import, clé composite, types exacts, contrôles

- **Besoin** : qu'aucun programme ne puisse enregistrer deux fois une saison, une date incohérente ou une valeur impossible.
- **Options** : contrôles dans le code Python seulement ; contraintes dans PostgreSQL.
- **Choix** :
  - **Unicité** : `UNIQUE (climate_index_id, year, season)`, sans `data_import_id`.
  - **Cohérence indice / import** : clé étrangère composite `(data_import_id, climate_index_id)` → `data_import (id, climate_index_id)`.
  - **Types** : `DATE` pour `reference_month`, `SMALLINT` pour `year`, `NUMERIC(4, 2)` pour `total_c` et `anom_c`.
  - **Contrôles `CHECK`** : la saison, l'année (≥ 1950), la date de référence (mois central), les bornes physiques de D18 et `source_line > 1`.
  - **Index** : `(climate_index_id, reference_month)` pour le filtre par période.
- **Avantage** : un doublon est refusé même s'il vient d'un autre import, ou d'un autre programme que l'ETL. Les deux décimales publiées sont conservées exactement.
- **Limite** :
  - `NUMERIC(4, 2)` arrondirait sans erreur une troisième décimale : l'import devra la refuser ;
  - l'index apporte peu sur 921 lignes ;
  - les conventions de nommage allongent les noms des contraintes.
- **Vérification** :
  - **SQL relu** avec `alembic upgrade head --sql` ;
  - **doublon refusé** entre deux imports, par une insertion SQL de lignes fictives : `duplicate key value violates unique constraint "uq_observation_climate_index_id_year_season"` ;
  - **15 tests de schéma réussis** ;
  - **les tests détectent les erreurs** : si `data_import_id` est ajouté à l'unicité ou si le contrôle de date est supprimé, deux tests échouent dans chaque cas.

## D23 — Fiche de provenance JSON à côté du fichier brut

- **Besoin** : donner à l'import l'URL, la date d'extraction, la version vérifiée et l'empreinte du fichier, sans les retaper à chaque fois.
- **Options** : lire le tableau Markdown de `data/raw/README.md` ; passer les valeurs en arguments de la commande ; fiche JSON versionnée à côté du fichier brut.
- **Choix** : `data/raw/<fichier>.provenance.json`, validée par un modèle Pydantic qui refuse tout champ inconnu et exige des dates avec fuseau horaire. Date d'extraction retenue : l'en-tête `Date` du serveur NOAA (13:42:35 UTC), plutôt que l'horloge locale (13:42:23 UTC).
- **Avantage** : la provenance est versionnée avec le fichier, relue par un programme et contrôlée : l'empreinte du fichier brut doit correspondre.
- **Limite** : la fiche est écrite à la main à partir du README. Une erreur de recopie n'est détectée que pour l'empreinte et le format.
- **Vérification** : tests d'une empreinte fausse et d'une date sans fuseau, tous deux refusés. En base, NDJ 2015 renvoie au fichier, à la ligne 793, à la date d'extraction, à la série `ONI_ERSSTv6` et à la source `NOAA_CPC`.

## D24 — Import dans le backend, sans doublon ni écrasement silencieux

- **Besoin** : charger le CSV transformé avec les modèles existants. Un second import du même fichier ne doit rien ajouter, et une valeur différente ne doit jamais être écrasée sans le dire.
- **Options** :
  - emplacement : import dans `etl/` (avec SQLAlchemy et accès aux modèles du backend) ou dans `backend/` (lecture du CSV avec la bibliothèque standard) ;
  - en cas de valeur différente : écraser, ignorer la ligne, ou refuser tout l'import.
- **Choix** : `backend/app/import_oni.py`.
  - Une saison déjà présente avec les mêmes valeurs n'est pas réinsérée.
  - Une valeur différente est un conflit : il est affiché avec les deux valeurs et l'import entier est refusé (code 1). Tous les contrôles ont lieu avant la première écriture.
  - Un même fichier (même SHA-256) réutilise l'import existant.
  - Une valeur de plus de deux décimales est refusée.
- **Avantage** : réutilise les modèles et la base de test, sans ajouter pandas à l'API. Pas de mélange de deux versions NOAA dans la base, et l'import peut être relancé sans risque.
- **Limite** :
  - un fichier NOAA révisé sera refusé tant qu'aucune règle d'acceptation des révisions n'existe ;
  - l'import fait confiance au CSV : il vérifie le fichier brut que le CSV désigne, mais pas que le CSV en dérive.
- **Vérification** :
  - 1er import réel : 921 ajoutées ;
  - 2e import : 0 ajoutée, 921 identiques, toujours 921 en base et 1 seul import ;
  - copie modifiée (NDJ 2015 : 2.59 → 2.60) : conflit affiché, rien d'écrit ;
  - 8 tests d'import ; si un conflit est ignoré volontairement, le test de conflit échoue.

## D25 — Contrat de `GET /api/v1/observations`

- **Besoin** : servir les observations d'une période pour la future courbe, avec des erreurs claires.
- **Options** : paramètres facultatifs ou obligatoires ; bornes incluses ou exclues ; liste seule ou réponse avec la série.
- **Choix** :
  - **Paramètres** `start` et `end` : obligatoires, au format ISO, comparés à `reference_month` et **inclus**, avec descriptions OpenAPI.
  - **Réponse** : la série (code, version, unité, source) et les observations triées (`reference_month`, `season`, `year`, `oni`), avec `oni` en nombre JSON.
  - **Codes d'erreur** : 422 pour une date invalide ou manquante et pour un début après la fin ; 404 si la série n'est pas importée ; 503 si la base est injoignable, après un délai de connexion de 5 s.
- **Avantage** :
  - contrat explicite pour React ;
  - unité et source disponibles pour l'affichage demandé par le sujet ;
  - la route de santé reste indépendante de la base.
- **Limite** :
  - une seule série servie (`ONI_ERSSTv6`) ;
  - pas de pagination, inutile pour 921 lignes au plus ;
  - une date de début en milieu de mois exclut la saison dont la date de référence est le 1er de ce mois.
- **Vérification** :
  - 10 tests de la route ;
  - requêtes réelles : 200 sur une période, une borne unique et une période vide ; 422 pour une date invalide, un début après la fin et un paramètre manquant ;
  - base arrêtée : 503 en 5 s, alors que la même requête restait sans réponse plus de 60 s avant l'ajout du délai de connexion.

## D26 — Tests sur une base partagée, une transaction par test

- **Besoin** : tester le schéma, l'import et la route sur un vrai PostgreSQL, sans que les tests dépendent les uns des autres.
- **Options** : base recréée à chaque test ; SQLite en mémoire ; base PostgreSQL jetable créée une fois par la migration, avec annulation après chaque test.
- **Choix** : `backend/tests/conftest.py`. Le schéma est créé par la migration en début de série, puis chaque test travaille dans une transaction annulée à la fin (`join_transaction_mode="create_savepoint"`). Les tests de la route remplacent la session de l'API par celle du test.
- **Avantage** : même moteur qu'en production (contraintes `CHECK`, `NUMERIC`, `make_date`) et tests rapides : 34 en 3,5 s.
- **Limite** : Docker et la base `enso_monitor_test` sont nécessaires. Les données des tests sont fictives ; les valeurs NOAA réelles ne sont vérifiées que par la démonstration.
- **Vérification** : les 16 tests existants passent après le regroupement des fixtures, et la série complète passe sans avertissement (`-W error`).

## D27 — Courbe dessinée en SVG, sans bibliothèque de graphiques

- **Besoin** : une courbe de 921 saisons au plus. Elle doit avoir des dates à l'horizontale, des °C à la verticale et les seuils ±0,5 °C. Elle doit rester lisible sur mobile, consultable au clavier et testable sans navigateur.
- **Options** : Recharts (composants React en SVG) ; Chart.js (dessin en canvas, invisible pour les lecteurs d'écran et pour les tests DOM) ; D3 (échelles et axes) ; SVG écrit dans un composant React.
- **Choix** : `frontend/src/components/OniChart.tsx`.
  - Échelles linéaires : rang du mois central à l'horizontale, °C à la verticale, toujours au moins de −1 à +1 °C pour garder 0 et les seuils visibles.
  - Graduations adaptées à la largeur réelle, mesurée avec `ResizeObserver`.
  - Surfaces au-dessus et au-dessous de 0, avec un point de passage interpolé quand la courbe change de signe.
  - La saison sélectionnée suit le modèle ARIA du curseur (`role="slider"`, `aria-valuetext`) : flèches, Pg↑ et Pg↓ (un an), Début et Fin. À la souris ou au doigt, la saison la plus proche est retenue.
  - Un tableau des valeurs (`<details>`) donne la même information sans graphique.
- **Avantage** : aucune dépendance de production ajoutée ; chaque calcul peut être expliqué ; le SVG fait partie du DOM, donc les tests le lisent.
- **Limite** : pas de zoom ni de déplacement dans la courbe ; plus de code à maintenir qu'avec une bibliothèque ; graduations simples, avec un pas choisi parmi 1, 3, 6, 12, 24, 60, 120 ou 240 mois.
- **Vérification** :
  - test Vitest du curseur au clavier ;
  - dans Chrome sur les données réelles, Début puis 5 fois → mènent à NDJ 2015 (+2,59 °C) ;
  - à 390 px de large, aucun défilement horizontal.

## D28 — Chargement par période et états de l'interface

- **Besoin** : recharger les observations à chaque période, ne jamais afficher la réponse d'une ancienne période, et rendre visibles le chargement, la période vide, les dates inversées et les erreurs.
- **Options** :
  - requête à chaque modification d'un champ, ou à la validation du formulaire ;
  - contrôle des dates dans le navigateur, dans l'API, ou les deux ;
  - bibliothèque de requêtes (TanStack Query) ou hook écrit pour le projet.
- **Choix** :
  - formulaire validé par « Afficher » ; une date vide ou une période inversée est refusée avant toute requête, avec un message en français (`role="alert"`). L'API garde sa propre validation (422) ;
  - hook `useObservations` : une clé par requête (période et numéro de tentative). La requête précédente est annulée au changement de période ou au démontage. Délai de 10 s, plus long que les 5 s après lesquelles l'API répond 503 ;
  - le JSON reçu est contrôlé dans `api.ts` avant usage ;
  - la carte « État du service » est retirée de la page. Le message d'erreur distingue déjà une API injoignable (502 du proxy, ou aucune réponse) d'une base indisponible (503). La route `/api/v1/health` reste dans l'API.
- **Avantage** : aucune dépendance ajoutée ; même principe que le premier appel de santé (annulation, délai, réponse ignorée après démontage). L'état « chargement » est déduit de la clé, sans écriture d'état dans l'effet, comme le demande la règle `react-hooks/set-state-in-effect`.
- **Limite** : pas de cache, donc revenir à une période déjà affichée relance la requête ; la période n'est pas dans l'URL et ne peut pas être partagée par un lien.
- **Vérification** :
  - tests : dates inversées sans requête, période vide, erreur réseau puis « Réessayer » ;
  - dans Chrome : 502 avec l'API arrêtée, 503 avec la base arrêtée, puis retour des valeurs après redémarrage.

## D29 — Épisodes comparés : El Niño 1997-1998 et La Niña 1988-1989

- **Besoin** : comparer un épisode chaud et un épisode froid réellement couverts par la série, avec des valeurs calculées depuis l'API, et interpréter prudemment le résultat.
- **Repérage** : le 15 novembre, un script temporaire, hors du dépôt, a appliqué la règle NOAA (au moins 5 saisons consécutives au-delà de ±0,5 °C) aux 921 observations de l'API. Suites relevées, entre autres :
  - El Niño : AMJ 1997 → MAM 1998, 12 saisons, pic NDJ 1997 (+2,37 °C) ; SON 2014 → AMJ 2016, 20 saisons, pic NDJ 2015 (+2,59 °C) ;
  - La Niña : AMJ 1988 → AMJ 1989, 13 saisons, pic NDJ 1988 (−1,85 °C) ; AMJ 1973 → MJJ 1974, 14 saisons, pic NDJ 1973 (−2,04 °C).
- **Options** : les deux extrêmes de la série (2015-2016 et 1973-1974) ; deux épisodes marqués et proches dans le temps. Pour les bornes : celles des suites détectées, ou des fenêtres de même durée.
- **Choix** : deux fenêtres de 12 saisons, de mai à avril (mois centraux), AMJ 1997 → MAM 1998 et AMJ 1988 → MAM 1989. Les deux pics tombent en fin d'année, au milieu de la fenêtre. Ces fenêtres sont un choix du projet, pas des dates officielles de début et de fin, et l'interface le dit.
- **Écartés** : 2015-2016 dure 20 saisons et ne tient pas dans une fenêtre de même durée ; 1973-1974 est à 24 ans de 1997, et ses références seraient encore plus éloignées.
- **Avantage** : même durée pour les deux épisodes ; chaque fenêtre reste entière au-delà du seuil ; neuf ans seulement d'écart.
- **Limite** :
  - les périodes de référence de 30 ans changent tous les 5 ans : à neuf ans d'écart, les deux anomalies n'ont pas la même référence ;
  - les saisons se chevauchent et ne sont pas indépendantes ;
  - un seul indice, une seule région ; deux épisodes ne permettent aucune généralisation.

  Ces limites sont écrites dans l'interface. Les phrases d'observation sont construites à partir des valeurs calculées, sans chiffre écrit en dur.
- **Vérification** :
  - dans Chrome, 12 saisons par fenêtre ;
  - El Niño : de +0,71 °C (AMJ 1997) à +2,37 °C (NDJ 1997) ;
  - La Niña : de −1,85 °C (NDJ 1988) à −0,85 °C (MAM 1989) ;
  - 12 saisons d'affilée au-delà du seuil pour chacun ;
  - un test Vitest vérifie que les valeurs affichées sont bien calculées à partir de la réponse de l'API.

## D30 — Test frontend avec Vitest, jsdom et Testing Library

- **Besoin** : le test exigé par le sujet, « un changement de période actualise la courbe ou les valeurs affichées », vérifié sur l'affichage et pas seulement sur l'envoi d'une requête.
- **Options** : Playwright (vrai navigateur, contre l'API et la base) ; Vitest avec un DOM simulé et une API simulée.
- **Choix** : outils de développement à versions fixées :

  | Outil | Version | Rôle |
  | --- | --- | --- |
  | Vitest | 5.1.0 | Lanceur de tests, réutilise la configuration Vite |
  | jsdom | 31.0.1 | DOM simulé, sans navigateur |
  | @testing-library/react | 16.3.3 | Rendu des composants |
  | @testing-library/dom | 10.4.2 | Recherche par rôle et par libellé, comme un utilisateur |
  | @testing-library/user-event | 14.6.10 | Saisie, clics et clavier |

  `fetch` est remplacé par une fausse API qui filtre 15 valeurs **fictives** selon `start` et `end`, bornes incluses, comme l'API réelle. jsdom impose Node 22.22.2 au minimum (champ `engines`).
- **Avantage** : 12 tests en 3 à 4 s, sans Docker ni base. Le test principal vérifie, après le changement de période :
  - le résumé : nombre de saisons, première et dernière, extrêmes ;
  - la valeur lue sur la courbe, y compris au clavier ;
  - les lignes du tableau.
- **Limite** :
  - ne prouve pas l'intégration avec l'API réelle, vérifiée par la démonstration manuelle ;
  - jsdom ne calcule pas la mise en page, donc le responsive est vérifié à part ;
  - `npm audit` signale 9 alertes modérées dans la chaîne ESLint (`minimatch`), sans lien avec ces outils, non traitées.
- **Vérification** :
  - `npm.cmd --prefix frontend test` : 12 passed ;
  - erreur volontaire (le formulaire ne transmet plus la période) : le test principal échoue ; fichier restauré à l'identique.
