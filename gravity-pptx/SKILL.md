---
name: gravity-pptx
description: Genera archivos PowerPoint (.pptx) profesionales en estilo Gravity (agencia) con misma paleta navy + verde + Montserrat/Open Sans que la skill gravity-deck. Usar cuando el cliente requiera PPTX editable (no HTML) — reportes mensuales, propuestas que el cliente debe modificar, decks para gente que solo usa PowerPoint, presentaciones para imprimir. Triggers "haz un pptx", "deck en powerpoint", "presentación editable", "PPT estilo Gravity", "genera el .pptx", "exporta a powerpoint".
---

# Gravity PPTX — Generador de presentaciones PowerPoint editables

Hermana de `gravity-deck` (HTML). Misma marca, mismo diseño, pero output `.pptx` editable.

## Cuándo usar gravity-pptx vs gravity-deck

| Situación | Skill |
|---|---|
| Cliente debe editar el deck después | **gravity-pptx** |
| Reporte mensual recurrente | **gravity-pptx** (más fácil de cambiar números a mano) |
| Presentación para imprimir | **gravity-pptx** |
| Cliente solo usa PowerPoint | **gravity-pptx** |
| Pitch a cliente importante donde TÚ presentás | **gravity-deck** (HTML, más wow) |
| Manifesto / lanzamiento | **gravity-deck** (animaciones) |
| Propuesta confidencial con password gate | **gravity-deck** |
| Deck para subir a web con URL | **gravity-deck** |
| Cliente pide AMBOS | Generar **gravity-deck** primero, después **gravity-pptx** del mismo contenido |

## Filosofía heredada de gravity-deck (no negociable)

Mantenemos las mismas reglas que la skill HTML:

1. **Light-dominant siempre** — fondo blanco 60%, navy 30%, acentos 10%
2. **Verde solo para datos positivos** (`#004714`)
3. **Rojo solo crítico** (`#E70039`) — máx 1 uso por slide
4. **Tipografía dura**: Montserrat (titulares) + Open Sans (cuerpo). Fallback Calibri.
5. **Dot rojo sello** en TODA slide (esquina superior izquierda)
6. **Aspect-ratio 16:9** (`Presentation()` con `slide_width=Inches(13.333), slide_height=Inches(7.5)`)
7. **Cards con bezel sutil** — rounded rectangle blanco + sombra suave + border-top navy 3pt
8. **Centrado vertical SIEMPRE** — el bloque de contenido (título + cards/bullets) se centra verticalmente en el slide vía `centered_start()`, NO se ancla arriba dejando hueco abajo. Header (marca + meta) arriba y page-num abajo quedan fijos; el contenido va al medio entre `CONTENT_TOP` y `CONTENT_BOTTOM`.
9. **Logo oficial Gravity SIEMPRE presente** — portada y/o cierre llevan el logo oficial de la agencia (nunca "GRAVITY" como texto ni recreado). Ver §Logo oficial Gravity.

## Logo oficial Gravity

Meter SIEMPRE el logo oficial. Dos variantes según el fondo del slide:

| Variante | Cuándo | URL |
|----------|--------|-----|
| **Color (azul)** | Slides de fondo claro/blanco (metrics, body, quote, footer) | `https://gravity.com.co/wp-content/uploads/2022/07/GV-AZUL_1.svg` |
| **Blanco** | Slides de fondo navy (cover, divider) | `https://gravity.com.co/wp-content/uploads/2022/07/logo-blanco-gravity.svg` |

⚠️ `python-pptx` **no** inserta SVG: `add_picture()` necesita PNG/EMF. Descargar el SVG oficial y rasterizarlo a PNG a alta resolución (p.ej. `cairosvg` o `rsvg-convert`, ~600px de ancho) una sola vez, guardarlo en `assets/`, y usar ese PNG. No deformar (fijar solo `height`/`width` manteniendo proporción), no recolorear.

## Limitaciones honestas vs HTML

PowerPoint es menos flexible que CSS. **Cosas que NO podemos replicar 1:1:**

| Feature en HTML | Equivalente en PPTX |
|---|---|
| 4 box-shadows recipe (bezel real) | Shape con shadow effect (más simple) |
| Animaciones CSS (entrance, stagger, counter) | Animaciones nativas PPT (limitadas) — opcional |
| Hover states | No existe en PPT |
| Gradientes complejos | Gradientes lineales solamente |
| Custom JS (password gate, nav teclado) | No aplica |
| Google Fonts auto-cargadas | Cliente debe tener fuente instalada o ver fallback |

**Conclusión:** PPTX se ve **90% igual** que HTML — pero el 10% restante es lo "wow factor". Si el caso de uso requiere wow, usar `gravity-deck` HTML. Si requiere editabilidad, usar `gravity-pptx`.

## Pipeline de generación

### Paso 1 — Recolectar datos del usuario

- Cliente / marca
- Periodo / tema
- Contenido por slide (puede ser JSON o texto libre)
- Logo del cliente (path opcional)

### Paso 2 — Crear o adaptar el JSON spec

Spec format en [`examples/corponovo-agosto.json`](examples/corponovo-agosto.json):

```json
{
  "client": "Corponovo",
  "title": "Informe orgánico agosto 2025",
  "presenter": "Gravity",
  "slides": [
    { "type": "cover", "eyebrow": "...", "title": "...", "subtitle": "..." },
    { "type": "metrics", "eyebrow": "...", "title": "...", "subtitle": "...",
      "cards": [
        { "platform": "FACEBOOK", "metric": "+150%", "label": "CRECIMIENTO MES",
          "stats": [{"value": "2.262", "label": "Total seguidores"}, ...] }
      ],
      "insight": "Texto del insight con **strong** opcional." },
    { "type": "divider", "number": "02", "title": "...", "subtitle": "..." },
    { "type": "body", "eyebrow": "...", "title": "...", "bullets": [...] },
    { "type": "quote", "text": "...", "highlight": "...", "author": "...", "role": "..." }
  ]
}
```

### Paso 3 — Generar el .pptx

```powershell
python scripts/build_deck.py examples/corponovo-agosto.json output/corponovo-agosto-2025.pptx
```

Output: archivo `.pptx` listo para abrir en PowerPoint, Keynote, o LibreOffice Impress.

### Paso 4 — Validar

1. Abrir el .pptx en PowerPoint
2. Verificar que todas las slides cargaron
3. Si las fuentes Montserrat/Open Sans no están instaladas, PPT sustituye automáticamente por Calibri (sigue viéndose pro, solo menos tipográficamente fiel)
4. Click derecho en cualquier elemento → "Editar" para confirmar editabilidad

## Tipos de slides soportados (7)

| Type | Función Python | Look |
|------|---------------|------|
| `cover` | `cover_slide()` | Fondo navy + título Black 96pt blanco |
| `divider` | `divider_slide()` | Fondo navy + número outline gigante + título sección |
| `metrics` | `metrics_slide()` | Fondo blanco + 2 cards bezel + métrica hero verde + insight footer |
| `body` | `body_slide()` | Fondo blanco + título 2 columnas + bullets numerados |
| `quote` | `quote_slide()` | Fondo blanco + cita gigante italic + autor |
| `image` | `image_slide()` | Fondo blanco + título compacto + imagen grande centrada (pizarra/diagrama) |
| `sitemap` | `sitemap_slide()` | Fondo blanco + mapa de sitio: headers navy por sección, sub-columnas, pills de páginas + Footer |

## Anti-patrones (heredados + específicos PPTX)

| Anti-patrón | Por qué falla | Fix |
|-------------|---------------|-----|
| Usar fuentes que no son Montserrat/Open Sans | Inconsistencia con marca | Solo esas + Calibri fallback |
| Verde en datos negativos | Confunde semántica | Verde = positivo, rojo = crítico |
| Rojo en más de 1 elemento por slide | Pierde énfasis | Limitar a sello + 1 alerta máx |
| **Shapes superpuestos sin orden Z** | PPTX corta lo que está atrás | Usar `slide.shapes` orden correcto |
| **Texto en placeholder de slide layout** | Difícil de editar después | Usar text boxes nuevos, no placeholders del layout |
| **Imágenes sin compress** | PPTX queda pesado | python-pptx no comprime auto, validar size final < 5 MB |
| **Más de 20 slides** | Cliente abre y se aburre | Decks Gravity óptimos: 8-12 slides |
| **Contenido pegado arriba con hueco abajo** | Se ve incompleto y desbalanceado | Centrar vertical con `centered_start()`; nunca anclar a Y fijo arriba |

## Convertir entre HTML y PPTX

**HTML → PPTX:** si ya generaste con `gravity-deck`, podés re-usar el JSON spec (cuando ambas skills lo soporten en futuro).

**PPTX → HTML:** no automático. Si querés ambos, generá los dos desde el mismo JSON spec.

## Referencias

- [`references/brand-palette.md`](references/brand-palette.md) — Paleta con valores RGB para python-pptx
- [`references/typography.md`](references/typography.md) — Fuentes + jerarquía PowerPoint
- [`references/slide-types.md`](references/slide-types.md) — Spec detallado de cada template
- [`scripts/build_deck.py`](scripts/build_deck.py) — Generador principal
- [`examples/corponovo-agosto.json`](examples/corponovo-agosto.json) — Ejemplo spec completo

## Sister skill

- [`gravity-deck`](../gravity-deck/) — Versión HTML con animaciones, password gate y deploy a Vercel.
