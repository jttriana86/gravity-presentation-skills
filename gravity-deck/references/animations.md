# Animaciones — Gravity Deck

Sutiles, profesionales, nunca distractoras. La animación debe pasar desapercibida — el contenido es el protagonista.

## Filosofía

1. **Solo opacity + translateY** — nunca rotaciones, escalados grandes, rebotes (`bounce`), elásticas.
2. **Duración corta** — 400-600ms máximo para entrance, 200ms para hover.
3. **Easing premium** — `cubic-bezier(0.16, 1, 0.3, 1)` (ease-out exponencial). Nunca `ease-in-out` genérico ni `linear`.
4. **Stagger 80-120ms** — entre elementos hermanos. Más rápido se ve "todo a la vez", más lento se ve lento.
5. **Una vez al cargar** — entrances suceden 1 vez al entrar a la slide. Si vuelves a la slide, no se re-animan (se sienten cheap).
6. **Respetar `prefers-reduced-motion`** — si el sistema lo pide, desactivar animaciones.

## Animaciones permitidas

### 1. Slide entrance (al entrar a una slide)

```css
@keyframes slideEnter {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide.active .animate-in {
  animation: slideEnter 600ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
```

Aplicar a: títulos, subtítulos, cards, párrafos.

### 2. Stagger en cards / grids

```css
.slide.active .animate-in:nth-child(1) { animation-delay: 0ms; }
.slide.active .animate-in:nth-child(2) { animation-delay: 100ms; }
.slide.active .animate-in:nth-child(3) { animation-delay: 200ms; }
.slide.active .animate-in:nth-child(4) { animation-delay: 300ms; }
```

### 3. Counter animation (números cuentan desde 0)

JavaScript-based, dispara al activar slide:

```javascript
function animateCounter(el, target, duration = 1200) {
  const start = performance.now();
  const startVal = 0;
  const update = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current = startVal + (target - startVal) * eased;
    el.textContent = formatNumber(current, el.dataset.format);
    if (progress < 1) requestAnimationFrame(update);
    else el.textContent = formatNumber(target, el.dataset.format);
  };
  requestAnimationFrame(update);
}
```

Usar en hero metrics (+150%, $25.000, 12.515).

### 4. Hover en cards (sutil)

```css
.card {
  transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 200ms cubic-bezier(0.16, 1, 0.3, 1);
}
.card:hover {
  transform: translateY(-2px);
  box-shadow:
    0 1px 0 rgba(255,255,255,1) inset,
    0 4px 8px rgba(5, 19, 103, 0.08),
    0 32px 64px -16px rgba(5, 19, 103, 0.22);
}
```

Solo en presentaciones interactivas (no impresas/PDF).

### 5. Slide transition (cambio entre slides)

```css
.slide {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 400ms cubic-bezier(0.16, 1, 0.3, 1);
  pointer-events: none;
}
.slide.active {
  opacity: 1;
  pointer-events: auto;
}
```

Crossfade simple. Sin slide horizontal estilo PowerPoint (cheap).

### 6. Progress bar

```css
.progress-bar {
  position: fixed;
  top: 0; left: 0;
  height: 3px;
  background: var(--primary);
  transition: width 400ms cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 100;
}
```

Width se actualiza con JS según `currentSlide / totalSlides * 100`.

## Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Sin esto, los usuarios con vestibular disorders sufren. Es accesibilidad básica.

## Anti-patrones

| ❌ Prohibido | Por qué falla |
|-------------|---------------|
| `bounce`, `elastic`, `back` easings | Cheap, infantil, distrae |
| Rotaciones (`rotate`) en entrances | Mareantes, no premium |
| `scale(2)` o más | Saltos visuales agresivos |
| Animar 10+ elementos a la vez sin stagger | Caótico |
| Stagger > 200ms entre hermanos | Lento, frustra al espectador |
| `linear` o `ease-in-out` genérico | Plano, no premium |
| Animaciones que se repiten (`infinite`) | Distrae del contenido |
| Hover effects en presentación viva | El presentador no hace hover, distrae |
| Counter animations en cifras > 5 segundos | Aburre |
| Slide horizontal estilo PowerPoint clásico | Cheap, todos lo conocen |
