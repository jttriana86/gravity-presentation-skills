---
name: deck-imagenes
description: Pone imágenes generadas con IA dentro de una presentación — decks HTML de Gravity y PPTX editables — con la paleta de la marca y sin romper el layout de la lámina. Genera el asset desde el contenido del slide (foto editorial, ilustración plana, textura de fondo o pizarra/sketchnote), lo optimiza y lo inserta. Usar cuando pidan "métele una imagen a este deck", "una foto para la portada", "un gráfico dibujado para explicar esto", "ilustra el slide 4", "este deck está muy plano", "ponle visuales a la presentación", o al cerrar un deck que quedó todo texto. NO es para generar una imagen suelta (eso es `image-generation`), ni para crear el deck (eso es `gravity-deck` / `gravity-pptx`).
---

# Deck imágenes — de un concepto a una imagen colocada en la lámina

Puente entre las skills de imagen y las de presentaciones. Un solo comando genera el asset
en la paleta correcta, lo optimiza y lo mete en el deck: HTML (`gravity-deck`)
o PPTX (`gravity-pptx` vía su JSON spec).

## La regla que manda todo: la lámina NO crece

El slide mide **1280×720 lógicos** y está fijo. Todo lo que no cabe **se corta**, no hace
scroll. De ahí salen los cinco patrones y sus restricciones — no son estética, son física.

## Patrones (elegí por lo que YA tiene el slide)

| Patrón | Qué hace | Cuándo |
|--------|----------|--------|
| `full` | **Crea un slide nuevo** dedicado a la imagen, con eyebrow + título + caption, y renumera el resto del deck | **El default.** Cuando el deck ya está armado y querés sumar visual sin tocar nada |
| `hero` | Imagen de fondo a sangre + overlay navy 62-78% | Portada, divisor, cierre. Solo donde el texto es corto y blanco |
| `split` | Imagen a la izquierda, contenido existente a la derecha | Slides de **texto o bullets**. Nunca con métricas o tablas |
| `card` | Figura con bezel (border-top navy + sombra) bajo el contenido | Slides con aire de sobra |
| `band` | Banda horizontal decorativa al pie | Cierre de sección, respiro visual |

El script **rechaza** `card`/`band`/`split` en slides que ya traen `cards-grid`, `tbl-wrap`,
`compare-grid`, `timeline` o `findings`, y te manda a `full`. No es cautela: probado, la
imagen queda cortada por abajo.

## Estilos de imagen

| `--style` | Qué produce | Para qué |
|-----------|-------------|----------|
| `photo` | Foto editorial, luz natural, paleta desaturada con el navy de la marca presente | Portadas, contexto humano, equipo, oficina |
| `illustration` | Vector plano sobre blanco, navy dominante + un acento | Conceptos, servicios, propuesta de valor |
| `texture` | Textura abstracta bajísimo contraste | Fondos que van **debajo** de texto |
| `pizarra` | Sketchnote a marcador con muñequitos y flechas | Explicar un proceso o un flujo |

Los cuatro llevan las mismas **guardas** en el prompt: sin texto, sin letras, sin logos, sin
marcos, con 5% de margen seguro. Los modelos de imagen escriben con faltas de ortografía —
la regla es que no escriban nada, y el texto lo pone el HTML.

## Uso

```bash
# 1. Ver qué haría, sin gastar API ni tocar archivos
python scripts/slide_image.py --concept "..." --pattern full --dry-run

# 2. Slide nuevo dedicado, insertado en la posición 5 del deck
python scripts/slide_image.py \
  --concept "equipo revisando resultados en una sala luminosa" \
  --style photo --pattern full \
  --deck ./proyecto/deck.html --slide 5 \
  --eyebrow "CÓMO TRABAJAMOS" --title "El comité de resultados" \
  --caption "Sesión mensual con el cliente"

# 3. Fondo de portada
python scripts/slide_image.py --concept "arquitectura corporativa desde abajo" \
  --style photo --pattern hero --deck ./proyecto/deck.html --slide 1

# 4. PPTX: se inserta en el JSON spec y después se regenera el .pptx
python scripts/slide_image.py --concept "el recorrido de un lead hasta el cierre" \
  --style pizarra --spec ./proyecto/spec.json --slide 4 \
  --eyebrow "EL PROCESO" --title "Cómo viaja un lead"
python ../gravity-pptx/scripts/build_deck.py ./proyecto/spec.json ./salida.pptx
```

Flags útiles: `--aspect 1:1|16:9|9:16`,
`--quality low|medium|high` (medium ≈ USD 0.06; high ≈ 0.25, solo si el detalle importa),
`--transparent` (PNG con alfa, para recortes), `--extra "…"` (instrucciones sueltas al prompt).

## Qué hace el script por vos

1. **Prompt de marca**: receta del estilo + hex de la paleta + guardas.
2. **Optimización**: WebP calidad 82 para HTML (~60-120 KB), **JPEG para PPTX**
   (PowerPoint no lee WebP y el PNG deja el archivo 10× más pesado), PNG solo con `--transparent`.
3. **CSS**: inyecta el bloque de patrones **una sola vez**, con las reglas base *antes* del
   primer `@media` y las móviles al final — si se invierte, el bloque móvil del deck pierde
   y el responsive se rompe.
4. **Inserción**: HTML por `data-slide`, o el spec JSON de `gravity-pptx`.
5. **Renumeración** (`full`): reescribe `data-slide` y los `NN / NN` de cada `page-num`
   según el slide que los contiene.

## Checklist antes de entregar

- [ ] **Abrí la captura.** `--pattern full` y `hero` son seguros; `card`/`split` dependen del
      contenido que ya tenía el slide.
- [ ] Escritorio (1600×900) **y** móvil vertical (390×844). El cliente lo abre por WhatsApp.
- [ ] La imagen no tiene texto inventado (mirala con Read, no confíes en el prompt).
- [ ] Ninguna imagen sobre 200 KB en un deck HTML; el .pptx entero bajo 5 MB.
- [ ] Contraste: el texto sobre `hero` se lee sin forzar la vista.
- [ ] Fotos de personas: que no parezcan banco de imágenes de 2010.

**macOS**
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --window-size=1600,900 --virtual-time-budget=4500 \
  --screenshot=desk.png "file:///ruta/deck.html#s5"
```

**Windows (PowerShell)**
```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --disable-gpu `
  --window-size=1600,900 --virtual-time-budget=4500 `
  --screenshot=desk.png "file:///C:/ruta/deck.html#s5"
```

Si el comando no funciona, sirve igual abrir el deck en Chrome y usar las DevTools
(F12 → icono de celular) para ver cómo queda en móvil.

## Anti-patrones

| Anti-patrón | Por qué falla | Fix |
|---|---|---|
| Meter la imagen en un slide de métricas | La lámina no crece: se corta por abajo | `--pattern full` |
| `split` en un slide con dos cards | Al pasar a media columna se apilan y desbordan | `--pattern full` |
| Dejar que el modelo escriba texto en la imagen | Escribe con faltas y en el idioma equivocado | Las guardas ya lo prohíben; no las quites |
| Foto de stock genérica en cada slide | Ruido, no comunica | Máximo 2-3 imágenes por deck, cada una con un motivo |
| PNG de 1.7 MB dentro del PPTX | Archivo que no se puede mandar por correo | El script ya usa JPEG para PPTX |
| Texto sobre foto sin overlay | Ilegible en proyector | `hero` ya trae overlay navy; no lo bajes de 60% |
| Imagen decorativa en un reporte de datos | Le quita seriedad al número | Si el slide es de datos, que la imagen sea diagrama (`pizarra`), no foto |

## Referencias

- [`references/prompt-recipes.md`](references/prompt-recipes.md) — recetas por tipo de visual y cómo derivar el prompt del contenido del slide
- [`references/patrones-html.md`](references/patrones-html.md) — el markup y el CSS de cada patrón, para pegarlo a mano
- [`scripts/slide_image.py`](scripts/slide_image.py) — generador + insertador

## Skills hermanas

- [`gravity-deck`](../gravity-deck/) — el deck HTML
- [`gravity-pptx`](../gravity-pptx/) — el PPTX editable (layout `image`)
- [`image-generation`](../image-generation/) — imagen suelta, sin deck de por medio
- [`pizarra`](../pizarra/) — sketchnote como archivo aparte, con más control del estilo
