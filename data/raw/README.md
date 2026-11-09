# Données brutes NOAA

Ce dossier contient des copies **non modifiées** de fichiers téléchargés auprès de
la NOAA. Elles ne doivent jamais être corrigées à la main : toute transformation
se fera par script, à partir de ces fichiers, dans une étape ultérieure.

## `noaa-cpc_oni-ersstv6_2026-11-09.txt`

| Information | Valeur |
| --- | --- |
| Producteur | NOAA, National Weather Service, Climate Prediction Center (CPC) |
| Série | Oceanic Niño Index (ONI), ERSSTv6, périodes de base centrées |
| URL exacte | <https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt> |
| Nom d'origine | `oni.ascii.txt` |
| Téléchargement | 9 novembre 2026 à 13:42 UTC (en-tête serveur `Date: Mon, 09 Nov 2026 13:42:35 GMT`) |
| Réponse HTTP | 200, `Content-Type: text/plain; charset=utf-8`, aucune redirection |
| Dernière modification côté NOAA | `Last-Modified: Tue, 03 Nov 2026 19:31:48 GMT` |
| Taille | 23 050 octets, 922 lignes (1 en-tête + 921 observations), ASCII, fins de ligne LF |
| Couverture | DJF 1950 à ASO 2026 |
| SHA-256 | `118c563331335c8649cdc2677e6be7ae89d1259d901345fcddbc2857af280f7f` |

Le nom local indique la source, la série et la date réelle d'extraction. La
version ERSSTv6 est établie par la page d'index de la NOAA, où ce lien figure
sous « Seasonal ERSSTv6 (centered base periods) "Oceanic Niño Index" ». Elle est
aussi confirmée par la comparaison avec les tableaux officiels v6 et v5 : voir
[la documentation scientifique](../../docs/DONNEES_NOAA.md).

Ce fichier n'est **pas** la RONI (`RONI.ascii.txt`), devenue l'indice officiel
de la NOAA le 1er février 2026. Les deux séries ne doivent pas être mélangées.

## Vérifier l'intégrité

PowerShell :

```powershell
Get-FileHash data/raw/noaa-cpc_oni-ersstv6_2026-11-09.txt -Algorithm SHA256
```

Git Bash ou Linux, depuis `data/raw/` :

```bash
sha256sum -c SHA256SUMS
```

L'empreinte doit être identique à celle du tableau. `.gitattributes` empêche Git
de convertir les fins de ligne de ces fichiers, ce qui changerait l'empreinte.

## Mise à jour

La NOAA met à jour ce fichier chaque mois et peut réviser les valeurs récentes.
Un nouveau téléchargement doit créer un **nouveau fichier** daté, avec sa propre
empreinte, sans écraser celui-ci.
