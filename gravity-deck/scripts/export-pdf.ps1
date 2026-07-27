# Gravity Deck — Export a PDF (backup para clientes que pidan PPT)
# Uso: .\export-pdf.ps1 -DeckPath "C:\ruta\a\proyecto" [-Output "deck-backup.pdf"]
#
# Usa Microsoft Edge headless (viene con Windows 10/11). Si prefieres Chrome, edita la variable $browser.

param(
  [Parameter(Mandatory=$true)][string]$DeckPath,
  [string]$Output = ""
)

$ErrorActionPreference = "Stop"

# === Buscar archivo HTML ===
$indexFile = Join-Path $DeckPath "index.html"
if (-not (Test-Path $indexFile)) {
  $indexFile = Join-Path $DeckPath "deck.html"
}
if (-not (Test-Path $indexFile)) {
  Write-Host "ERROR: no se encontro index.html ni deck.html en $DeckPath" -ForegroundColor Red
  exit 1
}

# === Output path ===
if ([string]::IsNullOrWhiteSpace($Output)) {
  $deckName = Split-Path $DeckPath -Leaf
  $Output = Join-Path $DeckPath "$deckName-backup.pdf"
}

# === Detectar Edge o Chrome ===
$browsers = @(
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
  "${env:ProgramFiles}\Microsoft\Edge\Application\msedge.exe",
  "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
)
$browser = $browsers | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $browser) {
  Write-Host "ERROR: no encontre Edge ni Chrome instalado." -ForegroundColor Red
  Write-Host "Instala Microsoft Edge (viene con Windows) o Google Chrome." -ForegroundColor Yellow
  exit 1
}

Write-Host "Usando navegador: $browser" -ForegroundColor Gray

# === Convertir a URL file:// ===
$fileUrl = ([Uri](Resolve-Path $indexFile)).AbsoluteUri

# === Ejecutar headless print-to-pdf ===
Write-Host "Generando PDF..." -ForegroundColor Cyan

$args = @(
  "--headless=new",
  "--disable-gpu",
  "--no-margins",
  "--print-to-pdf=`"$Output`"",
  "--print-to-pdf-no-header",
  "--virtual-time-budget=10000",  # esperar 10s a que carguen fuentes y animaciones
  "`"$fileUrl`""
)

$proc = Start-Process -FilePath $browser -ArgumentList $args -Wait -PassThru -NoNewWindow

if ($proc.ExitCode -eq 0 -and (Test-Path $Output)) {
  $size = [math]::Round((Get-Item $Output).Length / 1KB, 1)
  Write-Host ""
  Write-Host "PDF generado: $Output ($size KB)" -ForegroundColor Green
} else {
  Write-Host ""
  Write-Host "ERROR generando PDF (exit code: $($proc.ExitCode))" -ForegroundColor Red
  exit 1
}
