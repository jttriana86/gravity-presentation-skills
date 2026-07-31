# Responsive — que el deck se vea en móvil

**Regla dura: ningún deck se entrega sin esto.** Los decks se comparten por WhatsApp y el
cliente los abre en el teléfono. Un deck 16:9 con tipografías en px se ve así en un móvil:
la lámina queda en una franja de 200px, el texto se corta y las tablas desaparecen bajo el
`overflow: hidden`.

## El modelo: híbrido

| Contexto | Comportamiento |
|---|---|
| **Escritorio** | Lámina 1280×720 escalada por JS para caber entera en la ventana |
| **Móvil / tablet en horizontal** | La misma lámina, escalada: se ve la diapositiva completa |
| **Móvil en vertical** | La lámina se convierte en documento: columnas apiladas, texto legible, scroll, barra táctil abajo y swipe |

El truco central es que la lámina tiene **tamaño lógico fijo** (1280×720) y se escala con
`transform: scale()`. Así el diseño nunca se rompe y no hay que tocar ni una tipografía.

## 1. CSS — sustituye la regla `.slide` y el bloque `:fullscreen`

```css
  /* Lámina de tamaño lógico fijo: el JS la escala para que quepa entera. */
  .slide {
    width: 1280px;
    height: 720px;
    background: var(--white);
    position: absolute;
    overflow: hidden;
    box-shadow: 0 40px 80px rgba(0,0,0,0.4);
    padding: 48px 60px 44px;
    opacity: 0; pointer-events: none;
    transition: opacity 400ms var(--ease-premium);
    display: grid;
    grid-template-rows: auto auto 1fr auto;
    transform: scale(var(--scale, 1));
    transform-origin: center center;
  }

  :fullscreen .deck, :-webkit-full-screen .deck { background: var(--white); }
  :fullscreen .slide, :-webkit-full-screen .slide { box-shadow: none; }
  :fullscreen .nav-hint, :-webkit-full-screen .nav-hint { display: none; }

  .mobile-nav { display: none; }
```

## 2. CSS — el bloque móvil (va **al final** del `<style>`, ver trampa #1)

```css
  /* ============================================================
     MÓVIL EN VERTICAL — la lámina se convierte en documento legible.
     Al girar el teléfono vuelve a ser la lámina 16:9 completa.
     ============================================================ */
  @media (max-width: 820px) and (orientation: portrait) {
    html, body { overflow: auto; height: auto; -webkit-text-size-adjust: 100%; }
    .deck { display: block; width: 100%; height: auto; }

    .slide {
      position: relative;
      width: 100%; height: auto; min-height: 100svh;
      padding: 26px 20px 96px;
      overflow: visible;
      box-shadow: none;
      transform: none !important;
      display: none;
      grid-template-rows: none !important;
      transition: none;
    }
    .slide.active { display: block; opacity: 1; }
    .slide::before { display: none; }

    /* Nada de columnas: todo apilado.
       !important porque las láminas suelen traer grid-template-columns inline. */
    .cards-grid, .body-grid, .compare-grid, .stats-row, .timeline, .findings, .two-col {
      display: grid;
      grid-template-columns: 1fr !important;
      gap: 14px !important;
    }
    /* Sin esto, un hijo ancho (una tabla) estira la página y corta todo el texto */
    .cards-grid > *, .body-grid > *, .compare-grid > *, .stats-row > *,
    .timeline > *, .findings > *, .two-col > * { min-width: 0; }

    /* En Gravity el header va en position:absolute — en móvil debe volver
       al flujo o se superpone al título de la lámina */
    .slide-header {
      position: static;
      top: auto; left: auto; right: auto;
      margin-bottom: 18px;
    }
    .meta { font-size: 9px; letter-spacing: 1px; }
    .brand-name { font-size: 11px; letter-spacing: 2px; }

    .title-block { margin-bottom: 18px; }
    .eyebrow { font-size: 10px; letter-spacing: 2.5px; }
    .slide-title { font-size: clamp(22px, 7vw, 30px); letter-spacing: -0.8px; line-height: 1.06; }
    .slide-subtitle { font-size: 14px; }

    .slide.cover, .slide.divider { padding: 40px 22px 96px; }
    .cover-title { font-size: clamp(30px, 9.5vw, 42px); letter-spacing: -1.5px; }
    .cover-subtitle { font-size: 16px; }
    .cover-footer { flex-direction: column; align-items: flex-start; gap: 8px; margin-top: 36px; }
    .logo-cliente { font-size: 12px; }
    .section-number { font-size: clamp(80px, 26vw, 120px); margin-bottom: -14px; letter-spacing: -4px; }
    .section-title { font-size: clamp(26px, 8vw, 36px); }
    .section-subtitle { font-size: 15px; }

    .card { padding: 18px 18px 16px; }
    .metric-pct { font-size: clamp(30px, 9vw, 42px); }
    .metric-label { font-size: 9.5px; }
    .stat-value { font-size: 22px; }
    .stat-label { font-size: 11px; }

    .compare-value { font-size: clamp(26px, 8vw, 34px); }
    .compare-arrow { transform: rotate(90deg); margin: 4px auto; }

    .bullet-list li, .body-text { font-size: 13.5px; line-height: 1.6; }
    .bullet-num { font-size: 20px; }

    .quote-text { font-size: clamp(20px, 6.2vw, 28px); line-height: 1.18; }
    .quote-author, .author-name { font-size: 13.5px; }
    .punchline { font-size: clamp(22px, 6.6vw, 30px); }

    /* Las tablas anchas se deslizan solas, no rompen la página */
    .tbl-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; max-width: 100%; min-width: 0; }
    .tbl { font-size: 12px; min-width: 460px; }
    .tbl th { font-size: 8.5px; padding: 6px 8px; letter-spacing: 1px; }
    .tbl td { font-size: 12px; padding: 7px 8px; }

    .footer-insight { margin-top: 22px; padding-top: 16px; flex-direction: column; align-items: flex-start; gap: 10px; }
    .insight-text { font-size: 13px; }
    .page-num { position: static; display: block; margin-top: 22px; text-align: right; }
    .nav-hint { display: none; }

    /* Barra táctil fija: pasar láminas sin depender del teclado */
    .mobile-nav {
      display: flex; position: fixed; bottom: 0; left: 0; right: 0;
      align-items: center; justify-content: space-between;
      padding: 10px 16px calc(10px + env(safe-area-inset-bottom));
      background: var(--primary); z-index: 50;
    }
    .mobile-nav button {
      appearance: none; border: 0; background: rgba(255,255,255,0.14);
      color: var(--white); font-family: 'Montserrat', sans-serif; font-weight: 900;
      font-size: 15px; padding: 10px 22px; border-radius: 8px; cursor: pointer;
    }
    .mobile-nav button:disabled { opacity: 0.3; }
    .mobile-nav .mn-count {
      font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 12px;
      color: rgba(255,255,255,0.85); letter-spacing: 2px;
    }
  }
```

## 3. HTML — la barra táctil (justo después de `.nav-hint`)

```html
<nav class="mobile-nav" aria-label="Navegación de láminas">
  <button type="button" id="mnPrev" aria-label="Lámina anterior">‹</button>
  <span class="mn-count" id="mnCount">01 / 12</span>
  <button type="button" id="mnNext" aria-label="Lámina siguiente">›</button>
</nav>
```

Toda tabla ancha va envuelta:

```html
<div class="tbl-wrap"><table class="tbl">…</table></div>
```

## 4. JS — escalado, swipe y botones

```js
  const portraitMQ = window.matchMedia('(max-width: 820px) and (orientation: portrait)');
  const isPortrait = () => portraitMQ.matches;

  // La lámina mide 1280x720 lógicos: la escalamos para que quepa ENTERA en la ventana.
  function fitSlides() {
    if (isPortrait()) { document.documentElement.style.setProperty('--scale', '1'); return; }
    const margin = document.fullscreenElement ? 1 : 0.95;
    const k = Math.min((window.innerWidth * margin) / 1280, (window.innerHeight * margin) / 720);
    document.documentElement.style.setProperty('--scale', String(k));
  }

  // dentro de showSlide(index), al final:
  //   const count = document.getElementById('mnCount');
  //   if (count) count.textContent = `${String(index+1).padStart(2,'0')} / ${String(total).padStart(2,'0')}`;
  //   document.getElementById('mnPrev').disabled = index === 0;
  //   document.getElementById('mnNext').disabled = index === total - 1;
  //   if (isPortrait()) window.scrollTo(0, 0);

  // El click-para-avanzar solo en escritorio (en móvil estorba al hacer scroll)
  document.addEventListener('click', (e) => {
    if (isPortrait() || e.target.closest('.mobile-nav')) return;
    const x = e.clientX, half = window.innerWidth / 2;
    if (x > half) next(); else prev();
  });

  document.getElementById('mnPrev').addEventListener('click', prev);
  document.getElementById('mnNext').addEventListener('click', next);

  // Deslizar con el dedo
  let touchX = null, touchY = null;
  document.addEventListener('touchstart', (e) => {
    touchX = e.changedTouches[0].clientX; touchY = e.changedTouches[0].clientY;
  }, { passive: true });
  document.addEventListener('touchend', (e) => {
    if (touchX === null) return;
    const dx = e.changedTouches[0].clientX - touchX;
    const dy = e.changedTouches[0].clientY - touchY;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) { dx < 0 ? next() : prev(); }
    touchX = touchY = null;
  }, { passive: true });

  window.addEventListener('resize', fitSlides);
  window.addEventListener('orientationchange', () => setTimeout(fitSlides, 150));
  document.addEventListener('fullscreenchange', fitSlides);
  portraitMQ.addEventListener('change', fitSlides);

  fitSlides();   // antes del showSlide(0) inicial
```

## Las 3 trampas (las tres me costaron una iteración cada una)

1. **El `@media` va AL FINAL del `<style>`.** Si lo pones arriba, las reglas base (misma
   especificidad, declaradas después) ganan y el móvil se ve exactamente igual de roto.
   Síntoma: la barra táctil aparece pero las tipografías siguen gigantes.
2. **`min-width: 0` en los hijos de cualquier grid.** Un grid item no se encoge por debajo
   de su contenido: una tabla ancha estira la página entera y corta TODO el texto de la
   lámina, no solo la tabla.
3. **`!important` en `grid-template-columns`.** Las láminas suelen llevar
   `style="grid-template-columns: 1.2fr 1fr"` inline, y el estilo inline le gana a la media
   query. Síntoma: dos columnas superpuestas encima del texto.

## Verificación obligatoria antes de entregar

### Opción A — a ojo, en tu navegador (sirve en cualquier computador)

1. Abre el deck en Chrome.
2. `F12` → icono de móvil (`Ctrl+Shift+M` / `Cmd+Shift+M`).
3. Elige **iPhone 14** y revisa **la lámina más cargada del deck**, no la portada.
4. Dale al icono de rotar para verla en horizontal.

### Opción B — capturas automáticas

```bash
# macOS
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# Linux
CH="google-chrome"
# Windows (PowerShell): $CH = "C:\Program Files\Google\Chrome\Application\chrome.exe"

D="file:///ruta/al/deck.html"
"$CH" --headless --disable-gpu --window-size=390,844  --virtual-time-budget=4500 --screenshot=movil.png "$D#s7"
"$CH" --headless --disable-gpu --window-size=844,390  --virtual-time-budget=4500 --screenshot=horiz.png "$D#s7"
"$CH" --headless --disable-gpu --window-size=1600,900 --virtual-time-budget=4500 --screenshot=desk.png  "$D#s7"
```

Mirar las tres capturas:

- [ ] Ningún texto cortado por el borde derecho
- [ ] Ninguna tabla desaparecida ni superpuesta
- [ ] La cifra más grande (precio, métrica hero) se lee completa
- [ ] En horizontal se ve la lámina entera, sin recortes
- [ ] En escritorio nada cambió respecto a antes

Requiere que el deck soporte `#sN` para abrir una lámina suelta (ya viene en `deck-shell.html`).
