# Consignes de travail — ENSO Monitor

## Périmètre et progression

- Projet individuel HETIC WEB3. Répondre et expliquer les changements en français.
- Lire intégralement `docs/sujet/HETIC_WEB3_Projet_ENSO_Monitor.pdf` avant toute modification. Si la copie locale manque, demander le fichier ; consulter aussi `docs/EXIGENCES.md`.
- Réaliser uniquement la journée explicitement autorisée. Le Jour 1 est l'étape initiale autorisée ; toute journée suivante nécessite l'accord de l'étudiant.
- Présenter l'objectif et les fichiers concernés avant les modifications. À la fin : expliquer, vérifier, proposer des commits et attendre la validation.
- Ne jamais fabriquer des journées, dates, commits, résultats de tests ou observations climatiques.

## Architecture et qualité

- Frontend : React, Vite, TypeScript strict. Backend : Python, FastAPI et Pydantic.
- À introduire aux étapes prévues : PostgreSQL, SQLAlchemy, Alembic, Pandas, NumPy, tests de données et tests frontend.
- Indice retenu par l'étudiant : NOAA ONI, version ERSSTv6. Ne pas mélanger ONI et RONI.
- Conserver une architecture simple et séparer frontend, API et ETL. Justifier chaque dépendance.
- Expliquer les fonctions importantes et proposer un petit exercice personnel.
- Ne déclarer un test réussi qu'après son exécution. Un test de santé ne satisfait pas le test d'API filtrée exigé pour le livrable final.

## Git et traçabilité

- Commits atomiques, réels, messages courts avec `feat:`, `fix:`, `docs:`, `test:`, `refactor:` ou `chore:`.
- Proposer les commandes de revue, commit et push à chaque fin de session.
- Aucun push sans autorisation ; aucune réécriture d'historique ou force-push sans accord.
- Ne pas committer les secrets, `.env`, dépendances, environnements virtuels, fichiers temporaires ou le PDF officiel de l'épreuve.
- Maintenir `README.md`, `docs/PLAN.md`, `docs/DECISIONS.md` et `docs/JOURNAL.md`.
- Journaliser la date réelle communiquée par la session, les changements, erreurs, corrections, vérifications exécutées et contributions de l'IA.
- Distinguer le travail produit avec l'IA de la compréhension et de la validation personnelles de l'étudiant, qui ne doivent jamais être supposées.

## Livrables finaux

- Application et code source ; dossier indépendant de 15 pages maximum, couverture comprise.
- Inclure le planning sur cinq jours demandé par l'épreuve, distinct de la préparation progressive sur environ un mois.
- Documenter une cible VPS, Docker Compose et Caddy. Déploiement réel facultatif ; aucun achat nécessaire.
