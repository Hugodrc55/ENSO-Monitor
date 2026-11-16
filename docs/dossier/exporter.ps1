# Exporte le dossier de conception (dossier.html) en PDF avec Chrome ou Edge
# sans interface, puis contrôle le résultat : nombre de pages et passages
# encore marqués « À compléter ».
#
# Depuis la racine du dépôt :
#   powershell -ExecutionPolicy Bypass -File docs/dossier/exporter.ps1
#
# -ExecutionPolicy Bypass ne vaut que pour cette commande : aucun réglage
# de Windows n'est modifié.

param(
    [string]$Sortie = (Join-Path $PSScriptRoot 'ENSO_Monitor_dossier_de_conception.pdf')
)

$ErrorActionPreference = 'Stop'
$PagesMax = 15
$source = Join-Path $PSScriptRoot 'dossier.html'

# Navigateurs fondés sur Chromium : ils gèrent les numéros de page en CSS (@page).
$navigateur = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $navigateur) { throw 'Chrome ou Edge est introuvable.' }

# Profil temporaire : n'utilise ni l'historique ni les extensions du navigateur habituel.
$profil = Join-Path ([System.IO.Path]::GetTempPath()) 'enso-dossier-export'
if (Test-Path $Sortie) { Remove-Item $Sortie }

# Les chemins sont entre guillemets : le dossier du dépôt peut contenir des espaces.
$arguments = @(
    '--headless=new',
    '--disable-gpu',
    '--no-pdf-header-footer',
    "--user-data-dir=`"$profil`"",
    "`"--print-to-pdf=$Sortie`"",
    ([System.Uri]$source).AbsoluteUri
)
Start-Process -FilePath $navigateur -ArgumentList $arguments -Wait -NoNewWindow
if (-not (Test-Path $Sortie)) { throw "Le PDF n'a pas été produit." }

# Chaque page d'un PDF est un objet « /Type /Page » (« /Pages » désigne leur liste).
$octets = [System.IO.File]::ReadAllBytes($Sortie)
$contenu = [System.Text.Encoding]::GetEncoding('iso-8859-1').GetString($octets)
$pages = ([regex]::Matches($contenu, '/Type\s*/Page(?![a-z])')).Count
$aCompleter = ([regex]::Matches((Get-Content $source -Raw -Encoding UTF8), 'class="todo"')).Count

Write-Output "PDF : $Sortie ($([math]::Round($octets.Length / 1KB)) Ko)"
Write-Output "Pages : $pages (maximum $PagesMax, couverture comprise)"
Write-Output "Passages à compléter : $aCompleter"

if ($pages -gt $PagesMax) {
    Write-Warning "Le dossier dépasse $PagesMax pages."
    exit 1
}
if ($aCompleter -gt 0) {
    Write-Warning 'Des passages restent à compléter avant le rendu.'
}
