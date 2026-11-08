# Plan de préparation

Début réel : **4 novembre 2026**. Préparation prévue sur environ un mois, dont
14 journées de développement. Il s'agit d'une prévision, pas d'un historique.
Les journées ne sont pas nécessairement consécutives. Tout changement de durée
sera expliqué dans le journal, et chaque nouvelle étape attendra l'accord de l'étudiant.

| Jour | Objectif et critère de sortie prévu | Statut |
| --- | --- | --- |
| 1 | Dépôt Git, documentation, React strict, santé FastAPI, connexion vérifiée | Réalisé avec assistance IA ; validation personnelle attendue |
| 2 | Étudier NOAA ONI ERSSTv6 : format, unité, périodes, source, version et limites | À autoriser |
| 3 | Transformer la série avec Python, Pandas et NumPy ; expliquer le traitement | Non commencé |
| 4 | Modéliser PostgreSQL, contraintes SQL, SQLAlchemy et migrations Alembic | Non commencé |
| 5 | Import authentique, doublons, provenance, date d'extraction et test ETL | Non commencé |
| 6 | Exposer les observations avec FastAPI et documenter le contrat OpenAPI | Non commencé |
| 7 | Filtres temporels, validations et test API sur période + entrée invalide | Non commencé |
| 8 | Construire l'interface de consultation et brancher les observations | Non commencé |
| 9 | Ajouter courbe interactive, période sélectionnable, unité, légende et source | Non commencé |
| 10 | Comparer deux épisodes réels et documenter résultats et limites | Non commencé |
| 11 | Vérifier responsive, clavier, contrastes et états d'erreur | Non commencé |
| 12 | Exécuter un test frontend de changement de période ; documenter la preuve | Non commencé |
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

## Prochaine session : Jour 2 uniquement

Après validation : consulter la source NOAA, décrire son format, la signification
des colonnes, l'unité, les périodes et les limites, puis consigner les décisions.
Pas de script d'import, de schéma SQL ni de graphique pendant cette étude.
