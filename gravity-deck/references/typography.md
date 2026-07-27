# Tipografía — Gravity

Sistema dual estricto: **Montserrat** (titulares) + **Open Sans** (cuerpo). Nada más.

## Import (Google Fonts)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800;900&family=Open+Sans:ital,wght@0,400;0,700;0,800;1,400&display=swap" rel="stylesheet">
```

Fallback: `Arial, sans-serif`.

## Familia Montserrat — Titulares y números hero

| Variante | Peso | Uso |
|----------|------|-----|
| **Montserrat Black** | 900 | Titulares grandes, números destacados (+150%, hero metrics) |
| **Montserrat ExtraBold** | 800 | Subtítulos, callouts, tags, brand-name |
| **Montserrat SemiBold** | 700 | Encabezados secundarios, cards-platform |
| **Montserrat Regular/Medium** | 400-500 | Encabezados terciarios (raro, casi no usar) |

## Familia Open Sans — Cuerpo y descripciones

| Variante | Peso | Uso |
|----------|------|-----|
| **Open Sans ExtraBold** | 800 | Énfasis dentro del cuerpo, etiquetas, stat-labels |
| **Open Sans Regular** | 400 | Párrafos, listas, descripciones, captions |
| **Open Sans Italic** | 400 italic | Subtítulos editoriales, citas, insights |

## Jerarquía recomendada

| Elemento | Fuente | Tamaño | Color | Tracking |
|----------|--------|--------|-------|----------|
| **Título de portada** | Montserrat Black | 80-96 pt | `#FFFFFF` (sobre navy) o `#051367` | -2px |
| **Título de slide** | Montserrat Black | 56-64 pt | `#051367` | -1.5px |
| **Subtítulo / sección** | Montserrat ExtraBold | 20-24 pt | `#051367` | normal |
| **Eyebrow / kicker** | Montserrat ExtraBold | 11-12 pt | `#004714` o `#051367` | +4px (uppercase) |
| **Hero metric** | Montserrat Black | 56-72 pt | `#004714` (positivo) o `#051367` | -2px, `tnum` |
| **Stat value** | Montserrat Black | 24-32 pt | `#000000` o `#051367` | normal, `tnum` |
| **Body / cuerpo** | Open Sans Regular | 14-16 pt | `#000000` | normal |
| **Stat label** | Open Sans Regular | 11-12 pt | `#666666` | normal |
| **Caption / footer** | Open Sans Regular | 10-12 pt | `#666666` | normal |
| **Insight / cita** | Open Sans Italic | 14-17 pt | `#000000` con strong navy | normal |
| **Brand mark** | Montserrat Black | 14 pt | `#051367` | +3px (uppercase) |

## Tabular numbers (NÚMEROS)

Para que las cifras alineen verticalmente en métricas y reportes:

```css
.metric-pct, .stat-value {
  font-feature-settings: 'tnum';
}
```

Aplica a TODOS los números en métricas. Sin esto, "12.515" y "2.262" no alinean visualmente.

## Reglas duras

1. **Solo 2 fuentes** — Montserrat + Open Sans. Nunca mezclar con Inter, Poppins, Roboto, otras.
2. **Black para hero** — números grandes (+150%, $25K, 2.262) siempre Montserrat Black.
3. **Italic solo en insights** — citas, observaciones, subtítulos editoriales. Nunca en datos.
4. **Tracking ajustado en titulares grandes** — `letter-spacing: -1px a -2px` para títulos 56pt+. Ayuda a verse compacto y premium.
5. **Tracking expandido en eyebrows** — `letter-spacing: +3px a +4px` + uppercase para kickers/labels chicas. Da feel editorial.
6. **Uppercase con moderación** — solo en eyebrows, brand-marks, stat-labels. Nunca en cuerpo.
7. **Line-height ajustado en titulares** — `line-height: 0.95` para títulos 50pt+. Sin esto se ven flotantes.

## Anti-patrones tipográficos

| ❌ Anti-patrón | Por qué falla | ✅ Fix |
|---------------|---------------|--------|
| Todo Montserrat (sin Open Sans) | Visual pesado, agresivo | Cuerpo en Open Sans, jerarquía clara |
| Todo Open Sans (sin Montserrat) | Plano, sin presencia | Titulares en Montserrat Black |
| Mezclar 3+ fuentes | Inconsistencia marca | Solo 2 |
| Italic en cifras | Disminuye legibilidad numérica | Italic solo en texto, números siempre rectos |
| Black en cuerpo (no hero) | Imposible de leer en bloque | Cuerpo siempre Regular |
| Tracking apretado en eyebrow chica | Ilegible | Tracking +3-4px + uppercase |
| Sin `tnum` en datos | Números bailan, se ven amateur | `font-feature-settings: 'tnum'` siempre en métricas |
