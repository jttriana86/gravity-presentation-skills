# Brand Palette — Gravity

## Paleta principal (uso frecuente)

| Rol | HEX | Uso |
|-----|-----|-----|
| **Primario / marca** | `#051367` | Títulos principales, bloques de marca, cards top-border, fondos de portada/divisor |
| **Negro** | `#000000` | Texto base sobre fondos claros, números secundarios |
| **Blanco** | `#FFFFFF` | Fondos limpios, texto sobre navy |

## Paleta secundaria (apoyo)

| Rol | HEX | Uso |
|-----|-----|-----|
| **Verde bosque** | `#004714` | EXCLUSIVO datos positivos (% crecimiento, métricas favorables, checks) |
| **Gris medio** | `#666666` | Texto secundario, captions, labels, divisores |
| **Azul rey (variante primario)** | `#071689` | Variante del primario, uso moderado en hover/secondary buttons |

## Acento crítico

| Rol | HEX | Uso |
|-----|-----|-----|
| **Rojo carmín** | `#E70039` | SOLO énfasis crítico — dot esquina sello + alertas. Máx 1 uso visible por slide. |

## Tonos derivados (para UI fina)

| Rol | HEX | Uso |
|-----|-----|-----|
| **Background suave** | `#F8F9FB` | Hover states, fondos alternativos sutiles |
| **Borde sutil** | `rgba(5, 19, 103, 0.08)` | Bordes de cards (1px), divisores secundarios |
| **Gris suave** | `#E5E7EB` | Divisores horizontales |
| **Sombra navy** | `rgba(5, 19, 103, 0.18)` | Box-shadow de cards (24px difusa) |

## Regla 60/30/10 (no negociable)

```
60% — Blanco #FFFFFF (fondos) + Negro #000000 (texto base)
30% — Navy #051367 (titulares, bloques marca, cards top-border)
10% — Verde #004714 + Gris #666666 + Rojo #E70039 (acentos puntuales)
```

**Validación visual:** si miras una slide y predomina el navy o el verde, está mal. Debe predominar el blanco.

## Combinaciones recomendadas

| Fondo | Texto principal | Acento permitido |
|-------|-----------------|------------------|
| `#FFFFFF` | `#000000` o `#051367` | `#004714` (positivo) o `#E70039` (crítico) |
| `#051367` | `#FFFFFF` | `#FFFFFF` con peso ExtraBold |
| `#FFFFFF` | `#051367` (titular) + `#666666` (cuerpo) | `#E70039` puntual |

## Variables CSS (copiar en deck.html)

```css
:root {
  /* Brand */
  --primary:        #051367;
  --primary-2:      #071689;
  --black:          #000000;
  --white:          #FFFFFF;

  /* Accents */
  --green:          #004714;
  --gray:           #666666;
  --red-alert:      #E70039;

  /* Derived */
  --bg-soft:        #F8F9FB;
  --gray-soft:      #E5E7EB;
  --card-border:    rgba(5, 19, 103, 0.08);
  --shadow-navy:    rgba(5, 19, 103, 0.18);

  /* Shadows pre-built */
  --shadow-card:
    0 1px 0 rgba(255,255,255,1) inset,
    0 2px 4px rgba(5, 19, 103, 0.06),
    0 24px 48px -16px var(--shadow-navy);
}
```

## Anti-patrones de color

| ❌ Prohibido | Por qué | ✅ En su lugar |
|-------------|---------|---------------|
| `#4285F4` (azul Google) | Genérico tech, rompe marca | `#051367` |
| `#FFAB40` (naranja) | No está en paleta | Sin equivalente — pedir confirmación |
| Verde para datos negativos | Confunde semántica | Negro o gris |
| Rojo para más de 1 elemento por slide | Pierde énfasis | Limitar a alertas |
| Gradientes coloridos | No son brand-on | Solo gradientes white→#F8F9FB sutiles |
