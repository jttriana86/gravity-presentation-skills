# Slide Templates — Gravity Deck

6 templates listos para combinar. Cada uno tiene HTML + cuándo usarlo + variaciones permitidas.

Todos los templates van dentro de `<section class="slide" data-slide="N">...</section>` (ver `deck-shell.html`).

---

## §1 — `slide-cover` (Portada / Cierre)

**Cuándo usar:** primera slide del deck, slide de cierre, hero statements.

**Look:** fondo navy sólido, título Montserrat Black gigante en blanco, dot rojo arriba-izq.

```html
<section class="slide cover" data-slide="1">
  <div class="brand-mark animate-in">
    <span class="dot-sello"></span>
    <span class="brand-name brand-name-light">CORPONOVO</span>
  </div>

  <div class="cover-content">
    <p class="eyebrow eyebrow-light animate-in">INFORME ORGÁNICO</p>
    <h1 class="cover-title animate-in">Agosto 2025</h1>
    <p class="cover-subtitle animate-in">Reporte de crecimiento mensual · redes sociales</p>
  </div>

  <div class="cover-footer animate-in">
    <span class="logo-cliente">[LOGO CLIENTE]</span>
    <span class="meta-light">PRESENTADO POR GRAVITY</span>
  </div>
</section>
```

**Variaciones:**
- Imagen de fondo con overlay navy 80% (para covers más editoriales)
- Subtítulo en Cormorant italic blanco (si el deck es manifesto, no reporte)

---

## §2 — `slide-divider` (Divisor de sección)

**Cuándo usar:** entre secciones del deck, marcar inicio de capítulo.

**Look:** fondo navy con número de sección gigante en outline + título sección.

```html
<section class="slide divider" data-slide="2">
  <div class="brand-mark animate-in">
    <span class="dot-sello"></span>
    <span class="brand-name brand-name-light">CORPONOVO</span>
  </div>

  <div class="divider-content">
    <span class="section-number animate-in">01</span>
    <h2 class="section-title animate-in">Crecimiento orgánico</h2>
    <p class="section-subtitle animate-in">Seguidores, alcance y nuevas conexiones</p>
  </div>
</section>
```

**Estilo del número:** Montserrat Black 240px, color transparente, `-webkit-text-stroke: 2px rgba(255,255,255,0.3)`. Solo outline, no relleno.

---

## §3 — `slide-metrics` (Datos / Métricas)

**Cuándo usar:** mostrar KPIs, % crecimiento, comparar plataformas, reportes.

**Look:** fondo blanco, 2-3 cards con bezel sutil (border-top navy 3px + sombra 24px), números hero en verde.

```html
<section class="slide" data-slide="3">
  <header class="slide-header animate-in">
    <div class="brand-mark">
      <span class="dot-sello"></span>
      <span class="brand-name">CORPONOVO</span>
    </div>
    <span class="meta">INFORME ORGÁNICO · AGOSTO 2025</span>
  </header>

  <div class="title-block animate-in">
    <p class="eyebrow">SEGUIDORES</p>
    <h1 class="slide-title">Crecimiento mensual</h1>
    <p class="slide-subtitle">Activaciones presenciales como motor digital.</p>
  </div>

  <div class="cards-grid">
    <article class="card animate-in" data-stagger="1">
      <div class="card-header">
        <span class="card-platform">FACEBOOK</span>
        <span class="card-icon">f</span>
      </div>
      <div class="metric-hero">
        <span class="metric-arrow">▲</span>
        <span class="metric-pct" data-counter="150" data-format="percent">+150%</span>
      </div>
      <div class="metric-label">CRECIMIENTO MES</div>
      <div class="divider-h"></div>
      <div class="stats-row">
        <div class="stat">
          <span class="stat-value" data-counter="2262" data-format="number">2.262</span>
          <span class="stat-label">Total seguidores</span>
        </div>
        <div class="stat">
          <span class="stat-value" data-counter="5">5</span>
          <span class="stat-label">Nuevos en agosto</span>
        </div>
      </div>
    </article>

    <article class="card animate-in" data-stagger="2">
      <!-- ... segunda card Instagram (mismo schema) ... -->
    </article>
  </div>

  <footer class="footer-insight animate-in">
    <span class="insight-tag">INSIGHT</span>
    <p class="insight-text">
      Los picos de seguidores coincidieron con <strong>fechas clave fuera del entorno digital</strong>.
    </p>
  </footer>

  <span class="page-num">03 / 24</span>
</section>
```

**Variaciones:**
- 3 cards (1fr 1fr 1fr) cuando hay 3 plataformas
- 1 card grande hero (cuando hay 1 KPI dominante)
- Cards con icon SVG real (Facebook, Instagram, LinkedIn) en vez de letra

---

## §4 — `slide-body` (Cuerpo / Análisis)

**Cuándo usar:** explicaciones largas, análisis de tendencias, contexto.

**Look:** fondo blanco, título izq + cuerpo derecha (2 columnas) o título arriba + bullets abajo.

```html
<section class="slide" data-slide="4">
  <header class="slide-header animate-in">
    <div class="brand-mark">
      <span class="dot-sello"></span>
      <span class="brand-name">CORPONOVO</span>
    </div>
    <span class="meta">ANÁLISIS</span>
  </header>

  <div class="body-grid">
    <div class="body-left animate-in">
      <p class="eyebrow">CONTEXTO</p>
      <h1 class="slide-title">Por qué subió Facebook<br>tanto este mes.</h1>
    </div>

    <div class="body-right animate-in">
      <p class="body-text">
        El crecimiento de <strong>+150%</strong> en Facebook respondió a tres factores combinados:
      </p>
      <ul class="bullet-list">
        <li class="animate-in" data-stagger="1">
          <span class="bullet-num">01</span>
          <div>
            <strong>Activación presencial en el evento Corponovo Fest</strong>
            <p>3 días con QR de seguimiento en escenarios.</p>
          </div>
        </li>
        <li class="animate-in" data-stagger="2">
          <span class="bullet-num">02</span>
          <div>
            <strong>Contenido tipo carrusel de aliados</strong>
            <p>Tags cruzados generaron alcance orgánico extendido.</p>
          </div>
        </li>
        <li class="animate-in" data-stagger="3">
          <span class="bullet-num">03</span>
          <div>
            <strong>Algoritmo Meta favoreciendo contenido local</strong>
            <p>Cambio en el ranking visto desde mediados de agosto.</p>
          </div>
        </li>
      </ul>
    </div>
  </div>

  <span class="page-num">04 / 24</span>
</section>
```

---

## §5 — `slide-compare` (Antes/Después · Comparación)

**Cuándo usar:** mostrar evolución, antes/después, comparar dos opciones.

**Look:** dos columnas con bezel, izquierda gris (antes) vs derecha verde (después).

```html
<section class="slide" data-slide="5">
  <header class="slide-header animate-in">
    <div class="brand-mark">
      <span class="dot-sello"></span>
      <span class="brand-name">CORPONOVO</span>
    </div>
    <span class="meta">EVOLUCIÓN ANUAL</span>
  </header>

  <div class="title-block animate-in">
    <p class="eyebrow">12 MESES</p>
    <h1 class="slide-title">De agosto 2024 a agosto 2025</h1>
  </div>

  <div class="compare-grid">
    <article class="card card-muted animate-in" data-stagger="1">
      <span class="compare-label">ANTES · AGO 2024</span>
      <span class="compare-value compare-value-muted">8.420</span>
      <span class="compare-sub">seguidores Instagram</span>
    </article>

    <span class="compare-arrow animate-in">→</span>

    <article class="card card-positive animate-in" data-stagger="2">
      <span class="compare-label">HOY · AGO 2025</span>
      <span class="compare-value compare-value-positive">12.515</span>
      <span class="compare-sub">+48,6% interanual</span>
    </article>
  </div>

  <span class="page-num">05 / 24</span>
</section>
```

---

## §6 — `slide-quote` (Cita / Punchline)

**Cuándo usar:** frases emblemáticas, hooks, cierres impactantes, testimonios.

**Look:** fondo blanco con cita gigante en navy, italic, sin distracciones.

```html
<section class="slide" data-slide="6">
  <header class="slide-header animate-in">
    <div class="brand-mark">
      <span class="dot-sello"></span>
      <span class="brand-name">CORPONOVO</span>
    </div>
  </header>

  <blockquote class="punchline animate-in">
    <span class="quote-mark">"</span>
    <p class="quote-text">
      Lo presencial no compite con lo digital. <strong>Lo alimenta.</strong>
    </p>
    <footer class="quote-author">
      <span class="author-name">— Insight Gravity</span>
      <span class="author-role">Análisis estratégico Q3 2025</span>
    </footer>
  </blockquote>

  <span class="page-num">06 / 24</span>
</section>
```

**Reglas para citas:**
- Tipografía Open Sans Italic 48-56pt
- Solo 1 strong por cita (la palabra-clave)
- Autor en minúsculas Montserrat ExtraBold + role en gris

---

## Combinaciones recomendadas (deck de 8 slides estándar)

```
01 — slide-cover         (portada)
02 — slide-divider       (sección 1: contexto)
03 — slide-metrics       (KPIs principales)
04 — slide-body          (análisis del crecimiento)
05 — slide-compare       (evolución 12 meses)
06 — slide-quote         (insight clave)
07 — slide-body          (recomendaciones)
08 — slide-cover         (cierre + CTA)
```

## Reglas universales (TODOS los templates)

1. ✅ Dot sello rojo presente en TODA slide (`.brand-mark > .dot-sello`)
2. ✅ Aspect-ratio 16:9 estricto (heredado de `.stage`)
3. ✅ Page-num en esquina inferior derecha (`<span class="page-num">XX / NN</span>`)
4. ✅ `.animate-in` en elementos que entran (título, cards, párrafos)
5. ✅ `data-stagger="N"` para orden secuencial
6. ✅ Logo cliente en cover/cierre, brand-name de cliente en slides internas
