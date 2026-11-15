# Plan de préparation

Début réel : **4 novembre 2026**. Préparation prévue sur environ un mois, dont
14 journées de développement. Il s'agit d'une prévision, pas d'un historique.
Les journées ne sont pas nécessairement consécutives. Tout changement de durée
sera expliqué dans le journal, et chaque nouvelle étape attendra l'accord de l'étudiant.

| Jour | Objectif et critère de sortie prévu | Statut |
| --- | --- | --- |
| 1 | Dépôt Git, documentation, React strict, santé FastAPI, connexion vérifiée | Réalisé avec assistance IA ; validation personnelle attendue |
| 2 | Étudier NOAA ONI ERSSTv6 : format, unité, périodes, source, version et limites | Réalisé le 9 novembre avec assistance IA ; validation personnelle attendue |
| 3 | Transformer la série avec Python, Pandas et NumPy (contrôles, doublons, dates du mois central) ; premier test de données | Réalisé le 12 novembre avec assistance IA : transformation et 28 tests Pytest |
| 4 | Modéliser PostgreSQL, contraintes SQL, SQLAlchemy et migrations Alembic | Réalisé le 14 novembre avec assistance IA : PostgreSQL local, quatre tables, première migration et 15 tests du schéma |
| 5 | Import authentique en base, provenance (source, import, date d'extraction), test d'import | Réalisé le 14 novembre avec assistance IA : 921 observations importées, second import sans ajout, 8 tests |
| 6 | Exposer les observations avec FastAPI et documenter le contrat OpenAPI | Réalisé le 14 novembre avec assistance IA, regroupé avec la ligne 7 : `GET /api/v1/observations` |
| 7 | Filtres temporels, validations et test API sur période + entrée invalide | Réalisé le 14 novembre avec assistance IA : bornes incluses, erreurs 422/404/503, 10 tests |
| 8 | Construire l'interface de consultation et brancher les observations | Réalisé le 15 novembre avec assistance IA : page branchée sur `GET /api/v1/observations` |
| 9 | Ajouter courbe interactive, période sélectionnable, unité, légende et source | Réalisé le 15 novembre avec assistance IA : courbe SVG, filtre de période, tableau des valeurs |
| 10 | Comparer deux épisodes réels et documenter résultats et limites | Réalisé le 15 novembre avec assistance IA : El Niño 1997-1998 et La Niña 1988-1989, valeurs calculées depuis l'API |
| 11 | Vérifier responsive, clavier, contrastes et états d'erreur | En partie le 15 novembre : clavier, états d'erreur, largeur de 390 px et contrastes vérifiés ; restent un téléphone réel et un lecteur d'écran |
| 12 | Exécuter un test frontend de changement de période ; documenter la preuve | Réalisé le 15 novembre avec assistance IA : 12 tests Vitest, dont le changement de période |
| 13 | Préparer configuration locale et documentation Compose/Caddy/VPS, sauvegardes et restauration | Non commencé |
| 14 | Vérifier l'intégration, corriger les anomalies, relancer les tests pertinents | Non commencé |

La suite du mois est réservée aux corrections, au dossier (15 pages maximum,
couverture comprise), aux diagrammes UML commentés et à la préparation de l'oral.

## Planning sur cinq jours demandé par l'épreuve

**Projection pour le dossier, à réviser : ce tableau ne décrit pas cinq journées
déjà travaillées.** Il organise le périmètre officiel ; le journal retrace séparément
la préparation réelle sur environ un mois.

| Journée de l'épreuve | Priorités prévues | Vérification attendue |
| --- | --- | --- |
| A | Besoin, backlog, source NOAA, parcours, wireframes et conception initiale | Périmètre réduit, source identifiée, critères d'acceptation |
| B | Modèle de données, migrations, transformation et import | Provenance et test de données |
| C | API, filtres, validation et intégration React | Test API période valide et entrée invalide |
| D | Courbe, sélection de période, comparaison et accessibilité | Test frontend et contrôle des interprétations |
| E | Intégration, corrections, dossier, déploiement proposé et répétition de code review | Trois tests documentés, dossier <= 15 pages, explications personnelles |

## Risques et arbitrages initiaux

- Confondre ONI et RONI ou dater incorrectement une saison : étudier le format avant de coder l'ETL.
- Confondre le statut HTTP avec la qualité scientifique : le rendre explicite dès le Jour 1.
- Perdre du temps dans des extensions : conserver uniquement le MVP obligatoire.
- Produire du code incompris : explication, exercice et validation entre les journées.
- Dépasser le dossier : réserver la couverture et le sommaire dans les 15 pages.
- Installation sous Windows : utiliser un environnement Python isolé et `npm.cmd`.

## Risques identifiés au Jour 2

- L'ONI n'est plus l'indice officiel de la NOAA depuis le 1er février 2026, au profit de la RONI : nommer la série « ONI ERSSTv6 » partout et justifier le choix (décision D13).
- Valeurs récentes révisables jusqu'à deux mois, et versions ERSST différentes : extraction datée, empreinte SHA-256, nouveau fichier à chaque téléchargement (D11).
- Saisons DJF et NDJ à cheval sur deux années : règle du mois central, vérifiée (D12).
- Arrondi trompeur au seuil de ±0,5 °C : comparer les valeurs à deux décimales du fichier.

## Risques identifiés lors de la transformation (12 novembre)

- Avec ses réglages par défaut, pandas décale les colonnes sans erreur si une ligne a un champ de trop : lecture en texte et en-tête contrôlé (D16).
- Une saison publiée deux fois avec des valeurs différentes : aucune version retenue, commande en échec (D17).
- Une valeur impossible (code de remplissage, erreur d'unité) acceptée comme mesure : bornes physiques larges (D18).
- Le chargement en base devra partager le modèle de données avec l'API : organisation de `etl/` à réexaminer (D15).

## Risques identifiés lors de la mise en place de la base (14 novembre)

- `NUMERIC(4, 2)` arrondirait sans erreur une troisième décimale : l'import devra refuser toute valeur plus précise (D22).
- Une révision NOAA d'une saison déjà importée se heurtera à la contrainte d'unicité : règle de mise à jour à décider avant l'import.
- La provenance du fichier brut n'existe qu'en Markdown : la rendre lisible par le programme d'import.
- Les tests du schéma exigent Docker Desktop lancé et la base `enso_monitor_test`.

## Risques identifiés lors de l'import et de l'API (14 novembre)

- Un fichier NOAA révisé sera refusé : définir une règle d'acceptation des révisions avant une nouvelle extraction (D24).
- Sous Windows, une base arrêtée bloquait une requête plus de 60 s : délai de connexion de 5 s (D25).
- Remise le 22 novembre : il reste l'interface, le test frontend, la comparaison et le dossier.

## Risques identifiés lors de l'interface (15 novembre)

- Deux épisodes éloignés n'ont pas la même période de référence : limites écrites dans l'interface (D29).
- Le test frontend utilise une API simulée : l'intégration réelle n'est vérifiée que par la démonstration manuelle (D30).
- `npm audit` signale 9 alertes modérées dans la chaîne ESLint (`minimatch`), à réexaminer.
- Remise le 22 novembre : restent la documentation du déploiement et le dossier de conception.

## Étape suivante

Documentation du déploiement : Docker Compose, Caddy et VPS (ligne 13), puis
intégration et corrections (ligne 14), et le dossier de conception. Bilan de
l'import et de l'API : [NOTE_IMPORT_API.md](NOTE_IMPORT_API.md).
