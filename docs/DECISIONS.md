# Décisions du projet

- D01 à D09 : décisions initiales du **4 novembre 2026** (Jour 1), avec l'aide de Codex.
- D10 à D14 : décisions du **9 novembre 2026** (Jour 2, données NOAA), avec l'aide de Claude.

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
- **Vérification** : l'hypothèse « année du mois central » est confirmée sur 919 saisons sur 921 avec le fichier mensuel. L'hypothèse « année du premier mois » est rejetée (écarts jusqu'à 3,72 °C). Implémentation et tests prévus au Jour 3.

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
