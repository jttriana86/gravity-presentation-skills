#!/usr/bin/env python3
"""
slide_image.py — brand image for a slide: generate it, optimize it, place it.

One command does the whole trip:
  1. builds an on-brand prompt (palette + guard rails) from a plain-language concept
  2. renders it with OpenAI gpt-image-1
  3. optimizes it (resize + WebP for HTML, PNG for PowerPoint) into assets/imagenes/
  4. drops it into the deck: an HTML slide (4 layout patterns) or a PPTX JSON spec

Usage:
  # see the snippet without touching anything
  python slide_image.py --concept "equipo revisando dashboards" --pattern card --dry-run

  # generate + insert into slide 4 of an HTML deck
  python slide_image.py --concept "..." --deck ./proyecto/deck.html --slide 4 --pattern split

  # generate + add an image slide to a gravity-pptx JSON spec
  python slide_image.py --concept "..." --spec ./proyecto/spec.json --slide 5 \\
      --style pizarra --title "Cómo funciona el embudo"

Requirements:
  - pip install requests pillow
  - OPENAI_API_KEY: environment variable, or a line OPENAI_API_KEY=... in
    ~/.claude/.env or in a .env file of the current directory.
"""

import argparse
import base64
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: missing dependency 'requests'. Install: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    Image = None


GENERATIONS_URL = "https://api.openai.com/v1/images/generations"
DEFAULT_MODEL = "gpt-image-1"

# gpt-image-1 only accepts these canvases.
SIZES = {"1:1": "1024x1024", "16:9": "1536x1024", "9:16": "1024x1536"}

ENV_CANDIDATES = [
    Path.home() / ".claude" / ".env",
    Path.cwd() / ".env",
]

BRANDS = {
    "gravity": {"primary": "#051367", "accent": "#004714", "label": "deep navy blue"},
}

# Style recipes. Each one already assumes the guard rails added in build_prompt().
STYLES = {
    "photo": (
        "Editorial corporate photograph, natural window light, shallow depth of field, "
        "muted desaturated palette with {primary} ({label}) present in the environment, "
        "clean uncluttered composition with generous negative space, "
        "shot on a 35mm lens, subtle film grain. Realistic, never stocky or staged."
    ),
    "illustration": (
        "Flat vector editorial illustration on a pure white background. Limited palette: "
        "{primary} as the dominant color, {accent} for a single positive accent, "
        "warm gray for depth. Geometric shapes, confident thick strokes, no gradients "
        "beyond a single subtle tonal step, generous white space. Modern agency look."
    ),
    "texture": (
        "Abstract background texture, extremely subtle, low contrast, {primary} on near-white. "
        "Soft geometric gradient mesh or fine diagonal lines. It must sit BEHIND text: "
        "no focal point, no busy detail, nothing that competes for attention."
    ),
    "pizarra": (
        "Hand-drawn whiteboard sketchnote: black marker strokes on a clean white board, "
        "simple stick figures, arrows, boxes and connectors, slightly imperfect lines, "
        "accents in {accent} and orange only. Explanatory diagram, generous spacing, "
        "nothing photorealistic."
    ),
}

# Global guard rails — the things that break a deck when the model improvises.
GUARDS = (
    "Absolutely no text, no letters, no numbers, no logos, no watermarks, no UI chrome, "
    "no brand names anywhere in the image. No borders or frames. "
    "Composition must stay clear of the outer 5% on every side (safe margin for cropping)."
)

PATTERNS = ("full", "hero", "split", "card", "band")

# La lámina mide 1280x720 lógicos y NO crece: lo que no cabe se corta.
# HEAVY = bloques que ya se comen la lámina entera (ni siquiera media columna los aguanta).
# CROWDING = además, contenido que deja sin aire una imagen apilada debajo.
HEAVY = ("cards-grid", "compare-grid", "tbl-wrap", "timeline", "findings")
CROWDING = HEAVY + ("body-grid",)

CSS_MARKER = "/* deck-imagenes */"

CSS_BASE = """
  /* deck-imagenes — image patterns (generated, safe to edit) */
  .slide-bg { position: absolute; inset: 0; overflow: hidden; z-index: 0; }
  .slide-bg img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .slide-bg::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(180deg,
      color-mix(in srgb, var(--primary) 62%, transparent) 0%,
      color-mix(in srgb, var(--primary) 78%, transparent) 100%);
  }
  .slide.has-bg > *:not(.slide-bg) { position: relative; z-index: 1; }

  .split-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 40px; align-items: center; width: 100%;
  }
  /* `.slide` es un grid de filas fijas y el header/page-num son absolute, así que el
     contenido cae en una fila `auto` y el hueco libre se va al fondo. Ocupando todas
     las filas + align-self:center queda centrado de verdad (regla 9 de gravity-deck). */
  .slide > .split-grid,
  .slide > .img-full.solo { grid-row: 1 / -1; align-self: center; align-content: center; }
  .split-grid > * { min-width: 0; }
  .split-body, .split-body > * { min-width: 0; }
  /* Un grid de 2 columnas dentro de media lámina se sale por la derecha. */
  .split-body .cards-grid,
  .split-body .compare-grid,
  .split-body .body-grid { grid-template-columns: 1fr !important; }
  .split-media { border-radius: 10px; overflow: hidden; box-shadow: var(--shadow-card); }
  .split-media img { width: 100%; height: 100%; object-fit: cover; display: block; }

  .img-card {
    width: 100%; max-width: 860px; margin: 0 auto;
    flex: 0 1 auto; min-height: 0;
    background: var(--white); border-top: 3px solid var(--primary);
    border-radius: 4px; box-shadow: var(--shadow-card); overflow: hidden;
  }
  /* Techo de altura: sin esto, en un slide que ya trae cards o tabla la imagen
     empuja el contenido y se sale de la lámina. */
  .img-card img { width: 100%; max-height: 320px; object-fit: cover; display: block; }
  .img-caption {
    font-family: 'Open Sans', Arial, sans-serif; font-size: 12px; font-style: italic;
    color: var(--gray); text-align: center; padding: 10px 16px 14px;
  }

  .img-band { width: 100%; margin-top: 28px; border-radius: 8px; overflow: hidden; }
  .img-band img { width: 100%; height: 190px; object-fit: cover; display: block; }

  /* Slide dedicado a la imagen: la lámina lógica mide 720px de alto, header y título
     se comen ~250px, así que la imagen tiene 400px para vivir. */
  .img-full { width: 100%; text-align: center; }
  .img-full img {
    max-width: 100%; max-height: 400px; width: auto; height: auto;
    display: block; margin: 0 auto; border-radius: 6px;
  }
  .img-full.cover img {
    width: 100%; height: 400px; object-fit: cover; box-shadow: var(--shadow-card);
  }
"""

CSS_MOBILE = """
    /* deck-imagenes — mobile */
    .split-grid { grid-template-columns: 1fr !important; gap: 20px; }
    .slide > .split-grid,
    .slide > .img-full.solo { grid-row: auto; align-self: start; align-content: start; }
    .split-media { max-height: 200px; }
    .img-card img { max-height: 210px; }
    .img-band img { height: 130px; }
    .img-full img, .img-full.cover img { max-height: 260px; height: auto; }
    .slide-bg::after { background: color-mix(in srgb, var(--primary) 82%, transparent); }
"""


# --------------------------------------------------------------------------- helpers

def load_api_key() -> str:
    """OPENAI_API_KEY from the environment, else from a known .env file."""
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key.strip()
    for env_file in ENV_CANDIDATES:
        if env_file.is_file():
            for line in env_file.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if line.startswith("OPENAI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    print(
        "ERROR: no OPENAI_API_KEY found.\n"
        "  Set it in the environment, or add a line OPENAI_API_KEY=sk-... to\n"
        f"  {ENV_CANDIDATES[0]} or ./.env",
        file=sys.stderr,
    )
    sys.exit(1)


def slugify(text: str, max_len: int = 48) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return (text[:max_len].rstrip("-")) or "imagen"


def build_prompt(concept: str, style: str, brand: str, extra: str = "") -> str:
    b = BRANDS[brand]
    recipe = STYLES[style].format(primary=b["primary"], accent=b["accent"], label=b["label"])
    parts = [concept.strip().rstrip("."), ".", " ", recipe, " ", GUARDS]
    if extra:
        parts += [" ", extra.strip()]
    return "".join(parts)


def generate(prompt: str, size: str, quality: str, api_key: str,
             model: str, transparent: bool) -> bytes:
    payload = {"model": model, "prompt": prompt, "size": size, "quality": quality, "n": 1}
    if transparent:
        payload["background"] = "transparent"
        payload["output_format"] = "png"

    resp = requests.post(
        GENERATIONS_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=300,
    )
    if resp.status_code != 200:
        print(f"ERROR: OpenAI returned {resp.status_code}: {resp.text[:500]}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()["data"][0]
    if "b64_json" in data:
        return base64.b64decode(data["b64_json"])
    return requests.get(data["url"], timeout=120).content


def optimize(raw: bytes, out_path: Path, max_width: int, transparent: bool) -> Path:
    """Resize and write. WebP for the web, PNG when PowerPoint or alpha is involved."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if Image is None:
        out_path = out_path.with_suffix(".png")
        out_path.write_bytes(raw)
        print("  WARNING: Pillow not installed — saved raw PNG, no resize.", file=sys.stderr)
        return out_path

    tmp = out_path.with_suffix(".orig.png")
    tmp.write_bytes(raw)
    with Image.open(tmp) as im:
        if im.width > max_width:
            ratio = max_width / im.width
            im = im.resize((max_width, int(im.height * ratio)), Image.LANCZOS)
        if out_path.suffix.lower() == ".webp":
            im.save(out_path, "WEBP", quality=82, method=6)
        elif out_path.suffix.lower() in (".jpg", ".jpeg"):
            if im.mode in ("RGBA", "P"):
                im = im.convert("RGB")
            im.save(out_path, "JPEG", quality=88, optimize=True, progressive=True)
        else:
            if not transparent and im.mode in ("RGBA", "P"):
                im = im.convert("RGB")
            im.save(out_path, "PNG", optimize=True)
    tmp.unlink(missing_ok=True)
    return out_path


# ------------------------------------------------------------------------ html glue

def build_snippet(pattern: str, rel_src: str, alt: str, caption: str) -> str:
    cap = f'\n    <p class="img-caption">{caption}</p>' if caption else ""
    if pattern == "hero":
        return f'  <div class="slide-bg"><img src="{rel_src}" alt="{alt}"></div>'
    if pattern == "split":
        return f'    <div class="split-media animate-in"><img src="{rel_src}" alt="{alt}"></div>'
    if pattern == "band":
        return f'  <div class="img-band animate-in"><img src="{rel_src}" alt="{alt}"></div>'
    return (
        f'  <figure class="img-card animate-in" data-stagger="2">\n'
        f'    <img src="{rel_src}" alt="{alt}">{cap}\n'
        f'  </figure>'
    )


def build_full_slide(html: str, rel_src: str, alt: str, title: str,
                     eyebrow: str, caption: str, cover_fit: bool) -> str:
    """A whole new slide whose job is the image. Reuses the deck's own header if there is one."""
    m = re.search(r"<header class=\"slide-header[^\"]*\">.*?</header>", html, re.S)
    header = ("  " + m.group(0).strip() + "\n") if m else ""

    block = ""
    if eyebrow or title:
        block += '  <div class="title-block animate-in">\n'
        if eyebrow:
            block += f'    <p class="eyebrow">{eyebrow}</p>\n'
        if title:
            block += f'    <h1 class="slide-title">{title}</h1>\n'
        block += "  </div>\n"

    cap = f'\n    <figcaption class="img-caption">{caption}</figcaption>' if caption else ""
    cls = "img-full cover" if cover_fit else "img-full"
    if not (eyebrow or title):
        cls += " solo"  # sin título propio: la figura ocupa (y centra en) toda la lámina
    block += (
        f'  <figure class="{cls} animate-in" data-stagger="1">\n'
        f'    <img src="{rel_src}" alt="{alt}">{cap}\n'
        f"  </figure>\n"
    )
    return (
        '  <section class="slide" data-slide="0">\n'
        f'{header}{block}'
        '    <span class="page-num">00 / 00</span>\n'
        "  </section>\n"
    )


# El shell usa <span class="page-num">; toleramos <div> por si un deck lo cambió.
PAGE_BLOCK_RE = re.compile(r'\s*<(span|div) class="page-num"[^>]*>.*?</\1>\s*', re.S)

PAGE_NUM_RE = re.compile(r'<span class="page-num">\s*\d+\s*/\s*\d+\s*</span>')


def renumber(html: str) -> str:
    """Rewrite data-slide and the hand-written `NN / NN` page numbers after inserting.

    Each page-num is numbered by the slide that CONTAINS it — not by the order the
    spans appear — because covers and dividers usually carry no page number at all.
    """
    opens = list(re.finditer(r'<section[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>', html))
    total = len(opens)
    out, prev_end = [], 0

    for i, m in enumerate(opens, 1):
        out.append(html[prev_end:m.start()])
        tag = m.group(0)
        if 'data-slide="' in tag:
            tag = re.sub(r'data-slide="\d+"', f'data-slide="{i}"', tag)
        else:
            tag = tag[:-1] + f' data-slide="{i}">'
        out.append(tag)

        body_end = html.find("</section>", m.end())
        if body_end == -1:
            body_end = len(html)
        body = html[m.end():body_end]
        body = PAGE_NUM_RE.sub(
            f'<span class="page-num">{i:02d} / {total:02d}</span>', body)
        out.append(body)
        prev_end = body_end

    out.append(html[prev_end:])
    return "".join(out)


def insert_full_slide(html: str, slide_no: int, section_html: str):
    """Insert the new section before slide `slide_no` (or last if beyond the end)."""
    loc = find_slide(html, slide_no)
    if loc is not None:
        start = loc[0]
    else:
        last = None
        for m in re.finditer(r"</section>", html):
            last = m
        if last is None:
            return None, "el deck no tiene ningún <section class=\"slide\">"
        start = last.end() + 1
    new_html = html[:start] + section_html + html[start:]
    return renumber(new_html), None


def inject_css(html: str) -> str:
    """Base rules go BEFORE the first @media; mobile overrides go last.

    Both deck skills put the mobile block at the end of <style> on purpose: same
    specificity means last one wins. Appending our base rules there would silently
    outrank the mobile block and break the phone layout.
    """
    if CSS_MARKER in html or ".img-card {" in html:
        return html

    base = f"\n  {CSS_MARKER}\n{CSS_BASE}\n"
    m = re.search(r"\n\s*@media\b", html)
    if m:
        html = html[: m.start()] + base + html[m.start():]
    else:
        html = html.replace("</style>", base + "</style>", 1)

    mobile = (
        "\n  @media (max-width: 820px) and (orientation: portrait) {\n"
        f"{CSS_MOBILE}  }}\n"
    )
    return html.replace("</style>", mobile + "</style>", 1)


def find_slide(html: str, slide_no: int):
    """Return (start, end) offsets of the <section …data-slide="N"…>…</section> block."""
    open_re = re.compile(
        r'<section[^>]*class="[^"]*\bslide\b[^"]*"[^>]*data-slide="%d"[^>]*>' % slide_no
    )
    m = open_re.search(html)
    if not m:
        return None
    end = html.find("</section>", m.end())
    if end == -1:
        return None
    return m.start(), end + len("</section>")


def insert_html(html: str, slide_no: int, pattern: str, snippet: str):
    loc = find_slide(html, slide_no)
    if loc is None:
        return None, f'no encontré <section class="slide" data-slide="{slide_no}"> en el deck'
    start, end = loc
    block = html[start:end]
    open_tag_end = block.find(">") + 1
    open_tag = block[:open_tag_end]
    inner = block[open_tag_end:block.rfind("</section>")]

    if pattern == "hero":
        if "slide-bg" in inner:
            return None, f"el slide {slide_no} ya tiene una imagen de fondo"
        open_tag = re.sub(r'class="([^"]*)"', r'class="\1 has-bg"', open_tag, count=1)
        new_inner = "\n" + snippet + inner

    elif pattern == "split":
        if "split-grid" in inner:
            return None, f"el slide {slide_no} ya está en layout split"
        heavy = [c for c in HEAVY if c in inner]
        if heavy:
            return None, (
                f"el slide {slide_no} trae {', '.join(heavy)}: al pasar a media columna esos "
                f"bloques se apilan y se salen por abajo. Usá --pattern full (slide propio). "
                f"split es para slides de texto o bullets"
            )
        # Everything that is not the fixed header / page number becomes the text column.
        head_re = re.compile(r"\s*<header\b.*?</header>\s*", re.S)
        page_re = PAGE_BLOCK_RE
        head = head_re.search(inner)
        page = page_re.search(inner)
        head_txt = head.group(0) if head else ""
        page_txt = page.group(0) if page else ""
        body = inner
        if head:
            body = body.replace(head_txt, "", 1)
        if page:
            body = body.replace(page_txt, "", 1)
        body = body.strip("\n")
        if not body.strip():
            return None, f"el slide {slide_no} no tiene contenido para poner al lado de la imagen"
        new_inner = (
            f"{head_txt}\n  <div class=\"split-grid\">\n{snippet}\n"
            f"    <div class=\"split-body\">\n{body}\n    </div>\n  </div>\n{page_txt}"
        )

    else:  # card / band → antes del page-num si existe, si no al final
        if "img-card" in inner or "img-band" in inner:
            return None, f"el slide {slide_no} ya tiene una imagen de este tipo"
        crowded = [c for c in CROWDING if c in inner]
        if crowded:
            return None, (
                f"el slide {slide_no} ya está lleno ({', '.join(crowded)}) y la lámina no crece: "
                f"la imagen quedaría cortada por abajo. Usá --pattern full (slide propio); "
                f"--pattern split solo si el contenido es texto o bullets"
            )
        page_re = PAGE_BLOCK_RE
        page = page_re.search(inner)
        if page:
            new_inner = inner[: page.start()] + "\n" + snippet + "\n" + inner[page.start():]
        else:
            new_inner = inner + "\n" + snippet + "\n"

    new_block = open_tag + new_inner + "</section>"
    return html[:start] + new_block + html[end:], None


# ------------------------------------------------------------------------ pptx glue

def insert_spec(spec_path: Path, slide_no: int, img_path: Path,
                title: str, eyebrow: str, caption: str):
    """Add an `image` slide to a gravity-pptx JSON spec at position slide_no (1-based)."""
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    slides = spec.setdefault("slides", [])
    rel = os.path.relpath(img_path, spec_path.parent)
    entry = {"type": "image", "image": rel}
    if eyebrow:
        entry["eyebrow"] = eyebrow
    if title:
        entry["title"] = title
    if caption:
        entry["caption"] = caption

    idx = max(0, min(slide_no - 1, len(slides)))
    slides.insert(idx, entry)
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return idx + 1


# ----------------------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(
        description="Generate an on-brand image and place it in a deck (HTML or PPTX spec)."
    )
    p.add_argument("--concept", required=True,
                   help="Qué debe mostrar la imagen, en lenguaje normal (ES o EN)")
    p.add_argument("--style", default="photo", choices=list(STYLES),
                   help="photo | illustration | texture | pizarra (default: photo)")
    p.add_argument("--brand", default="gravity", choices=list(BRANDS),
                   help="Paleta de marca a inyectar en el prompt (default: gravity)")
    p.add_argument("--pattern", default="card", choices=PATTERNS,
                   help="Layout HTML: hero | split | card | band (default: card)")
    p.add_argument("--deck", help="Ruta al deck.html donde insertar")
    p.add_argument("--spec", help="Ruta al JSON spec de gravity-pptx donde insertar")
    p.add_argument("--slide", type=int, help="Número de slide destino (data-slide / posición)")
    p.add_argument("--output", help="Ruta de salida de la imagen (default: assets/imagenes/<slug>)")
    p.add_argument("--aspect", default="16:9", choices=list(SIZES))
    p.add_argument("--quality", default="medium", choices=["low", "medium", "high"])
    p.add_argument("--max-width", type=int, default=1600, help="Ancho máximo en px (default 1600)")
    p.add_argument("--transparent", action="store_true", help="Fondo transparente (PNG con alfa)")
    p.add_argument("--title", default="", help="PPTX: título del slide de imagen")
    p.add_argument("--eyebrow", default="", help="PPTX: eyebrow del slide de imagen")
    p.add_argument("--caption", default="", help="Pie de foto (card en HTML, caption en PPTX)")
    p.add_argument("--alt", default="", help="Texto alternativo del <img> (default: --concept)")
    p.add_argument("--extra", default="", help="Instrucciones extra que se añaden al prompt")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--dry-run", action="store_true",
                   help="No llama a la API ni toca archivos: imprime prompt y snippet")
    args = p.parse_args()

    if args.deck and args.spec:
        print("ERROR: usa --deck o --spec, no los dos.", file=sys.stderr)
        sys.exit(1)
    if (args.deck or args.spec) and not args.slide:
        print("ERROR: --slide es obligatorio cuando insertas en un deck o spec.", file=sys.stderr)
        sys.exit(1)

    prompt = build_prompt(args.concept, args.style, args.brand, args.extra)

    # Destino de la imagen
    slug = slugify(args.concept)
    # WebP para HTML; JPEG para PowerPoint (no lee WebP y el PNG lo deja pesadísimo);
    # PNG solo cuando hace falta canal alfa.
    for_pptx = bool(args.spec)
    ext = ".png" if args.transparent else (".jpg" if for_pptx else ".webp")
    if args.output:
        out_path = Path(args.output).expanduser()
    else:
        anchor = Path(args.deck or args.spec).expanduser().parent if (args.deck or args.spec) else Path.cwd()
        out_path = anchor / "assets" / "imagenes" / f"{slug}{ext}"

    rel_src = os.path.relpath(out_path, Path(args.deck).expanduser().parent) if args.deck else out_path.name
    alt = args.alt or args.concept
    cover_fit = args.style in ("photo", "texture")
    if args.pattern == "full":
        deck_html = Path(args.deck).expanduser().read_text(encoding="utf-8") if args.deck else ""
        snippet = build_full_slide(deck_html, rel_src, alt, args.title,
                                   args.eyebrow, args.caption, cover_fit)
    else:
        snippet = build_snippet(args.pattern, rel_src, alt, args.caption)

    print(f"PROMPT:{prompt}")
    if args.dry_run:
        print(f"OUTPUT:{out_path}  (dry-run, no se generó nada)")
        if not for_pptx:
            print("SNIPPET:\n" + snippet)
        return

    api_key = load_api_key()
    print(f"  → generando {args.style} {args.aspect} ({args.quality})…", file=sys.stderr)
    raw = generate(prompt, SIZES[args.aspect], args.quality, api_key, args.model, args.transparent)
    out_path = optimize(raw, out_path, args.max_width, args.transparent)
    size_kb = out_path.stat().st_size / 1024
    print(f"IMAGE:{out_path}  ({size_kb:.0f} KB)")

    if args.deck:
        deck_path = Path(args.deck).expanduser()
        html = deck_path.read_text(encoding="utf-8")
        html = inject_css(html)
        if args.pattern == "full":
            new_html, err = insert_full_slide(html, args.slide, snippet)
        else:
            new_html, err = insert_html(html, args.slide, args.pattern, snippet)
        if err:
            print(f"WARNING: {err}. La imagen quedó generada; pégala a mano:", file=sys.stderr)
            print("SNIPPET:\n" + snippet)
            return
        deck_path.write_text(new_html, encoding="utf-8")
        print(f"DECK:{deck_path} slide {args.slide} · patrón {args.pattern}")

    elif args.spec:
        spec_path = Path(args.spec).expanduser()
        pos = insert_spec(spec_path, args.slide, out_path,
                          args.title, args.eyebrow, args.caption)
        print(f"SPEC:{spec_path} · slide de imagen insertado en posición {pos}")
        print("  Regenerá el .pptx: python scripts/build_deck.py <spec.json> <salida.pptx>")
    else:
        print("SNIPPET:\n" + snippet)


if __name__ == "__main__":
    main()
