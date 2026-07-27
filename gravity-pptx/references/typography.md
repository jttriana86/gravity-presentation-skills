# Tipografía — Gravity (PPTX edition)

Misma jerarquía que `gravity-deck`. Diferencia: PowerPoint **no carga Google Fonts**, depende de fuentes instaladas en la máquina del usuario final.

## Estrategia de fuentes

```python
FONT_HEADING = "Montserrat"   # Fallback automático: Calibri/Arial
FONT_BODY    = "Open Sans"    # Fallback automático: Calibri/Arial
```

**Si la máquina del cliente NO tiene Montserrat/Open Sans:**
- PowerPoint sustituye automáticamente por Calibri (Office default)
- El deck sigue viéndose profesional, solo menos tipográficamente fiel
- No es un error, es un comportamiento aceptable

**Para fidelidad máxima:** mandar al cliente las fuentes (gratis, Google Fonts) o exportar a PDF antes de mandar.

## Instalar Montserrat + Open Sans (recomendado para que tu máquina genere bien)

### Windows
1. https://fonts.google.com/specimen/Montserrat → "Download family"
2. https://fonts.google.com/specimen/Open+Sans → "Download family"
3. Descomprimir, seleccionar todos los `.ttf` → click derecho → "Instalar"

### Mac
```bash
brew install --cask font-montserrat font-open-sans
```

## Jerarquía PPTX

| Elemento | Fuente | Tamaño (pt) | Bold | Color | Uso |
|----------|--------|-------------|------|-------|-----|
| **Cover title** | Montserrat | 96 | 900 (Black) | `#FFFFFF` | Portada/cierre |
| **Slide title** | Montserrat | 56 | 900 | `#051367` | Título de slide normal |
| **Section number** | Montserrat | 240 | 900 | Outline blanco | Divisor de sección (texto grande) |
| **Section title** | Montserrat | 64 | 900 | `#FFFFFF` | Divisor título |
| **Subtitle** | Montserrat | 24 | 800 (ExtraBold) | `#051367` o `#FFFFFF` | Subtítulo principal |
| **Eyebrow** | Montserrat | 12 | 800 | `#004714` | Kicker arriba del título |
| **Hero metric** | Montserrat | 64 | 900 | `#004714` | +150%, +10.4%, etc. |
| **Stat value** | Montserrat | 28 | 900 | `#000000` | Cifras secundarias |
| **Stat label** | Open Sans | 12 | 400 | `#666666` | Caption debajo de cifra |
| **Body** | Open Sans | 16 | 400 | `#000000` | Párrafos |
| **Insight italic** | Open Sans | 14 | 400 italic | `#000000` | Insight footer |
| **Quote** | Open Sans | 56 | 400 italic | `#051367` | Citas grandes |
| **Brand mark** | Montserrat | 14 | 900 | `#051367` | Logo/nombre marca esquina |
| **Page num** | Montserrat | 11 | 800 | `#666666` | Paginación esquina |

## Letter spacing en PPTX

PPTX no tiene `letter-spacing` directo como CSS. Aproximación:

```python
from pptx.util import Pt

# En python-pptx, espaciado entre caracteres se llama "spc" (XML attribute)
# Para tracking expandido (eyebrows, brand-mark), usar caps + ESPACIO entre palabras
# o setear via XML directo:

from pptx.oxml.ns import qn
def set_letter_spacing(run, points_x100):
    """spc value en unidades de 1/100 de point"""
    rPr = run._r.get_or_add_rPr()
    rPr.set('spc', str(points_x100))

# Uso:
set_letter_spacing(eyebrow_run, 400)  # +4pt tracking (uppercase eyebrow)
set_letter_spacing(title_run, -150)   # -1.5pt tracking (titular grande)
```

## Reglas duras

1. **Solo Montserrat + Open Sans.** Nunca Calibri salvo como fallback automático del cliente.
2. **Black para hero metrics.** Siempre 900 weight para números grandes.
3. **Italic solo en insights y citas.** Nunca en datos numéricos.
4. **Uppercase con espaciado expandido** en eyebrows + brand-marks.
5. **Tracking ajustado en titulares grandes** (titles 56pt+): -1 a -2pt.
6. **Line-height ajustado en títulos** (`paragraph.line_spacing = 0.95` para 50pt+).

## Anti-patrones

| ❌ Anti-patrón | Por qué falla | ✅ Fix |
|---------------|---------------|--------|
| Cambiar fuente del slide layout | Inconsistencia, difícil rollback | Setear fuente por run en cada text frame |
| Olvidar bold en hero metrics | Pierde presencia | Siempre `font.bold = True` para Montserrat Black |
| Usar Cambria, Times New Roman | No on-brand | Solo Montserrat + Open Sans |
| Letter-spacing default en eyebrows | Ilegible en mayúsculas | Setear `spc=400` mínimo |
| Auto-fit text en titulares | Reescala tamaños inconsistentemente | Setear tamaño explícito + revisar overflow manual |
