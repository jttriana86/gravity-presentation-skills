# Slide Types — Gravity PPTX

5 tipos de slide soportados. Cada uno se invoca desde el JSON spec con `"type": "..."`.

---

## §1 — `cover` (Portada / Cierre)

**Cuándo:** primera slide, slide de cierre.

**Schema JSON:**
```json
{
  "type": "cover",
  "eyebrow": "INFORME ORGÁNICO",
  "title": "Agosto 2025",
  "subtitle": "Reporte de crecimiento mensual · redes sociales",
  "footer_logo": "[LOGO CLIENTE]",
  "footer_meta": "PRESENTADO POR GRAVITY"
}
```

**Look generado:**
- Fondo: navy `#051367` sólido full-bleed
- Esquina sup-izq: dot rojo `#E70039` 10pt + brand name blanco
- Centro: eyebrow verde claro (uppercase, +4pt tracking) → título Montserrat Black 96pt blanco → subtítulo italic 20pt
- Esquina inf-izq: logo cliente | esquina inf-der: meta "PRESENTADO POR..."

---

## §2 — `divider` (Divisor de sección)

**Cuándo:** entre capítulos del deck.

**Schema JSON:**
```json
{
  "type": "divider",
  "number": "02",
  "title": "Crecimiento orgánico",
  "subtitle": "Seguidores, alcance y nuevas conexiones"
}
```

**Look generado:**
- Fondo: navy `#051367` sólido
- Esquina sup-izq: dot + brand name
- Centro vertical: número outline gigante (240pt, transparente con stroke blanco 30%) → título 64pt Black → subtítulo italic 20pt

---

## §3 — `metrics` (Datos / KPIs)

**Cuándo:** mostrar métricas, %, comparar plataformas, reportes mensuales.

**Schema JSON:**
```json
{
  "type": "metrics",
  "eyebrow": "SEGUIDORES",
  "title": "Crecimiento mensual",
  "subtitle": "Activaciones presenciales como motor digital.",
  "cards": [
    {
      "platform": "FACEBOOK",
      "icon": "f",
      "metric": "+150%",
      "metric_label": "CRECIMIENTO MES",
      "stats": [
        {"value": "2.262", "label": "Total seguidores"},
        {"value": "5", "label": "Nuevos en agosto"}
      ]
    },
    {
      "platform": "INSTAGRAM",
      "icon": "IG",
      "metric": "+10,4%",
      "metric_label": "CRECIMIENTO MES",
      "stats": [
        {"value": "12.515", "label": "Total seguidores"},
        {"value": "170", "label": "Nuevos en agosto"}
      ]
    }
  ],
  "insight": "Los picos coincidieron con **fechas clave fuera del entorno digital**."
}
```

**Look generado:**
- Fondo: blanco
- Header (top): brand-mark izq + meta uppercase der
- Title block: eyebrow verde → título navy 56pt Black → subtítulo italic gris
- Cards (grid 1/2): rounded rectangle blanco con sombra suave + border-top navy 3pt
  - Header: platform name (Montserrat Black) + icono navy
  - Hero: arrow ▲ + métrica verde 64pt + label uppercase
  - Divider gris fino
  - Stats row 2 columnas
- Footer: tag navy "INSIGHT" + texto italic
- Esquina inf-der: paginación

**Soporta 1, 2 o 3 cards.** Si hay 3, grid se reorganiza a 1/3 cada una.

---

## §4 — `body` (Cuerpo / Análisis)

**Cuándo:** explicaciones, análisis de tendencias, contexto.

**Schema JSON:**
```json
{
  "type": "body",
  "eyebrow": "CONTEXTO",
  "title": "Por qué subió Facebook tanto este mes.",
  "intro": "El crecimiento de **+150%** respondió a tres factores combinados:",
  "bullets": [
    {
      "number": "01",
      "title": "Activación presencial en Corponovo Fest",
      "description": "3 días con QR de seguimiento en escenarios."
    },
    {
      "number": "02",
      "title": "Contenido tipo carrusel de aliados",
      "description": "Tags cruzados generaron alcance orgánico extendido."
    },
    {
      "number": "03",
      "title": "Algoritmo Meta favoreciendo contenido local",
      "description": "Cambio en el ranking visto desde mediados de agosto."
    }
  ]
}
```

**Look generado:**
- Fondo: blanco
- Header común
- Layout 2 columnas:
  - **Izquierda (40%):** eyebrow + título grande izq-aligned
  - **Derecha (60%):** intro párrafo + bullets numerados (número en círculo navy + título + descripción)

---

## §5 — `quote` (Cita / Punchline)

**Cuándo:** frases emblemáticas, hooks, cierres.

**Schema JSON:**
```json
{
  "type": "quote",
  "text": "Lo presencial no compite con lo digital. Lo alimenta.",
  "highlight": "Lo alimenta",
  "author": "Insight Gravity",
  "role": "Análisis estratégico Q3 2025"
}
```

**Look generado:**
- Fondo: blanco
- Header común
- Centro: cita Open Sans Italic 56pt navy, con `highlight` en bold (no italic)
- Debajo: autor Montserrat ExtraBold + role italic gris

---

## §6 — `image` (Pizarra / Diagrama)

**Cuándo:** insertar una imagen grande (sketchnote, pizarra, diagrama exportado) con título compacto que maximiza el área visual.

**Schema JSON:**
```json
{
  "type": "image",
  "meta": "DIAGRAMA",
  "eyebrow": "CÓMO FUNCIONA",
  "title": "El flujo de extremo a extremo.",
  "image": "assets/flujo.png",
  "caption": "Esquema simplificado del proceso."
}
```

**Look generado:**
- Fondo: blanco, header común
- Título compacto (32pt) para dejar máximo espacio a la imagen
- Imagen centrada con fit que preserva aspect-ratio (requiere Pillow; si falta, hace fallback)
- `caption` opcional italic gris centrado al pie
- Ruta `image` relativa al JSON o absoluta

---

## §7 — `sitemap` (Mapa del sitio / Arquitectura IA)

**Cuándo:** mostrar la arquitectura de información de un sitio — secciones, sub-secciones y páginas. Replica un diagrama de sitemap con marca Gravity.

**Schema JSON:**
```json
{
  "type": "sitemap",
  "meta": "ARQUITECTURA",
  "eyebrow": "ESTRUCTURA DEL SITIO",
  "title": "Mapa del sitio.",
  "columns": [
    {
      "title": "Home",
      "footer": true,
      "pages": ["Banner Promo / Marca", "Grid de productos (CTA)", "Socios comerciales"]
    },
    {
      "title": "Institucional",
      "span": 2,
      "subcolumns": [
        { "title": "La empresa", "footer": true, "pages": ["Banner + Descripción", "Video"] },
        { "title": "Política integral", "footer": true, "pages": ["Visión", "Misión"] }
      ]
    },
    {
      "title": "Novedades",
      "footer": true,
      "pages": ["Grid de Noticias", {"text": "Detalle novedades", "highlight": true}]
    }
  ]
}
```

**Estructura de `columns`:**
- Columna simple: `title` + `pages` (+ `footer` opcional).
- Columna dividida: `title` + `span` (nº de slots que ocupa) + `subcolumns`, cada sub-columna con su `title`, `pages` y `footer`.
- `pages`: string, o `{ "text": "...", "highlight": true }` para resaltar una página (pill navy con texto blanco, ej. estado seleccionado).
- `footer: true` agrega una pill gris "Footer" al final de esa columna/sub-columna.

**Look generado:**
- Fondo: blanco, header común, título 30pt navy
- Header de sección: chip navy (Montserrat bold, blanco) que abarca su `span`
- Sub-sección: chip gris-azul (#8A96A3) bajo el header
- Páginas: pills blancas con borde sutil + texto navy; altura variable según wrap del texto
- Footer: pill gris-azul "Footer"
- El ancho se reparte en slots iguales (suma de `span`); las columnas simples empiezan sus pills a la altura de los sub-headers

**Notas:**
- Diseñado para ~6 secciones top-level (8-9 slots). Más de eso aprieta el texto.
- Si una columna tiene muchas páginas (7+), las pills pueden acercarse al borde inferior; reducir páginas o usar texto más corto.

---

## Reglas universales (TODAS las slides)

1. ✅ **Dot rojo sello** en esquina sup-izq de TODA slide
2. ✅ **Brand name** del cliente al lado del dot
3. ✅ **Page num** en esquina inf-der (formato `XX / NN`)
4. ✅ **Aspect ratio 16:9** (`Inches(13.333) x Inches(7.5)`)
5. ✅ **Padding interno mínimo** ~10% (eqv. 1 inch en horizontal, 0.6in vertical)

## Combinaciones recomendadas (deck de 8 slides estándar)

```
01 — cover         (portada)
02 — divider       (sección 1: contexto)
03 — metrics       (KPIs principales)
04 — body          (análisis)
05 — divider       (sección 2: insights)
06 — body          (causas / hallazgos)
07 — quote         (insight clave)
08 — cover         (cierre con CTA)
```

## Markdown soportado en strings de texto

- `**texto**` → bold (Montserrat ExtraBold) en color navy `#051367`
- Otros (italic, links, etc.) → texto plano

Solo aplica a campos de tipo párrafo (`insight`, `intro`, `description`). No aplica a títulos/labels.
