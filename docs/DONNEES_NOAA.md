# Données NOAA — Oceanic Niño Index (ONI), ERSSTv6

Étude réalisée le **9 novembre 2026** (Jour 2), avec l'assistance de Claude.
Chaque affirmation sur la source renvoie à une page NOAA consultée ce jour-là
ou à une vérification exécutée sur le fichier téléchargé. Ce document ne
contient aucune prévision climatique.

## 1. Les données ENSO en bref

**ENSO** signifie *El Niño–Southern Oscillation*. C'est une variation naturelle
du climat dans le Pacifique tropical, qui couple l'océan et l'atmosphère. La NOAA
la décrit comme « le principal mode de variabilité climatique d'une année à
l'autre » (*« the leading pattern of year-to-year climate variability »*,
communiqué NWS 26-05). Elle influence les températures, les précipitations,
les trajectoires des tempêtes et l'activité cyclonique.

- **El Niño** est la phase **chaude** : la surface de l'océan est plus chaude que
  la normale dans le centre-est du Pacifique équatorial.
- **La Niña** est la phase **froide** : cette même surface est plus froide que
  la normale.
- Entre les deux, on parle de conditions **neutres**.
- *Southern Oscillation* désigne la composante atmosphérique du phénomène, liée
  à la pression et aux vents. L'ONI ne la mesure pas : il ne regarde que l'océan.

La NOAA précise que l'ONI est *une* mesure d'ENSO parmi d'autres. D'autres
indices sont nécessaires pour confirmer qu'un épisode s'accompagnait bien d'un
phénomène couplé océan-atmosphère.

## 2. L'indice ONI

L'**Oceanic Niño Index** est, selon la page ONI v6 de la NOAA, la *« moyenne
glissante sur 3 mois des anomalies de température de surface de la mer (SST)
ERSST.v6 dans la région Niño 3.4 (5°N–5°S, 120°–170°W) »*, calculée avec des
*« périodes de base de 30 ans centrées, mises à jour tous les 5 ans »*.

Décomposons :

| Terme | Signification |
| --- | --- |
| SST | *Sea Surface Temperature*, température de surface de la mer |
| ERSST | *Extended Reconstructed SST* : jeu de données NOAA reconstruit à partir d'observations (navires, bouées…) ; **v6** est sa version 6 |
| Niño 3.4 | Rectangle du Pacifique équatorial central, entre 5°N et 5°S, et entre 120°W et 170°W |
| Anomalie | Écart entre la température observée et une température de **référence** pour la même période de l'année |
| Période de base | Les 30 années servant à calculer la référence. Pour l'ONI, elle est centrée sur la période étudiée et mise à jour tous les 5 ans |
| Moyenne glissante sur 3 mois | Chaque valeur est la moyenne de trois mois consécutifs ; la fenêtre avance d'un mois à chaque ligne |

**Qu'est-ce qu'une anomalie ?** Si la référence de janvier vaut 26,5 °C et que
l'on observe 27,5 °C, l'anomalie vaut **+1,0 °C**. Une anomalie positive signifie
« plus chaud que d'habitude pour cette saison », une anomalie négative « plus
froid ». On utilise une anomalie plutôt que la température brute parce que la
température varie naturellement au fil de l'année. En 1950, la température passe
par exemple de 25,01 °C (DJF) à 26,35 °C (AMJ), alors que l'anomalie reste
négative toute l'année.

**Seuils utilisés par la NOAA** (page ONI v6) : on parle de période chaude
(El Niño) lorsque l'ONI est **≥ +0,5 °C** et de période froide (La Niña)
lorsqu'il est **≤ −0,5 °C**. Pour classer un **épisode historique**, ce seuil
doit être atteint pendant **au moins 5 saisons glissantes consécutives**. Une
seule saison au-dessus du seuil ne suffit pas à définir un épisode.

Les textes NOAA formulent ce seuil tantôt « ±0,5 °C » (page ONI), tantôt
« 0,5 °C ou plus » (communiqué 26-05), tantôt « supérieur à 0,5 » (page RONI).
Le code devra donc fixer et documenter la comparaison retenue (`>=` ou `>`).

## 3. Origine, version et statut de la série

- **Producteur** : NOAA, National Weather Service, NCEP, Climate Prediction Center (CPC).
- **Série** : ONI, calculé à partir d'**ERSSTv6** avec des périodes de base centrées.
- **Preuve de la version** :
  1. La page d'index des données NOAA (<https://www.cpc.ncep.noaa.gov/data/indices/>)
     place le lien `oni.ascii.txt` sous l'intitulé *« Seasonal ERSSTv6 (centered
     base periods) "Oceanic Niño Index" or the 3-month running average in Niño 3.4 »*.
  2. Les 921 valeurs `ANOM` du fichier ont été comparées aux tableaux HTML
     officiels (valeurs à une décimale) :

     | Tableau NOAA | Valeurs comparées | Écart ≤ 0,05 | Écart > 0,05 |
     | --- | --- | --- | --- |
     | [ONI v6](https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/index.php) | 921 | **921** | 0 |
     | [ONI v5](https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v5/) | 917 | 422 | **495** |

     Le fichier correspond au tableau v6, et non au v5. Les 51 valeurs dont
     l'arrondi diffère du tableau v6 sont toutes exactement à 0,05 d'écart (par
     exemple `-0.45` dans le fichier, `-0.4` sur la page). C'est un effet
     d'arrondi, sans contradiction.
- **Statut depuis 2026** : selon le *Public Information Statement 26-05* du
  National Weather Service (émis le 13 janvier 2026), la NOAA utilise depuis le
  **1er février 2026** la **RONI** (*Relative Oceanic Niño Index*) pour la
  surveillance et la prévision officielles d'ENSO. Le même communiqué précise que
  *« the legacy Niño 3.4 and Oceanic Niño Index files will continue to be
  updated »*. La page ONI v6 confirme qu'elle reste mise à jour avant le 5 de
  chaque mois.

### ONI ou RONI : ne pas mélanger

| | ONI (notre série) | RONI (non utilisée) |
| --- | --- | --- |
| Calcul | Anomalie SST de Niño 3.4 | Anomalie SST de Niño 3.4 **moins** l'anomalie moyenne des tropiques (20°N–20°S), puis remise à l'échelle pour retrouver l'amplitude de l'indice traditionnel |
| Référence | Périodes de 30 ans centrées, mises à jour tous les 5 ans | Période fixe 1991–2020 |
| Statut NOAA | Série historique, toujours mise à jour | Indice officiel depuis le 1er février 2026 |
| Fichier | `data/indices/oni.ascii.txt` | `data/indices/RONI.ascii.txt` |

L'idée de la RONI : mesurer si Niño 3.4 est plus chaud ou plus froid *que le
reste des tropiques*, et non seulement par rapport à sa propre moyenne passée.
Selon le communiqué, cette approche est *« less sensitive to the chosen base
climatology period »* et plus liée aux variations de pluie du Pacifique tropical.

Les deux indices peuvent conduire à des conclusions différentes pour une même
saison. Valeurs lues le 9 novembre 2026 sur les pages officielles :

| Saison | ONI v6 | RONI |
| --- | --- | --- |
| DJF 2026 | −0,4 (au-dessus du seuil La Niña) | −0,9 (sous le seuil La Niña) |
| ASO 2026 | 2,5 | 2,0 |

Une même valeur ne peut donc pas être lue avec l'autre indice. L'application
affichera toujours le nom exact de la série : « ONI ERSSTv6 ».

## 4. URL et date d'extraction

| Information | Valeur |
| --- | --- |
| URL du fichier | <https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt> |
| Page de référence | <https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/index.php> |
| Date d'extraction | **9 novembre 2026**, 13:42 UTC |
| Réponse HTTP | 200, `text/plain; charset=utf-8`, aucune redirection, 23 050 octets |
| `Last-Modified` NOAA | 3 novembre 2026, 19:31:48 GMT |
| Copie locale | [`data/raw/noaa-cpc_oni-ersstv6_2026-11-09.txt`](../data/raw/noaa-cpc_oni-ersstv6_2026-11-09.txt) |
| SHA-256 | `118c563331335c8649cdc2677e6be7ae89d1259d901345fcddbc2857af280f7f` |

Une **empreinte SHA-256** est une « signature » de 64 caractères calculée à
partir des octets du fichier. Si un seul caractère change, l'empreinte change.
Elle permet de prouver que le fichier analysé est bien celui qui a été téléchargé.

## 5. Les colonnes du fichier

Le fichier est un texte à colonnes séparées par des espaces, avec une ligne
d'en-tête : ` SEAS  YR   TOTAL   ANOM`.

| Colonne | Type observé | Signification | Unité |
| --- | --- | --- | --- |
| `SEAS` | 3 lettres | Saison : les initiales anglaises des trois mois de la moyenne glissante | — |
| `YR` | Entier à 4 chiffres | Année de la saison, c'est-à-dire **l'année du mois central** (vérifié, voir ci-dessous) | année |
| `TOTAL` | Décimal, 2 décimales | Température moyenne de surface de la mer dans Niño 3.4 sur les 3 mois | °C |
| `ANOM` | Décimal, 2 décimales | Anomalie de cette température par rapport à la référence : **c'est la valeur de l'ONI** | °C |

**Origine des définitions.** Le fichier ne contient ni dictionnaire des colonnes
ni unité. Les définitions ci-dessus s'appuient sur trois éléments :

- le libellé de la page d'index NOAA ;
- la page ONI v6, dont le seuil est exprimé en °C ;
- deux vérifications sur les données. Le fichier mensuel que la NOAA présente
  comme *« monthly input to the Oceanic Niño Index »* (`detrend.nino34.ascii.txt`,
  colonnes `YR MON TOTAL ClimAdjust ANOM`) a été téléchargé pour contrôle,
  sans être conservé. La moyenne de trois mois consécutifs de ce fichier
  retrouve `ANOM` pour 919 saisons sur 921, et `TOTAL` pour 920 sur 921, à
  0,01 près (écart maximal : 0,013, dû aux arrondis).

### Les douze saisons

| `SEAS` | Mois moyennés | Mois central | Exemple |
| --- | --- | --- | --- |
| DJF | décembre, janvier, février | janvier | `DJF 1950` = déc. 1949 → févr. 1950 |
| JFM | janvier, février, mars | février | |
| FMA | février, mars, avril | mars | |
| MAM | mars, avril, mai | avril | |
| AMJ | avril, mai, juin | mai | |
| MJJ | mai, juin, juillet | juin | |
| JJA | juin, juillet, août | juillet | |
| JAS | juillet, août, septembre | août | |
| ASO | août, septembre, octobre | septembre | `ASO 2026` = août → oct. 2026 |
| SON | septembre, octobre, novembre | octobre | |
| OND | octobre, novembre, décembre | novembre | |
| NDJ | novembre, décembre, janvier | décembre | `NDJ 2025` = nov. 2025 → janv. 2026 |

**Attention à DJF et NDJ**, qui chevauchent deux années civiles. La règle a été
**vérifiée et non supposée** : `YR` est toujours l'année du **mois central**.

- Hypothèse retenue : `DJF 1950` = décembre 1949 + janvier + février 1950.
  Les moyennes mensuelles concordent pour 919 saisons sur 921.
- Hypothèse rejetée : `DJF 1950` = décembre 1950 + janvier + février 1951.
  Les écarts atteignent 3,72 °C.
- Indice cohérent : le fichier mensuel commence en décembre 1949, et `DJF 2026`
  figure déjà dans un fichier publié en novembre 2026.

Les saisons se **chevauchent** : DJF et JFM partagent janvier et février.
Douze valeurs par an ne sont donc pas douze mesures indépendantes.

## 6. Exemples réels tirés du fichier

Début du fichier (lignes 1 à 6) :

```text
 SEAS  YR   TOTAL   ANOM
  DJF 1950  25.01  -1.32
  JFM 1950  25.36  -1.20
  FMA 1950  25.88  -1.12
  MAM 1950  26.24  -1.08
  AMJ 1950  26.35  -1.10
```

Les valeurs extrêmes de la série au 9 novembre 2026, avec leurs voisines :

```text
  OND 1973  24.57  -1.89
  NDJ 1973  24.39  -2.04    <- ANOM et TOTAL minimaux
  DJF 1974  24.61  -1.87

  OND 2015  29.10   2.45
  NDJ 2015  29.15   2.59    <- ANOM maximale
  DJF 2016  29.05   2.50
```

Autres valeurs élevées, en fin d'année 1997 :

```text
  OND 1997  28.97   2.34
  NDJ 1997  28.96   2.37
  DJF 1998  28.85   2.22
```

Fin du fichier, valeurs les plus récentes et provisoires :

```text
  JJA 2026  29.09   1.80
  JAS 2026  29.12   2.16
  ASO 2026  29.23   2.46    <- dernière ligne ; TOTAL maximal de la série
```

Lecture de `NDJ 2015 29.15 2.59` : de novembre 2015 à janvier 2016, la surface
de la région Niño 3.4 a été en moyenne à 29,15 °C, soit 2,59 °C de plus que la
référence de cette saison.

**La référence change au fil du temps.** `TOTAL − ANOM` donne la référence
implicite d'une saison :

```text
  DJF 1980  27.09   0.62    -> référence ≈ 26,47 °C
  DJF 1981  26.31  -0.27    -> référence ≈ 26,58 °C
```

Cette hausse de 0,11 °C illustre le changement de période de base de 30 ans.
Conséquence pour le code : il ne faut **pas** recalculer `ANOM` à partir de
`TOTAL` avec une référence fixe. On conserve l'anomalie publiée par la NOAA.

## 7. Période couverte et contrôles effectués

| Contrôle sur le fichier téléchargé | Résultat |
| --- | --- |
| Ressource accessible | HTTP 200, sans redirection |
| Fichier non vide, pas une page HTML | 23 050 octets ; aucune balise `<html>` ou `<!doctype>` |
| Encodage et fins de ligne | ASCII pur ; 922 fins de ligne LF, aucun CR ; saut de ligne final présent |
| En-tête | Exactement `SEAS`, `YR`, `TOTAL`, `ANOM` |
| Format des 921 lignes | Toutes conformes : 3 lettres, année sur 4 chiffres, deux décimaux à 2 décimales |
| Codes de saison | Uniquement les 12 codes attendus |
| Doublons (`SEAS`, `YR`) | Aucun |
| Valeurs manquantes ou sentinelles (\|v\| ≥ 99) | Aucune |
| Continuité | Aucune saison sautée ni désordonnée de DJF 1950 à ASO 2026 |
| Années incomplètes | Seulement 2026 (9 saisons sur 12 : SON, OND et NDJ pas encore calculables) |
| Plage `TOTAL` | 24,39 °C (NDJ 1973) à 29,23 °C (ASO 2026) |
| Plage `ANOM` | −2,04 °C (NDJ 1973) à +2,59 °C (NDJ 2015) |

**Période couverte : de DJF 1950 (décembre 1949) à ASO 2026 (octobre 2026),
soit 921 saisons.** Cela représente 76 années complètes et 9 saisons de 2026.

Ces contrôles ont été exécutés avec des scripts Python temporaires (bibliothèque
standard, hors du dépôt). Ils seront réécrits au Jour 3 avec Pandas et NumPy,
puis automatisés par des tests.

## 8. Unités et règles d'interprétation

- `TOTAL` et `ANOM` sont en **degrés Celsius (°C)**. L'anomalie est un *écart*
  de température : +1,0 signifie « 1 °C au-dessus de la référence ».
- Le fichier donne 2 décimales, les pages NOAA en affichent une. **L'arrondi
  peut tromper** : `MAM 2026` vaut `0.46` dans le fichier mais s'affiche
  « 0,5 » sur la page. Arrondie, la valeur semble atteindre le seuil, alors
  qu'elle reste en dessous. Les comparaisons se feront sur les valeurs du
  fichier, et l'interface indiquera la précision affichée.
- Une valeur décrit **une saison de 3 mois**, pas un jour ni un mois précis.
- Un **épisode** El Niño ou La Niña exige au moins 5 saisons consécutives
  au-delà de ±0,5 °C. Le sujet rappelle que « Super El Niño » n'est pas une
  classe scientifique universelle : tout classement devra définir l'indice, les
  seuils et la durée.
- L'ONI est une température océanique régionale. Il ne mesure ni les pluies ni
  les impacts locaux, et ne permet pas de prédire la météo d'un lieu.

## 9. Limites scientifiques et précautions

1. **Valeurs récentes provisoires.** Selon la NOAA, les valeurs peuvent changer
   jusqu'à deux mois après leur première publication. Les dernières saisons
   (JAS et ASO 2026 au moment de l'extraction) sont des estimations.
2. **Révisions de version.** Les tableaux v5 et v6 diffèrent sur 495 saisons.
   Une même URL peut donc fournir des valeurs différentes selon la version du
   jeu ERSST. La date d'extraction et l'empreinte permettent de savoir quelle
   version a été utilisée.
3. **Référence mobile.** Les périodes de base changent tous les 5 ans. Comparer
   deux épisodes éloignés revient à comparer des écarts calculés par rapport à
   des références différentes. C'est l'une des raisons de la création de la RONI.
4. **Indice non officiel depuis le 1er février 2026.** L'ONI reste publié, mais
   la NOAA utilise la RONI pour la surveillance officielle.
5. **Reconstruction sans incertitude fournie.** ERSST est une reconstruction
   statistique. Le fichier ne donne aucune marge d'incertitude, ce qui ne veut
   pas dire que les valeurs sont exactes.
6. **Valeurs dépendantes.** Les saisons glissantes se chevauchent. Il faut en
   tenir compte avant toute statistique, même simple.
7. **Une seule région, une seule variable.** L'ONI ne décrit pas à lui seul le
   couplage océan-atmosphère.
8. **Incohérence relevée dans la documentation NOAA.** La page ONI v6 mentionne
   *« the high frequency filter applied to the ERSSTv5 data »* alors que le
   reste de la page, la page RONI et l'index parlent d'ERSSTv6. Cela ressemble
   à un reste de l'ancienne page. Le constat est signalé sans être interprété.
9. **Aucune prévision.** Ce projet affiche des observations passées. Il ne
   prédit pas l'évolution d'ENSO.

## 10. Plan de transformation prévu pour le Jour 3

Le Jour 3 ne commencera qu'après l'accord de l'étudiant. Il produira une
transformation testable, sans base de données : PostgreSQL, SQLAlchemy et
Alembic viendront aux Jours 4 et 5.

1. **Lire** le fichier brut sans le modifier, avec Pandas (`read_csv` et
   séparateur « espaces »). Vérifier l'empreinte SHA-256 avant le traitement.
2. **Valider la structure** et refuser le fichier s'il échoue :
   - en-tête exact ;
   - 12 codes de saison ;
   - années entières ;
   - décimaux finis (NumPy) ;
   - aucune valeur manquante ou sentinelle ;
   - aucun doublon `(SEAS, YR)` ;
   - séquence continue.
3. **Dater chaque saison** selon la règle vérifiée (décision D12) :
   - `reference_month` = 1er jour du mois central (`DJF 1950` → `1950-01-01`,
     `NDJ 2025` → `2025-12-01`). Comme `YR` est l'année du mois central, aucune
     exception n'est nécessaire pour DJF et NDJ.
   - `period_start` et `period_end` : début du premier mois et fin du troisième
     (`DJF 1950` → du `1949-12-01` au `1950-02-28`), pour l'affichage.
   - `SEAS` et `YR` d'origine sont **conservés**, pour pouvoir toujours
     retrouver la ligne NOAA.
4. **Conserver `ANOM` tel quel**, sans le recalculer (référence mobile).
5. **Attacher la provenance** à chaque import : code de série `ONI_ERSSTv6`, URL,
   nom du fichier, SHA-256, date d'extraction et `Last-Modified`. Ces éléments
   préparent les entités *Indice*, *Source* et *Import* demandées pour l'UML.
6. **Tester** la transformation sur le vrai fichier, puis sur une copie
   volontairement altérée (doublon, saison inconnue, valeur manquante).

Piste de représentation dans PostgreSQL, **à décider au Jour 4** et non
implémentée : une ligne par `(série, SEAS, YR)` avec une contrainte d'unicité.
Les valeurs seraient stockées en `NUMERIC` plutôt qu'en `float`, pour conserver
exactement les deux décimales publiées.

### Problèmes à anticiper

| Problème | Situation au 9 novembre 2026 | Traitement prévu |
| --- | --- | --- |
| Doublons | Aucun | Refus du fichier ; contrainte d'unicité en base |
| Valeurs manquantes | Aucune | Refus explicite, jamais de valeur inventée ou interpolée |
| Dates incohérentes | Aucune ; DJF et NDJ demandent une règle claire | Règle du mois central, contrôle de la séquence |
| Année incomplète | 2026 : 9 saisons | Normal ; ne pas compléter |
| Révisions NOAA | Valeurs récentes provisoires ; v5 et v6 différentes | Nouveau fichier daté à chaque extraction, comparaison avec l'import précédent |
| Confusion ONI/RONI | Fichiers distincts | Un seul fichier ONI importé, code de série explicite |

## Sources consultées le 9 novembre 2026

- NOAA CPC, ONI v6 : <https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/index.php>
- NOAA CPC, ONI v5 (comparaison) : <https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v5/>
- NOAA CPC, RONI : <https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/>
- NOAA CPC, index des données : <https://www.cpc.ncep.noaa.gov/data/indices/>
- NOAA CPC, fichier ONI : <https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt>
- NOAA CPC, fichier mensuel de contrôle : <https://www.cpc.ncep.noaa.gov/data/indices/detrend.nino34.ascii.txt>
- NWS, *Public Information Statement 26-05*, 13 janvier 2026 : <https://www.weather.gov/media/notification/pdf_2026/pns26-05_Relative_ONI.pdf>
- Référence citée par la NOAA pour ERSSTv6 : Huang et al., 2025, *Journal of Climate*, parties 1 et 2 (non consultée directement).
