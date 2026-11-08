# Décisions initiales — 4 novembre 2026

Ces décisions sont proposées ou mises en œuvre avec l'aide de Codex, dans le
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
