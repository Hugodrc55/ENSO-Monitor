# Dossier de conception

Livrable B de l'épreuve : document indépendant du README, 15 pages maximum,
couverture comprise, avec sommaire et pagination.

| Fichier | Rôle |
| --- | --- |
| `dossier.html` | Source du dossier : texte, mise en page A4 et diagrammes en SVG |
| `captures/` | Captures réelles de l'interface, prises le 16 novembre 2026 sur les données NOAA |
| `exporter.ps1` | Export PDF et contrôles : nombre de pages, passages à compléter |

## Exporter le PDF

Depuis la racine du dépôt, sous Windows, avec Chrome ou Edge installé :

```powershell
powershell -ExecutionPolicy Bypass -File docs/dossier/exporter.ps1
```

Le script produit `docs/dossier/ENSO_Monitor_dossier_de_conception.pdf`, exclu
de Git car il se régénère. Il affiche le nombre de pages et s'arrête en erreur
au-delà de 15. Il compte aussi les passages encadrés « À compléter », qui
doivent avoir disparu avant le rendu. `-ExecutionPolicy Bypass` ne vaut que pour
cette commande.

Le navigateur est lancé sans interface, avec un profil temporaire. Les numéros de
page viennent de la règle CSS `@page`.

## Modifier le dossier

- Chaque section commence sur une nouvelle page (`<section class="chapter">`).
  Les numéros du sommaire sont écrits à la main : si une section change de longueur,
  exporter, vérifier les pages, puis corriger le sommaire.
- Les passages à compléter par l'étudiant portent la classe `todo`.
- Badges : `tag ok` pour un résultat réellement vérifié et daté, `tag prop` pour
  une proposition non testée.
- Les diagrammes suivent le code : `backend/app/models.py` pour le modèle de
  domaine, `frontend/src/` et `backend/app/observations.py` pour la séquence.
  Toute modification de ces fichiers doit être reportée dans le schéma.

## Vérification du 16 novembre 2026

Export avec Chrome 157 : **15 pages**. Ce nombre a été compté de deux façons :
par le script et par le moteur PDF de Windows (`Windows.Data.Pdf`), qui a aussi
servi à afficher chaque page pour contrôler la lisibilité des schémas. Chaque
section commence à la page indiquée dans le sommaire. Quatre passages restent à
compléter par l'étudiant.
