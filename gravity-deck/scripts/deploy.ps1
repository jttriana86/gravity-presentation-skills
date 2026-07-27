# Gravity Deck — Deploy script (Windows PowerShell)
# Uso: .\deploy.ps1 -DeckPath "C:\ruta\a\proyecto" [-Name "cliente-mes"] [-Pdf]
#
# Requisitos:
#  - Node.js + npm instalados (verificar con `node --version`)
#  - Cuenta gratis en https://vercel.com (primera vez, hará login interactivo)
#  - (Opcional) Microsoft Edge o Chrome para exportar PDF backup

param(
  [Parameter(Mandatory=$true)][string]$DeckPath,
  [string]$Name = "",
  [switch]$Pdf,
  [switch]$Production = $true
)

$ErrorActionPreference = "Stop"

# === Validaciones ===
if (-not (Test-Path $DeckPath)) {
  Write-Host "ERROR: la ruta '$DeckPath' no existe." -ForegroundColor Red
  exit 1
}

$indexFile = Join-Path $DeckPath "index.html"
if (-not (Test-Path $indexFile)) {
  $deckFile = Join-Path $DeckPath "deck.html"
  if (Test-Path $deckFile) {
    Write-Host "Renombrando deck.html -> index.html (Vercel sirve index por default)..." -ForegroundColor Yellow
    Copy-Item $deckFile $indexFile
  } else {
    Write-Host "ERROR: no se encontro index.html ni deck.html en $DeckPath" -ForegroundColor Red
    exit 1
  }
}

# === Nombre del proyecto ===
if ([string]::IsNullOrWhiteSpace($Name)) {
  $Name = (Split-Path $DeckPath -Leaf).ToLower() -replace '[^a-z0-9-]', '-'
}
Write-Host "Proyecto Vercel: $Name" -ForegroundColor Cyan

# === Generar vercel.json minimo si no existe ===
$vercelJson = Join-Path $DeckPath "vercel.json"
if (-not (Test-Path $vercelJson)) {
  $config = @{
    name = $Name
    cleanUrls = $true
    trailingSlash = $false
  } | ConvertTo-Json -Depth 3
  Set-Content -Path $vercelJson -Value $config -Encoding UTF8
  Write-Host "vercel.json generado." -ForegroundColor Gray
}

# === Deploy ===
Push-Location $DeckPath
try {
  Write-Host ""
  Write-Host "Deployando a Vercel..." -ForegroundColor Cyan
  Write-Host "(primera vez: Vercel pedira login con GitHub/email)" -ForegroundColor Gray
  Write-Host ""

  $deployArgs = @("vercel", "--yes", "--name", $Name)
  if ($Production) { $deployArgs += "--prod" }

  $url = & npx @deployArgs 2>&1 | Tee-Object -Variable output | Select-String -Pattern "https://.*vercel\.app" | Select-Object -Last 1

  if ($url) {
    $finalUrl = $url.Matches[0].Value
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "DEPLOY EXITOSO" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "URL: $finalUrl" -ForegroundColor Yellow
    Write-Host ""
    Set-Clipboard -Value $finalUrl
    Write-Host "(URL copiada al portapapeles)" -ForegroundColor Gray
  } else {
    Write-Host "Deploy completado pero no pude extraer URL. Revisa output:" -ForegroundColor Yellow
    Write-Host $output
  }
} finally {
  Pop-Location
}

# === Export PDF backup (opcional) ===
if ($Pdf) {
  Write-Host ""
  Write-Host "Generando PDF backup..." -ForegroundColor Cyan
  $pdfScript = Join-Path $PSScriptRoot "export-pdf.ps1"
  if (Test-Path $pdfScript) {
    & $pdfScript -DeckPath $DeckPath
  } else {
    Write-Host "Script export-pdf.ps1 no encontrado en $PSScriptRoot" -ForegroundColor Yellow
  }
}

Write-Host ""
Write-Host "Listo. Comparte la URL con tu cliente." -ForegroundColor Green
