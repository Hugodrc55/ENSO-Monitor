# ETL — réservé aux prochaines étapes

Ce dossier accueillera le traitement Python des données NOAA ONI ERSSTv6.
Aucune transformation, aucun import et aucun accès à PostgreSQL ne sont encore
implémentés.

Au Jour 2 (9 novembre 2026), la source a été étudiée et le fichier brut a été
téléchargé manuellement dans [`data/raw/`](../data/raw/README.md). Son format,
la règle de datation des saisons et le plan de transformation sont décrits
dans [`docs/DONNEES_NOAA.md`](../docs/DONNEES_NOAA.md).

La transformation avec Pandas et NumPy est prévue au Jour 3, et l'import avec
provenance et contrôle des doublons au Jour 5. Chaque étape nécessite la
validation de l'étudiant.
