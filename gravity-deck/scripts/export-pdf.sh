#!/usr/bin/env bash
# Gravity Deck — Export a PDF (macOS / Linux)
# Uso: ./export-pdf.sh <deck-path> [output.pdf]
#
# Usa Google Chrome headless. En Mac instala con: brew install --cask google-chrome

set -euo pipefail

DECK_PATH="${1:-}"
OUTPUT="${2:-}"

if [[ -z "$DECK_PATH" ]]; then
  echo "Uso: ./export-pdf.sh <deck-path> [output.pdf]"
  exit 1
fi

if [[ ! -d "$DECK_PATH" ]]; then
  echo "ERROR: la ruta '$DECK_PATH' no existe."
  exit 1
fi

DECK_PATH="$(cd "$DECK_PATH" && pwd)"

# === Buscar archivo HTML ===
INDEX_FILE="$DECK_PATH/index.html"
if [[ ! -f "$INDEX_FILE" ]]; then
  INDEX_FILE="$DECK_PATH/deck.html"
fi
if [[ ! -f "$INDEX_FILE" ]]; then
  echo "ERROR: no se encontro index.html ni deck.html en $DECK_PATH"
  exit 1
fi

# === Output path ===
if [[ -z "$OUTPUT" ]]; then
  DECK_NAME="$(basename "$DECK_PATH")"
  OUTPUT="$DECK_PATH/${DECK_NAME}-backup.pdf"
fi

# === Detectar Chrome ===
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS
  CHROME_CANDIDATES=(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    "/Applications/Chromium.app/Contents/MacOS/Chromium"
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
  )
else
  # Linux
  CHROME_CANDIDATES=(
    "$(command -v google-chrome 2>/dev/null || true)"
    "$(command -v chromium 2>/dev/null || true)"
    "$(command -v chromium-browser 2>/dev/null || true)"
    "$(command -v brave-browser 2>/dev/null || true)"
  )
fi

CHROME=""
for c in "${CHROME_CANDIDATES[@]}"; do
  if [[ -n "$c" && -e "$c" ]]; then
    CHROME="$c"
    break
  fi
done

if [[ -z "$CHROME" ]]; then
  echo "ERROR: no encontre Chrome/Chromium/Brave/Edge instalado."
  echo "Instalar con: brew install --cask google-chrome (macOS)"
  exit 1
fi

echo "Usando navegador: $CHROME"
echo "Generando PDF..."

# === Headless print-to-pdf ===
"$CHROME" \
  --headless=new \
  --disable-gpu \
  --no-margins \
  --print-to-pdf="$OUTPUT" \
  --print-to-pdf-no-header \
  --virtual-time-budget=10000 \
  "file://$INDEX_FILE"

if [[ -f "$OUTPUT" ]]; then
  SIZE=$(du -k "$OUTPUT" | cut -f1)
  echo ""
  echo "PDF generado: $OUTPUT (${SIZE} KB)"
else
  echo ""
  echo "ERROR generando PDF"
  exit 1
fi
