---
name: gravity-deck
description: Genera presentaciones HTML profesionales en estilo Gravity (agencia). Usar cuando el usuario pida un deck, presentación, slide, reporte mensual, pitch para cliente, manifesto, o mencione "estilo Gravity". Aplica paleta navy #051367 + verde #004714 + Montserrat/Open Sans con doble capa bezel sutil sobre fondo claro y animaciones de entrada por slide. Triggers: "hazme un deck", "presentación cliente", "reporte mensual", "pitch", "slide HTML", "estilo Gravity", "deck para agencia".
---

# Gravity Deck — Generador de presentaciones HTML para agencia

Sistema visual propio: light-dominant, premium, con efecto bezel sutil y animaciones suaves. Inspirado en filosofía Titaniumorphism pero adaptado a marca clara.

## Cuándo usar

| Usar | NO usar |
|------|---------|
| Pitch a cliente importante | Cuando el cliente debe editar el deck (mejor PPTX) |
| Reportes mensuales recurrentes | Colaboración en tiempo real con varias personas |
| Manifestos, lanzamientos, brand-forward | Hand-off rápido sin curva de aprendizaje |
| Demos en vivo en navegador | Decks de uso interno trivial |

## Filosofía (no negociable)

1. **Light-dominant siempre** — fondo blanco 60%, navy 30%, acentos 10%
2. **Bezel sutil light-mode** — cards con border-top navy 3px + sombra 24px difusa = sensación de pieza, sin oscurecer
3. **Verde solo para datos positivos** — crecimiento, éxito, métricas favorables
4. **Rojo `#E70039` solo crítico** — máximo 1 uso por slide, idealmente 1 por deck (alertas, énfasis vital)
5. **Tipografía dura: Montserrat + Open Sans** — nada más, nunca mezclar con otras
6. **Dot esquina como sello** — punto rojo 10px arriba-izq, sello de marca en TODA slide
7. **Aspect-ratio 16:9 estricto** — `aspect-ratio: 16/9` obligatorio en `.stage`
8. **Animaciones sutiles** — fade + translateY 20px on entrance, stagger 100ms en cards, nunca rebotes ni efectos chillones
9. **Centrado vertical SIEMPRE** — el contenido de cada slide se agrupa al medio (vertical). El `.slide` es `display:flex; flex-direction:column; justify-content:center`; header y page-num van `position:absolute`. NUNCA dejar un hueco grande en el centro con el título arriba y el contenido abajo. NUNCA poner `height:100%` en grids internos (`.body-grid`, `.cards-grid`, `.month-grid`…) — rompe el centrado; usar `width:100%` y dejar que el flex del slide centre.
10. **Logo oficial Gravity SIEMPRE presente** — toda presentación/reporte de Gravity lleva el logo oficial de la agencia (portada y/o cierre y/o footer). Usar los SVG oficiales, nunca escribir "GRAVITY" como texto ni recrear el logo. Ver §Logo oficial Gravity.
11. **Responsive obligatorio** — el cliente abre el deck en el celular. En móvil vertical la
    lámina se convierte en documento legible; al girar el teléfono vuelve a ser la lámina
    completa. **Ningún deck se entrega sin verificarlo.** Ver [`references/responsive.md`](references/responsive.md)

## Logo oficial Gravity

Meter SIEMPRE el logo oficial en las presentaciones de Gravity. Dos variantes según el fondo:

| Variante | Cuándo | URL |
|----------|--------|-----|
| **Color (azul)** | Sobre fondo claro/blanco (lo habitual: portada light, footer) | `https://gravity.com.co/wp-content/uploads/2022/07/GV-AZUL_1.svg` |
| **Blanco** | Sobre fondo navy/oscuro (divisores, header azul, overlays) | `https://gravity.com.co/wp-content/uploads/2022/07/logo-blanco-gravity.svg` |

```html
<!-- fondo claro -->
<img src="https://gravity.com.co/wp-content/uploads/2022/07/GV-AZUL_1.svg" alt="Gravity" style="height:28px">
<!-- fondo oscuro -->
<img src="https://gravity.com.co/wp-content/uploads/2022/07/logo-blanco-gravity.svg" alt="Gravity" style="height:28px">
```

En decks co-branded (cliente + Gravity): logo del **cliente** en el header, logo de **Gravity** en portada/cierre/footer — nunca omitir el de Gravity. Reglas: no deformar (fijar solo `height`, `width:auto`), no aplicar color/filtros, elegir la variante por contraste con el fondo.

## Logos de producto Gravity

Cuando el deck sea de un **producto** de Gravity (no de la agencia en general), usar su logo además del de Gravity.

| Producto | Logo | ⚠ Restricción |
|----------|------|---------------|
| **LeadPro** — agentes de IA de voz + WhatsApp | `https://gravity.com.co/wp-content/uploads/2026/05/logo-leadpro.png` | **Es BLANCO** con el punto rojo "AI" (PNG 414×123 con alfa). **Solo sobre fondo navy/oscuro** — sobre fondo blanco desaparece. |

```html
<!-- correcto: portada, divisores, cualquier fondo navy -->
<img src="https://gravity.com.co/wp-content/uploads/2026/05/logo-leadpro.png" alt="LeadPro" style="height:34px;width:auto">
```

**En slides de fondo blanco** (el 90% de un deck Gravity) NO uses el PNG: se pierde. Ahí va el
`brand-mark` de texto (`dot-sello` + `<span class="brand-name">LEADPRO</span>` en navy), que es
legible y mantiene el sello. Regla: **el logo donde hay fondo oscuro, el texto donde hay fondo claro.**

## Estructura de archivos por deck

```
proyectos/YYYY-MM-DD-cliente-tema/
├── deck.html              ← Archivo principal (multi-slide con nav teclado)
├── data.json              ← (opcional) datos para reportes mensuales
└── assets/
    ├── logo-cliente.svg
    └── imagenes/
```

## Decisión tree por tipo de slide

| Tipo de slide | Template a usar | Referencia |
|---------------|----------------|------------|
| **Portada / cierre** | `slide-cover` | `references/slide-templates.md` §1 |
| **Divisor de sección** | `slide-divider` | `references/slide-templates.md` §2 |
| **Datos / métricas** | `slide-metrics` | `references/slide-templates.md` §3 |
| **Cuerpo / análisis** | `slide-body` | `references/slide-templates.md` §4 |
| **Comparativa antes/después** | `slide-compare` | `references/slide-templates.md` §5 |
| **Cita / punchline** | `slide-quote` | `references/slide-templates.md` §6 |

## Pipeline de generación

### Paso 1 — Recolectar contexto del usuario

Antes de generar, asegurar:
- Cliente / marca del deck
- Tema y objetivo (pitch, reporte, manifesto, etc.)
- Cantidad aproximada de slides
- Datos a incluir (si es reporte)
- Logo del cliente (path o pedirlo)

Si falta info crítica, preguntar con `AskUserQuestion`.

### Paso 2 — Estructurar narrativa

Esquema típico de deck Gravity (8-12 slides):
1. Portada
2. Contexto / problema
3. Datos clave (1-3 slides métricas)
4. Análisis / insight
5. Recomendación
6. Cierre / CTA

### Paso 3 — Generar HTML

1. Copiar `references/deck-shell.html` como base (ya trae animaciones + nav teclado + barra progreso)
2. Reemplazar slides con templates de `slide-templates.md`
3. Inyectar paleta exacta de `references/brand-palette.md`
4. Validar tipografía de `references/typography.md`

### Paso 4 — Validar antes de entregar

```powershell
# Verificar paleta correcta (no debe haber colores fuera de spec)
Select-String -Path "deck.html" -Pattern "#[0-9A-Fa-f]{6}" | Select-Object -ExpandProperty Matches

# Verificar aspect-ratio 16:9
Select-String -Path "deck.html" -Pattern "aspect-ratio: 16"

# Verificar fuentes correctas
Select-String -Path "deck.html" -Pattern "Montserrat|Open Sans"
```

Checklist visual:
- [ ] Dot rojo presente en TODAS las slides
- [ ] Animación fade-in funciona (recargar página)
- [ ] Navegación con flechas ← → funciona
- [ ] Barra de progreso se actualiza
- [ ] Aspect-ratio 16:9 mantenido al cambiar tamaño de ventana
- [ ] Verde solo en datos positivos
- [ ] Rojo solo en alertas críticas (max 1 por deck)
- [ ] Logo oficial de Gravity presente (SVG oficial, variante correcta por fondo)

### Validación en móvil (OBLIGATORIA — no es opcional)

Revisar **la lámina más cargada del deck**, no la portada.

**A ojo:** Chrome → `F12` → icono de móvil (`Ctrl+Shift+M`) → **iPhone 14**, y rotar a horizontal.

**Con capturas:**

```bash
# macOS: CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# Linux: CH="google-chrome"
# Windows (PowerShell): $CH = "C:\Program Files\Google\Chrome\Application\chrome.exe"
D="file:///ruta/al/deck.html"
"$CH" --headless --disable-gpu --window-size=390,844  --virtual-time-budget=4500 --screenshot=movil.png "$D#s7"
"$CH" --headless --disable-gpu --window-size=844,390  --virtual-time-budget=4500 --screenshot=horiz.png "$D#s7"
"$CH" --headless --disable-gpu --window-size=1600,900 --virtual-time-budget=4500 --screenshot=desk.png  "$D#s7"
```

- [ ] Móvil vertical: nada cortado por el borde derecho, la cifra más grande se lee completa
- [ ] Móvil vertical: ninguna tabla desaparecida ni superpuesta (van en `.tbl-wrap`)
- [ ] Móvil horizontal: se ve la lámina entera, sin recortes
- [ ] Escritorio: nada cambió respecto a antes
- [ ] La barra táctil inferior aparece solo en móvil vertical

## Anti-patrones (PROHIBIDO)

| Anti-patrón | Por qué falla | Fix |
|-------------|--------------|-----|
| **Fondo oscuro tipo Titaniumorphism** | Rompe identidad light-dominant Gravity | Solo blanco/navy claro |
| **Mezclar otras fuentes** (Inter, Poppins, Roboto) | Inconsistencia con spec marca | Solo Montserrat + Open Sans |
| **Verde en datos negativos** | Confunde semántica color | Verde = positivo, rojo = crítico |
| **Más de 3 colores acento por slide** | Visual ruidoso | Máx 2 acentos + base |
| **Sombras agresivas** | Sensación cheap | Sombra 24px difusa, opacity 0.18 max |
| **Animaciones de rebote / spin** | Cheap, distrae | Solo fade + translateY suave |
| **Texto sobre imágenes sin overlay** | Ilegibilidad | Overlay navy 60% mínimo |
| **Más de 6 elementos por slide** | Sobrecarga | Regla 1 idea por slide |
| **Aspect-ratio libre** | Se rompe en proyectores | `aspect-ratio: 16/9` siempre |
| **Hueco vertical** (título arriba, contenido abajo) | Se ve incompleto y desbalanceado | `.slide` flex + `justify-content:center`; header/page-num absolute; sin `height:100%` en grids |
| **Entregar sin abrirlo en móvil** | El cliente lo abre por WhatsApp y ve texto cortado y tablas desaparecidas | Las 3 capturas de §Validación en móvil |
| **`@media` móvil arriba del `<style>`** | Misma especificidad: ganan las reglas base y el móvil sigue roto | El bloque móvil va **al final** |
| **Grid sin `min-width: 0` en los hijos** | Una tabla ancha estira la página y corta TODO el texto | `min-width: 0` en los items |
| **`grid-template-columns` inline en la slide** | El estilo inline le gana a la media query y las columnas se superponen | `!important` en el bloque móvil, o clases `.c2` / `.c3` |
| **Tabla suelta, sin envolver** | En móvil desborda la lámina | `<div class="tbl-wrap"><table class="tbl">…` |

## Deploy a URL temporal (clientes)

Para enviar el deck a un cliente con URL pública:

**Windows (PowerShell):**
```powershell
.\scripts\deploy.ps1 -DeckPath "C:\ruta\proyecto-cliente"
.\scripts\deploy.ps1 -DeckPath "C:\ruta\proyecto-cliente" -Pdf  # con PDF backup
.\scripts\deploy.ps1 -DeckPath "C:\ruta\proyecto" -Name "corponovo-agosto-2025"
```

**macOS / Linux (bash):**
```bash
./scripts/deploy.sh ~/ruta/proyecto-cliente
./scripts/deploy.sh ~/ruta/proyecto-cliente "" --pdf  # con PDF backup
./scripts/deploy.sh ~/ruta/proyecto corponovo-agosto-2025
```

URL final tipo: `https://corponovo-agosto-2025.vercel.app` (queda copiada al portapapeles).

**Primera vez:** Vercel pedirá login (GitHub/email). Una sola vez por máquina.

## Propuestas confidenciales (password gate)

Para decks con info sensible (precios, estrategia, NDA), copiar [`references/password-gate.html`](references/password-gate.html) al inicio del `<body>` del deck. Cambiar `CAMBIAR_ESTE_PASSWORD` y `CLIENT_NAME`.

> ⚠️ **Es protección básica.** Para seguridad real (NDA, financiero), usar Vercel Pro Password Protection ($20/mes) o servidor con auth real.

## Backup PDF (clientes que pidan PPT)

Algunos clientes legacy piden "el PPT". Genera PDF con la misma estructura visual:

**Windows:**
```powershell
.\scripts\export-pdf.ps1 -DeckPath "C:\ruta\proyecto"
```

**macOS / Linux:**
```bash
./scripts/export-pdf.sh ~/ruta/proyecto
```

Usa Edge/Chrome/Brave headless. PDF queda con todas las slides + paleta correcta (sin animaciones).

> **Si tu cliente necesita PPTX editable** (no solo PDF), usá la skill hermana [`gravity-pptx`](../gravity-pptx/) que genera `.pptx` real.

## Referencias

- [`references/responsive.md`](references/responsive.md) — **Móvil: CSS + JS + las 3 trampas + checklist**
- [`references/brand-palette.md`](references/brand-palette.md) — Paleta exacta + regla 60/30/10
- [`references/typography.md`](references/typography.md) — Jerarquía Montserrat + Open Sans
- [`references/slide-templates.md`](references/slide-templates.md) — 6 templates listos para copiar
- [`references/animations.md`](references/animations.md) — Animaciones permitidas (sutiles)
- [`references/deck-shell.html`](references/deck-shell.html) — Template base multi-slide listo para usar
- [`references/password-gate.html`](references/password-gate.html) — Snippet password protection opcional
- [`scripts/deploy.ps1`](scripts/deploy.ps1) — Deploy automatico a Vercel
- [`scripts/export-pdf.ps1`](scripts/export-pdf.ps1) — Export PDF backup
