# Analyse du sujet officiel

Source : `sujet/HETIC_WEB3_Projet_ENSO_Monitor.pdf`, huit pages, lecture intégrale
le **4 novembre 2026**, complétée par une vérification du rendu des huit pages.
Le PDF est une référence de l'épreuve ; les consignes de session de l'étudiant
déterminent la progression autorisée. Le PDF n'est pas publié avec le dépôt.

## Synthèse et traçabilité

| Pages | Exigence du sujet | Prise en compte prévue |
| --- | --- | --- |
| 1, 7 | Travail individuel, code review prépondérante, compréhension et justification personnelles | Explications à chaque étape, journal des apports de l'IA, exercices et préparation orale |
| 2 | Import d'une série NOAA authentique ONI **ou** RONI dans PostgreSQL, source et contrôle des doublons | ONI ERSSTv6 choisi par l'étudiant ; J2 à J5 |
| 2–3 | Source, version, date d'extraction, période et unités explicites ; pas de confusion ONI/RONI | Documentation J2, provenance J5, affichage J9 |
| 2–3 | FastAPI, Pydantic, OpenAPI, routes `/api/v1`, filtrage temporel et validation | Route technique santé J1 ; observations J6–J7 |
| 2–3 | React/TypeScript strict/Vite, courbe interactive et sélection de période | Initialisation J1, interface J8, courbe J9 |
| 2–3 | Comparaison de deux épisodes, explication écrite et prudence dans l'interprétation | J10 ; ne jamais inventer les mesures |
| 3 | PostgreSQL, SQLAlchemy, Alembic ; contraintes et migrations | J4–J5 |
| 3 | ETL Python, Pandas et NumPy ; fiabilité et traçabilité | J3–J5 |
| 3 | Responsive, clavier, contrastes, légendes, erreurs, séparation des responsabilités, linting et README | Base simple J1, vérification approfondie J11–J12 |
| 3 | Requêtes paramétrées, secrets hors Git ; contrôle d'accès si administration | Exclusions J1, accès aux données J4–J7 ; aucune administration prévue |
| 3, 8 | Trois tests minimaux exécutés et documentés | Données J5, API J7, frontend J12 ; détails ci-dessous |
| 4–5, 8 | Dossier indépendant, paginé, sommaire, 15 pages maximum **couverture comprise** | Consolidation après J14, à partir du suivi réel |
| 5 | UML : cas d'utilisation ; classes ou domaine avec Observation, Indice, Source, Import et cardinalités ; séquence d'une consultation avec erreurs | Conception progressive puis diagrammes commentés ; aucun modèle implémenté au J1 |
| 5 | Architecture React/API/PostgreSQL/ETL, schéma relationnel, déploiement cible | Documentation consolidée ; besoin, options, choix, avantages, limites et vérification pour chaque décision |
| 6 | Déploiement documenté : VPS Linux, Compose, Caddy, HTTPS, réseaux, secrets, sauvegardes/restauration, logs, supervision, retour arrière, capacité et limites | J13 puis dossier ; mise en ligne facultative et aucun achat exigé |
| 7–8 | Déclaration des apports de l'IA, bugs reproductibles, corrections vérifiées, historique Git authentique | README, journal et commits proposés à chaque session |

## Trois tests finaux imposés (page 3)

1. **Données** : une transformation sur des observations NOAA réelles, par exemple
   le contrôle des doublons ou d'une date invalide.
2. **API** : une route filtrée par période, réponse attendue et prise en charge
   d'une entrée invalide.
3. **Frontend** : un changement de période actualise la courbe ou les valeurs.

Le test `/api/v1/health` du Jour 1 est un contrôle initial supplémentaire.
Il ne constitue aucun des trois tests finaux à lui seul.

## Dossier de conception : huit sections obligatoires (page 4)

1. Besoin et contexte : public, contraintes, périmètre et limites.
2. Fonctionnel et UX : user stories, priorisation, parcours, wireframes, critères d'acceptation.
3. UML et modélisation : trois diagrammes attendus, expliqués.
4. Architecture : composants, flux, décisions et schéma SQL.
5. Organisation : backlog personnel, planning **sur cinq jours**, outils, risques et arbitrages.
6. Qualité et sécurité : tests, UX, performance et traitement des anomalies.
7. Déploiement proposé : VPS, Docker Compose, Caddy, exploitation et limites.
8. Bilan et sources : IA, difficultés, corrections et références scientifiques.

Les volumes par section sont indicatifs ; leur addition ne doit pas faire dépasser
15 pages au total. Les documents de suivi actuels ne sont pas le dossier final.

## Limites explicites du MVP (pages 2–3, 6)

Une seule série suffit. ERA5, administration, automatisation, exports,
cartographie et statistiques avancées sont facultatifs. Aucune prévision n'est
demandée. « Super El Niño » n'est pas une classe universelle : tout classement
devrait définir indice, seuils et durée. Ces extensions ne sont pas prévues au Jour 1.

Deux livrables sont distincts : l'application avec son code et le dossier de conception.
Une mise en ligne publique n'est pas une condition de réussite.
