# Plan de préparation

Début réel : **4 novembre 2026**. Préparation prévue sur environ un mois, dont
14 journées de développement. Il s'agit d'une prévision, pas d'un historique.
Les journées ne sont pas nécessairement consécutives. Tout changement de durée
sera expliqué dans le journal, et chaque nouvelle étape attendra l'accord de l'étudiant.

| Jour | Objectif et critère de sortie prévu | Statut |
| --- | --- | --- |
| 1 | Dépôt Git, documentation, React strict, santé FastAPI, connexion vérifiée | Réalisé avec assistance IA ; validation personnelle attendue |
| 2 | Étudier NOAA ONI ERSSTv6 : format, unité, périodes, source, version et limites | Réalisé le 9 novembre avec assistance IA ; validation personnelle attendue |
| 3 | Transformer la série avec Python, Pandas et NumPy (contrôles, dates du mois central, provenance) ; expliquer le traitement | À autoriser |
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

## Risques identifiés au Jour 2

- L'ONI n'est plus l'indice officiel de la NOAA depuis le 1er février 2026, au profit de la RONI : nommer la série « ONI ERSSTv6 » partout et justifier le choix (décision D13).
- Valeurs récentes révisables jusqu'à deux mois, et versions ERSST différentes : extraction datée, empreinte SHA-256, nouveau fichier à chaque téléchargement (D11).
- Saisons DJF et NDJ à cheval sur deux années : règle du mois central, vérifiée (D12).
- Arrondi trompeur au seuil de ±0,5 °C : comparer les valeurs à deux décimales du fichier.

## Prochaine session : Jour 3 uniquement

Après validation : transformer le fichier brut avec Pandas et NumPy selon le plan
de [DONNEES_NOAA.md](DONNEES_NOAA.md#10-plan-de-transformation-prévu-pour-le-jour-3).
Les contrôles, la datation et la provenance seront testés. Pas de PostgreSQL,
de SQLAlchemy, d'Alembic, d'API d'observations ni de graphique pendant cette étape.
