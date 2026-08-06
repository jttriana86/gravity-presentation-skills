# Patrones HTML — markup y CSS

El script inyecta este CSS solo y coloca el markup. Este archivo es para cuando lo hacés a
mano (deck con estructura rara, o querés ajustar algo después).

## Dónde va el CSS

El bloque base va **antes del primer `@media`** del `<style>`, y las reglas móviles **al
final**. Los dos deck shells ponen su bloque móvil de último a propósito: misma
especificidad, gana el último. Si pegás las reglas base al final, le ganan al bloque móvil
y el deck se rompe en el celular sin que se note en el escritorio.

Marcador para no duplicar: `/* deck-imagenes */`.

## 1. `full` — slide dedicado

```html
<section class="slide" data-slide="5">
  <header class="slide-header animate-in">
    <div class="brand-mark"><span class="dot-sello"></span><span class="brand-name">CLIENTE</span></div>
    <span class="meta">SECCIÓN</span>
  </header>
  <div class="title-block animate-in">
    <p class="eyebrow">CÓMO TRABAJAMOS</p>
    <h1 class="slide-title">El comité de resultados</h1>
  </div>
  <figure class="img-full cover animate-in" data-stagger="1">
    <img src="assets/imagenes/comite.webp" alt="equipo revisando resultados">
    <figcaption class="img-caption">Sesión mensual con el cliente</figcaption>
  </figure>
  <span class="page-num">05 / 12</span>
</section>
```

- `cover` = la imagen llena 400px de alto recortando (fotos). Sin `cover` = se muestra
  completa sin recortar (diagramas, pizarra).
- Sin `title-block`, agregá la clase `solo` a la figura para que ocupe y centre toda la lámina.
- **Al insertar un slide hay que renumerar** `data-slide` y todos los `page-num` (`NN / NN`).
  El total lo calcula el JS solo, pero los números escritos en el HTML no.

## 2. `hero` — fondo a sangre

```html
<section class="slide cover has-bg" data-slide="1">
  <div class="slide-bg"><img src="assets/imagenes/fachada.webp" alt=""></div>
  <!-- el contenido del slide sigue igual -->
</section>
```

El `::after` del `.slide-bg` pone el degradado navy 62% → 78%. Es el mínimo para que el
blanco se lea en proyector; en móvil sube a 82% porque el texto se apila.

## 3. `split` — imagen al lado del contenido

```html
<div class="split-grid">
  <div class="split-media animate-in"><img src="…" alt="…"></div>
  <div class="split-body">
    <!-- todo lo que había en el slide, menos el header y el page-num -->
  </div>
</div>
```

Tres cosas que hay que respetar:
- `min-width: 0` en los hijos, o una tabla ancha estira la columna y corta el texto.
- Cualquier grid interno pasa a una columna (`grid-template-columns: 1fr !important`).
- `grid-row: 1 / -1` + `align-self: center` en el `.split-grid`, o el contenido se pega
  arriba y queda un hueco abajo — el header y el `page-num` son `absolute`, así que el grid
  del slide solo ve un hijo en flujo.

## 4. `card` — figura con bezel

```html
<figure class="img-card animate-in" data-stagger="2">
  <img src="…" alt="…">
  <p class="img-caption">Pie de foto opcional</p>
</figure>
```

Va **antes** del `<span class="page-num">`. Techo de 320px de alto (210 en móvil).

## 5. `band` — banda al pie

```html
<div class="img-band animate-in"><img src="…" alt="…"></div>
```

190px de alto, recortando. Decorativa: no metas ahí información que haya que leer.

## Variables de color

El CSS usa las variables del propio deck (`--primary`, `--green`, `--shadow-card`, `--gray`),
así que no hay hex escritos a mano: si algún día cambia la paleta en el `deck-shell.html`,
las imágenes siguen combinando solas.
