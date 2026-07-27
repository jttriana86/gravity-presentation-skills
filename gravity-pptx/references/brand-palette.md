# Brand Palette — Gravity (PPTX edition)

Misma paleta que `gravity-deck`, pero con valores RGB para uso con `python-pptx`.

## Paleta principal

| Rol | HEX | RGB | Constante Python |
|-----|-----|-----|------------------|
| Primario / marca | `#051367` | `(5, 19, 103)` | `PRIMARY` |
| Variante azul rey | `#071689` | `(7, 22, 137)` | `PRIMARY_2` |
| Negro | `#000000` | `(0, 0, 0)` | `BLACK` |
| Blanco | `#FFFFFF` | `(255, 255, 255)` | `WHITE` |
| Verde positivo | `#004714` | `(0, 71, 20)` | `GREEN` |
| Gris medio | `#666666` | `(102, 102, 102)` | `GRAY` |
| Rojo crítico | `#E70039` | `(231, 0, 57)` | `RED_ALERT` |
| Background suave | `#F8F9FB` | `(248, 249, 251)` | `BG_SOFT` |
| Gris suave | `#E5E7EB` | `(229, 231, 235)` | `GRAY_SOFT` |

## Uso en python-pptx

```python
from pptx.dml.color import RGBColor

PRIMARY    = RGBColor(0x05, 0x13, 0x67)
PRIMARY_2  = RGBColor(0x07, 0x16, 0x89)
BLACK      = RGBColor(0x00, 0x00, 0x00)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
GREEN      = RGBColor(0x00, 0x47, 0x14)
GRAY       = RGBColor(0x66, 0x66, 0x66)
RED_ALERT  = RGBColor(0xE7, 0x00, 0x39)
BG_SOFT    = RGBColor(0xF8, 0xF9, 0xFB)
GRAY_SOFT  = RGBColor(0xE5, 0xE7, 0xEB)

# Aplicar a fill de shape
shape.fill.solid()
shape.fill.fore_color.rgb = PRIMARY

# Aplicar a font color
run.font.color.rgb = WHITE
```

## Regla 60/30/10 (no negociable)

```
60% — Blanco fondos + Negro texto base
30% — Navy títulos, bloques marca, cards top-border
10% — Verde + Gris + Rojo (acentos puntuales)
```

Si un slide tiene más de 30% navy, está mal. Si tiene más de 10% combinando los tres acentos, está mal.

## Combinaciones recomendadas

| Fondo | Texto principal | Acento permitido |
|-------|-----------------|------------------|
| Blanco | Negro o Navy | Verde (positivo) o Rojo (crítico) |
| Navy | Blanco | Blanco con peso ExtraBold |
| Blanco | Navy título + Gris cuerpo | Rojo puntual |

## Anti-patrones de color

| ❌ Prohibido | Por qué | ✅ En su lugar |
|-------------|---------|---------------|
| Azul Office default `#1F497D` | Genérico, no marca | `#051367` |
| Verde Office `#9BBB59` | Cheap, no on-brand | `#004714` |
| Rojo Office `#C0504D` | Cheap | `#E70039` |
| Verde para datos negativos | Confunde semántica | Negro o gris |
| Más de 1 rojo por slide | Pierde énfasis | Limitar a sello + 1 alerta máx |
| Gradientes coloridos | No on-brand | Solo gradient white→#F8F9FB |
