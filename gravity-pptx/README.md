# Gravity PPTX Skill

Skill nativa de [Claude Code](https://claude.com/claude-code) para generar presentaciones PowerPoint (`.pptx`) editables en estilo Gravity (agencia).

> **Hermana de `gravity-deck`.**
> Misma marca, misma paleta, misma jerarquía — pero output `.pptx` que el cliente puede editar.

## Cómo instalar

### Pre-requisitos

- **Python 3.10+** ([descargar](https://www.python.org/downloads/))
- **pip** (incluido con Python)

### Windows

```powershell
# Copiar la carpeta gravity-pptx\ a %USERPROFILE%\.claude\skills\gravity-pptx
# Luego instalar dependencias Python:
cd "$env:USERPROFILE\.claude\skills\gravity-pptx"
pip install -r requirements.txt
```

### macOS / Linux

```bash
# Copiar la carpeta gravity-pptx/ a ~/.claude/skills/gravity-pptx
# Luego instalar dependencias Python:
cd ~/.claude/skills/gravity-pptx
pip3 install -r requirements.txt
```

## Cómo usar

### Opción A — Desde Claude Code (recomendado)

En cualquier proyecto, decile a Claude:

> *"Hazme un PPTX en estilo Gravity para reporte mensual de Corponovo agosto 2025"*

Claude carga la skill, construye el JSON spec, ejecuta el script, te entrega el `.pptx`.

### Opción B — Desde terminal directo

```bash
# Editar examples/corponovo-agosto.json con tus datos
# Luego correr:
python scripts/build_deck.py examples/corponovo-agosto.json output/mi-deck.pptx
```

Output: archivo `.pptx` listo para abrir en PowerPoint, Keynote, Google Slides, o LibreOffice Impress.

## Cuándo usar gravity-pptx vs gravity-deck

| Situación | Skill |
|---|---|
| Cliente debe editar el deck | **gravity-pptx** |
| Reporte mensual recurrente | **gravity-pptx** |
| Presentación para imprimir | **gravity-pptx** |
| Cliente solo usa PowerPoint | **gravity-pptx** |
| Pitch importante donde TÚ presentás | **gravity-deck** (HTML, animaciones) |
| Manifesto / lanzamiento | **gravity-deck** |
| Propuesta confidencial con password | **gravity-deck** |

## Estructura

```
gravity-pptx/
├── SKILL.md                          # Orquestador + decision tree
├── README.md                         # Este archivo
├── requirements.txt                  # python-pptx, lxml
├── references/
│   ├── brand-palette.md              # Paleta con valores RGB
│   ├── typography.md                 # Fuentes + jerarquía
│   └── slide-types.md                # Spec detallado de cada template
├── scripts/
│   └── build_deck.py                 # Generador principal (Python)
└── examples/
    └── corponovo-agosto.json         # Ejemplo spec completo
```

## Tipos de slide soportados (5)

| Type | Look |
|------|------|
| `cover` | Fondo navy + título Black 96pt blanco + dot rojo sello |
| `divider` | Fondo navy + número outline gigante + título sección |
| `metrics` | Fondo blanco + cards con bezel + métrica hero verde + insight |
| `body` | Fondo blanco + título 2 columnas + bullets numerados |
| `quote` | Fondo blanco + cita italic gigante + autor |

## Sistema de marca

### Paleta (regla 60/30/10)

| Rol | HEX | RGB |
|-----|-----|-----|
| Primario | `#051367` | (5, 19, 103) |
| Verde positivo | `#004714` | (0, 71, 20) |
| Negro | `#000000` | (0, 0, 0) |
| Blanco | `#FFFFFF` | (255, 255, 255) |
| Gris | `#666666` | (102, 102, 102) |
| Rojo crítico | `#E70039` | (231, 0, 57) |

### Tipografía

- **Montserrat** (Black 900, ExtraBold 800) — titulares + números hero
- **Open Sans** (Regular 400, Italic) — cuerpo + citas
- **Fallback automático:** Calibri si no están instaladas

### Para fidelidad tipográfica máxima

Instalar Montserrat + Open Sans (gratis Google Fonts) en la máquina del cliente final.

**Mac:**
```bash
brew install --cask font-montserrat font-open-sans
```

**Windows:** descargar de [Google Fonts](https://fonts.google.com/) → click derecho `.ttf` → "Instalar"

## Limitaciones honestas vs HTML

PowerPoint es menos flexible que CSS. **Cosas que NO podemos replicar 1:1 vs gravity-deck HTML:**

- Animaciones CSS (entrance, stagger, counter)
- Hover states
- 4 box-shadows recipe (bezel real)
- Custom JS (password gate, navegación teclado)

PPTX queda **~90% igual** que HTML. Si necesitás el 10% restante de "wow", usá `gravity-deck`.

## JSON spec format

Ver ejemplo completo en [`examples/corponovo-agosto.json`](examples/corponovo-agosto.json).

```json
{
  "client": "Corponovo",
  "title": "...",
  "slides": [
    { "type": "cover", "eyebrow": "...", "title": "...", "subtitle": "..." },
    { "type": "metrics", "cards": [...], "insight": "..." },
    { "type": "body", "bullets": [...] },
    { "type": "quote", "text": "...", "highlight": "...", "author": "..." }
  ]
}
```

## Markdown soportado

- `**texto**` → bold navy en runs de párrafo (insight, intro, descripciones)

## Sister skill

- `gravity-deck` — Versión HTML con animaciones y deploy a Vercel (va en el mismo paquete)

## Licencia

MIT
