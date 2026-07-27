---
name: image-generation
description: Generar y editar imágenes con OpenAI (gpt-image-1). Usar cuando el usuario pida crear, generar, dibujar o editar una imagen, logo, banner, ilustración, thumbnail, foto o cualquier visual para una presentación. NO usar para diagramas explicativos estilo pizarra/sketchnote (esa es la skill `pizarra`).
allowed-tools: [Bash, Read, Write]
---

# Generación de imágenes (OpenAI gpt-image-1)

Genera imágenes desde texto, o edita una imagen existente. Útil para acompañar decks
(`gravity-deck`, `gravity-pptx`) con visuales propios en vez de stock genérico.

## Comando

```bash
python3 ~/.claude/skills/image-generation/scripts/generate_image.py \
  --prompt "DESCRIPCION" \
  --output ./assets/img/nombre.png \
  [--aspect 16:9] [--quality medium] [--image /ruta/entrada.png]
```

## Argumentos

| Arg | Obligatorio | Descripción |
|-----|-------------|-------------|
| `--prompt` | SÍ | Qué generar (o cómo editar la imagen de entrada). Sé descriptivo. |
| `--output` | SÍ | Ruta del PNG de salida. El script crea las carpetas que falten. |
| `--aspect` | NO | `1:1` (default), `16:9` (horizontal, slides), `9:16` (vertical, stories) |
| `--quality` | NO | `low` / `medium` / `high`. Default `medium` (~USD 0.06 por imagen 16:9). Usar `high` (~USD 0.25) solo cuando el detalle importe: fotos realistas, algo que va a producción. |
| `--image` | NO | Ruta a una imagen existente (`.png`, `.jpg`, `.webp`) para editarla/transformarla. |
| `--model` | NO | Default `gpt-image-1`. |

El script imprime la ruta final del PNG en stdout.

## Cómo usarla en la conversación

1. Traduce/mejora el prompt del usuario al inglés — `gpt-image-1` responde mejor así.
2. Ejecuta el comando. Guarda en una carpeta dedicada del proyecto (`assets/img/`), nombres en kebab-case sin acentos.
3. **Lee el PNG generado (`Read`) antes de reportarlo** — verifica que no salieran textos con typos ni elementos raros. Los modelos de imagen escriben mal el texto: si el visual necesita palabras, es mejor generarlo sin texto y ponerlo encima en el HTML/PPTX.
4. Reporta la ruta al usuario.

## Ejemplos

```bash
# Texto a imagen, horizontal para un slide
python3 ~/.claude/skills/image-generation/scripts/generate_image.py \
  --prompt "Abstract navy blue geometric background with subtle green accents, minimal, corporate" \
  --aspect 16:9 --output ./assets/img/fondo-portada.png

# Editar una imagen existente
python3 ~/.claude/skills/image-generation/scripts/generate_image.py \
  --prompt "Remove the background, keep only the product on pure white" \
  --image ./fotos/producto.jpg --output ./assets/img/producto-limpio.png
```

## Requisitos

- `pip install requests`
- `OPENAI_API_KEY` — se lee, en este orden:
  1. la variable de entorno `OPENAI_API_KEY`,
  2. una línea `OPENAI_API_KEY=sk-...` en `~/.claude/.env`,
  3. una línea igual en el `.env` de la carpeta actual.

  Se factura a la cuenta de OpenAI dueña de esa key.

## Anti-patrones

| ❌ No hacer | ✅ Hacer |
|------------|---------|
| Pedir imágenes con frases largas dentro | Generar sin texto y superponerlo en el deck |
| Usar `--quality high` por defecto | `medium` alcanza para casi todo; `high` cuesta 4x |
| Generar el logo de un cliente o de Gravity con IA | Usar el archivo oficial del logo |
| Entregar sin mirar el PNG | Siempre `Read` la imagen antes de reportarla |
