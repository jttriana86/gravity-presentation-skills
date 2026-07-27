# Gravity Deck Skill

Skill nativa de [Claude Code](https://claude.com/claude-code) para generar presentaciones HTML profesionales en estilo Gravity (agencia).

> **Light-dominant, premium, con efecto bezel sutil y animaciones suaves.**
> Inspirado en filosofía Titaniumorphism pero adaptado a marca clara.

## Cómo instalar

### Opción A — Skill nativa de Claude Code (recomendado)

Copiar esta carpeta (`gravity-deck/`) dentro de la carpeta de skills de Claude Code:

**Windows:** `%USERPROFILE%\.claude\skills\gravity-deck`
**macOS / Linux:** `~/.claude/skills/gravity-deck`

En macOS / Linux, darle permiso de ejecución a los scripts:
```bash
chmod +x ~/.claude/skills/gravity-deck/scripts/*.sh
```

Ambas plataformas tienen scripts equivalentes:
- Windows: `deploy.ps1`, `export-pdf.ps1`
- Mac/Linux: `deploy.sh`, `export-pdf.sh`

Luego en cualquier proyecto invocás con triggers naturales:
- *"Hazme un deck Gravity para pitch del cliente X"*
- *"Necesito un reporte mensual estilo Gravity"*
- *"Slide en HTML con métricas de [datos]"*

### Opción B — Solo el deck HTML (sin Claude Code)

Si solo querés el template visual:
1. Abrí `references/deck-shell.html` en tu navegador
3. Editá los slides con tu contenido
4. Pantalla completa con `F`

## Estructura

```
gravity-deck/
├── SKILL.md                       # Orquestador + decision tree
├── README.md                      # Este archivo
└── references/
    ├── brand-palette.md           # Paleta + 60/30/10 + variables CSS
    ├── typography.md              # Montserrat + Open Sans + jerarquía
    ├── animations.md              # Animaciones permitidas
    ├── slide-templates.md         # 6 templates listos (cover, divider, metrics, body, compare, quote)
    └── deck-shell.html            # Template base funcional con nav teclado
```

## Sistema de marca

### Paleta (regla 60/30/10)

| Rol | HEX | Uso |
|-----|-----|-----|
| Primario | `#051367` | Navy — títulos, bloques marca |
| Verde positivo | `#004714` | Datos positivos, % crecimiento |
| Negro | `#000000` | Texto base |
| Blanco | `#FFFFFF` | Fondo dominante (60%) |
| Gris | `#666666` | Captions, secundarios |
| Rojo crítico | `#E70039` | Solo alertas, máx 1 por deck |

### Tipografía

- **Montserrat** (Black 900, ExtraBold 800) — titulares y números hero
- **Open Sans** (Regular 400, ExtraBold 800, Italic) — cuerpo y citas

### Animaciones (sutiles)

- Fade + translateY 24px on entrance
- Stagger 100ms entre elementos hermanos
- Easing `cubic-bezier(0.16, 1, 0.3, 1)` — ease-out exponencial
- Counter animation para métricas (números que cuentan desde 0)
- Hover lift -2px en cards
- Crossfade entre slides (sin slide horizontal cheap)
- Barra de progreso superior

### Navegación (deck-shell.html)

| Tecla | Acción |
|-------|--------|
| ← → | Slide anterior / siguiente |
| Espacio | Avanzar |
| F | Pantalla completa |
| Home / End | Primera / última slide |
| Click izq / der | Atrás / adelante |

## Templates incluidos

1. **cover** — Portada con fondo navy + título Black 96pt blanco
2. **divider** — Divisor de sección con número outline gigante
3. **metrics** — Cards bezel con KPIs y verde para % positivos
4. **body** — Análisis 2 columnas con bullets numerados
5. **compare** — Antes/Después con bezel diferenciado
6. **quote** — Punchline en italic gigante

## Filosofía

- Light-dominant siempre (60% blanco)
- Bezel sutil sin oscurecer (border-top navy 3px + sombra 24px)
- Tipografía dura: solo Montserrat + Open Sans
- Dot rojo esquina como sello en TODA slide
- Aspect-ratio 16:9 estricto

## Licencia

MIT — usalo, modificalo, compartilo.
