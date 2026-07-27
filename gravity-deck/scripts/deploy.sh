#!/usr/bin/env bash
# Gravity Deck — Deploy script (macOS / Linux)
# Uso: ./deploy.sh <deck-path> [project-name] [--pdf]
#
# Requisitos:
#  - Node.js + npm (verificar con `node --version`)
#  - Cuenta gratis en https://vercel.com (primera vez login interactivo)
#  - (Opcional) Google Chrome para exportar PDF backup

set -euo pipefail

# === Args ===
DECK_PATH="${1:-}"
PROJECT_NAME="${2:-}"
EXPORT_PDF=false

# Parse --pdf flag from any position
for arg in "$@"; do
  if [[ "$arg" == "--pdf" ]]; then
    EXPORT_PDF=true
  fi
done

# === Validaciones ===
if [[ -z "$DECK_PATH" ]]; then
  echo "Uso: ./deploy.sh <deck-path> [project-name] [--pdf]"
  exit 1
fi

if [[ ! -d "$DECK_PATH" ]]; then
  echo "ERROR: la ruta '$DECK_PATH' no existe."
  exit 1
fi

# Resolver path absoluto
DECK_PATH="$(cd "$DECK_PATH" && pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Verificar index.html (rename deck.html si hace falta)
if [[ ! -f "$DECK_PATH/index.html" ]]; then
  if [[ -f "$DECK_PATH/deck.html" ]]; then
    echo "Copiando deck.html -> index.html..."
    cp "$DECK_PATH/deck.html" "$DECK_PATH/index.html"
  else
    echo "ERROR: no se encontro index.html ni deck.html en $DECK_PATH"
    exit 1
  fi
fi

# === Nombre del proyecto ===
if [[ -z "$PROJECT_NAME" ]]; then
  PROJECT_NAME="$(basename "$DECK_PATH" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')"
fi
echo "Proyecto Vercel: $PROJECT_NAME"

# === Generar vercel.json minimo si no existe ===
if [[ ! -f "$DECK_PATH/vercel.json" ]]; then
  cat > "$DECK_PATH/vercel.json" <<EOF
{
  "name": "$PROJECT_NAME",
  "cleanUrls": true,
  "trailingSlash": false
}
EOF
  echo "vercel.json generado."
fi

# === Deploy ===
echo ""
echo "Deployando a Vercel..."
echo "(primera vez: Vercel pedira login con GitHub/email)"
echo ""

cd "$DECK_PATH"
URL=$(npx --yes vercel --prod --yes 2>&1 | tee /dev/stderr | grep -Eo 'https://[^[:space:]]+\.vercel\.app' | tail -1)

if [[ -n "$URL" ]]; then
  echo ""
  echo "================================================"
  echo "DEPLOY EXITOSO"
  echo "================================================"
  echo "URL: $URL"
  echo ""

  # Copy URL to clipboard (macOS pbcopy / Linux xclip)
  if command -v pbcopy >/dev/null 2>&1; then
    echo -n "$URL" | pbcopy
    echo "(URL copiada al portapapeles)"
  elif command -v xclip >/dev/null 2>&1; then
    echo -n "$URL" | xclip -selection clipboard
    echo "(URL copiada al portapapeles)"
  fi
else
  echo "Deploy completado pero no pude extraer URL."
fi

# === Export PDF backup ===
if $EXPORT_PDF; then
  echo ""
  echo "Generando PDF backup..."
  if [[ -f "$SCRIPT_DIR/export-pdf.sh" ]]; then
    bash "$SCRIPT_DIR/export-pdf.sh" "$DECK_PATH"
  else
    echo "Script export-pdf.sh no encontrado en $SCRIPT_DIR"
  fi
fi

echo ""
echo "Listo. Comparte la URL con tu cliente."
