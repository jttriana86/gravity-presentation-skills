#!/usr/bin/env python3
"""
Pizarra image generator — whiteboard / sketchnote style.

Generates hand-drawn marker-on-whiteboard images using the OpenAI
Images API (gpt-image-1). Forces 16:9 (or other) aspect ratio via
Pillow post-processing if the model ignores the requested ratio.

Style: black marker on white background, wobbly imperfect lines,
simple illustrations (characters, arrows, icons), optional handwritten
text in Spanish, accent colors limited to orange / green / yellow.

Usage:
  python generate_pizarra.py --concept "..." --output path/to/foo.png
  python generate_pizarra.py --concept "..." --output ... --aspect 16:9
  python generate_pizarra.py --concept "..." --output ... --no-text
  python generate_pizarra.py --concept "..." --output ... --accent black-only

Requirements:
  - pip install requests Pillow
  - OPENAI_API_KEY — from the environment variable, or from a line
    OPENAI_API_KEY=... in ~/.claude/.env or in ./.env
"""

import argparse
import base64
import os
import sys
from io import BytesIO
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: missing dependency 'requests'. Install: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("ERROR: missing dependency 'Pillow'. Install: pip install Pillow", file=sys.stderr)
    sys.exit(1)


OPENAI_API_URL = "https://api.openai.com/v1/images/generations"
DEFAULT_MODEL = "gpt-image-1"
ENV_CANDIDATES = [Path.home() / ".claude" / ".env", Path.cwd() / ".env"]

ASPECT_RATIOS = {
    "16:9": (16, 9),
    "1:1": (1, 1),
    "4:3": (4, 3),
}

# gpt-image-1 only accepts these canvas sizes. We pick the closest one and let
# force_aspect_ratio() pad it to the exact ratio afterwards.
OPENAI_SIZES = {
    "16:9": "1536x1024",
    "4:3": "1536x1024",
    "1:1": "1024x1024",
}


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

    print("ERROR: OPENAI_API_KEY not found.", file=sys.stderr)
    print("Export it (export OPENAI_API_KEY=sk-...) or add it to ~/.claude/.env", file=sys.stderr)
    sys.exit(1)


def build_pizarra_prompt(
    concept: str,
    aspect: str = "16:9",
    include_text: bool = True,
    accent: str = "orange,green,yellow",
) -> str:
    """Wrap user concept with whiteboard sketchnote style guidelines."""
    aspect_hint = {
        "16:9": "wide horizontal cinematic 16:9 aspect ratio (much wider than tall, like a slide presentation, 1920x1080 proportions). Compose all elements horizontally across the width.",
        "1:1": "square 1:1 aspect ratio (equal width and height, like an Instagram post).",
        "4:3": "horizontal 4:3 aspect ratio (slightly wider than tall, like an old presentation slide).",
    }.get(aspect, "wide horizontal 16:9 aspect ratio.")

    text_clause = (
        "Include short handwritten Spanish title at top in big rough capital letters "
        "and small handwritten Spanish labels under the illustrations. Keep text short "
        "(max 3-4 words per phrase). Letters should look hand-drawn, slightly wobbly."
        if include_text
        else "Pure illustration only — absolutely NO text, NO words, NO letters, NO labels anywhere in the image. Use only visual symbols, arrows, and icons to convey meaning."
    )

    if accent == "black-only":
        accent_clause = "Use ONLY black marker ink on pure white background. NO color accents. Pure black-and-white."
    else:
        accent_clause = (
            f"Limited accent colors only: {accent.replace(',', ', ')}. "
            "Use these accents sparingly on a few key elements (frames, arrow tips, "
            "underlines, highlights). Everything else in black ink."
        )

    return (
        f"Hand-drawn whiteboard sketch in black marker on plain white paper background. "
        f"Sketchnote / visual thinking / didactic explainer style. "
        f"Concept to illustrate: {concept}. "
        f"{text_clause} "
        f"Use casual hand-drawn arrows, small stars, asterisks, dotted lines, "
        f"underlines and circles for emphasis. Wobbly imperfect lines like a real "
        f"marker on a whiteboard, not perfect vectors. Simple stick-figure-like "
        f"characters with friendly faces. Icons and small symbols (lightbulbs, "
        f"checkmarks, gears, speech bubbles, arrows). "
        f"{accent_clause} "
        f"NO gradients, NO neon, NO 3D, NO photorealism, NO glossy textures, "
        f"NO computer-generated clean vectors. Looks like a person drew it on a "
        f"whiteboard with a marker in 2 minutes. "
        f"Aspect ratio: {aspect_hint}"
    )


def call_openai(api_key: str, prompt: str, model: str, aspect: str, quality: str) -> bytes:
    """Call the OpenAI Images API (gpt-image-1). Returns PNG image bytes."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    size = OPENAI_SIZES.get(aspect, "1536x1024")
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "n": 1,
    }

    print(f"  -> POST {OPENAI_API_URL}", file=sys.stderr)
    print(f"  -> model: {model} · size: {size} · quality: {quality}", file=sys.stderr)

    r = requests.post(OPENAI_API_URL, json=payload, headers=headers, timeout=300)

    if r.status_code != 200:
        print(f"ERROR: OpenAI returned {r.status_code}", file=sys.stderr)
        print(f"Response: {r.text[:800]}", file=sys.stderr)
        sys.exit(2)

    data = r.json()

    try:
        item = data["data"][0]
    except (KeyError, IndexError) as e:
        print(f"ERROR: unexpected response structure: {e}", file=sys.stderr)
        print(f"Response: {str(data)[:800]}", file=sys.stderr)
        sys.exit(3)

    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])

    if item.get("url"):
        resp = requests.get(item["url"], timeout=120)
        resp.raise_for_status()
        return resp.content

    print("ERROR: response has no image data.", file=sys.stderr)
    print(f"Full response: {str(data)[:800]}", file=sys.stderr)
    sys.exit(4)


def strip_gray_bands(image_bytes: bytes, brightness_threshold: int = 200) -> bytes:
    """Detect and crop uniform gray/black bands at top/bottom/sides.

    The image model sometimes returns a square canvas with solid gray fill bars
    framing the actual sketch (RGB ~111). Those bars look like a dirty background
    when the slide background is pure white. We scan inward from each edge and
    crop the first row/column whose average brightness clears the threshold.
    """
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    w, h = img.size
    px = img.load()

    def row_avg(y):
        s = 0
        n = 0
        for x in range(0, w, 4):
            r, g, b = px[x, y]
            s += (r + g + b) / 3
            n += 1
        return s / n if n else 255

    def col_avg(x, y0, y1):
        s = 0
        n = 0
        for y in range(y0, y1 + 1, 4):
            r, g, b = px[x, y]
            s += (r + g + b) / 3
            n += 1
        return s / n if n else 255

    top = 0
    for y in range(h):
        if row_avg(y) > brightness_threshold:
            top = y
            break
    bottom = h - 1
    for y in range(h - 1, -1, -1):
        if row_avg(y) > brightness_threshold:
            bottom = y
            break

    if top == 0 and bottom == h - 1:
        return image_bytes  # no bands found

    left = 0
    for x in range(w):
        if col_avg(x, top, bottom) > brightness_threshold:
            left = x
            break
    right = w - 1
    for x in range(w - 1, -1, -1):
        if col_avg(x, top, bottom) > brightness_threshold:
            right = x
            break

    if top == 0 and bottom == h - 1 and left == 0 and right == w - 1:
        return image_bytes

    cropped = img.crop((left, top, right + 1, bottom + 1))
    out = BytesIO()
    cropped.save(out, format="PNG", optimize=True)
    print(
        f"  -> stripped gray bands: {w}x{h} -> {cropped.size[0]}x{cropped.size[1]}",
        file=sys.stderr,
    )
    return out.getvalue()


def force_aspect_ratio(image_bytes: bytes, aspect: str) -> bytes:
    """Pad the image with white pixels to force exact aspect ratio.
    Never crops content — always extends canvas with white padding.
    """
    if aspect not in ASPECT_RATIOS:
        return image_bytes

    target_w, target_h = ASPECT_RATIOS[aspect]
    target_ratio = target_w / target_h

    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    w, h = img.size
    current_ratio = w / h

    # Already close enough (within 2%)
    if abs(current_ratio - target_ratio) / target_ratio < 0.02:
        return image_bytes

    if current_ratio < target_ratio:
        # Image too tall -> pad sides (left + right) with white
        new_w = int(round(h * target_ratio))
        new_img = Image.new("RGB", (new_w, h), (255, 255, 255))
        offset_x = (new_w - w) // 2
        new_img.paste(img, (offset_x, 0))
    else:
        # Image too wide -> pad top + bottom with white
        new_h = int(round(w / target_ratio))
        new_img = Image.new("RGB", (w, new_h), (255, 255, 255))
        offset_y = (new_h - h) // 2
        new_img.paste(img, (0, offset_y))

    out = BytesIO()
    new_img.save(out, format="PNG", optimize=True)
    print(
        f"  -> padded to {aspect}: {w}x{h} -> {new_img.size[0]}x{new_img.size[1]}",
        file=sys.stderr,
    )
    return out.getvalue()


def main():
    parser = argparse.ArgumentParser(
        description="Generate whiteboard / sketchnote image (pizarra style)"
    )
    parser.add_argument(
        "--concept", required=True, help="What the image should explain (Spanish or English)"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to save the PNG (e.g. ./assets/pizarra/foo.png)",
    )
    parser.add_argument(
        "--aspect",
        default="16:9",
        choices=list(ASPECT_RATIOS.keys()),
        help="Aspect ratio (default: 16:9)",
    )
    parser.add_argument(
        "--no-text",
        action="store_true",
        help="Disable handwritten text — pure illustrations only",
    )
    parser.add_argument(
        "--accent",
        default="orange,green,yellow",
        help="Accent colors (comma-separated) or 'black-only'. Default: orange,green,yellow",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"OpenAI image model (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--quality",
        default="medium",
        choices=["low", "medium", "high"],
        help="Render quality / cost (default: medium)",
    )
    parser.add_argument(
        "--no-pad",
        action="store_true",
        help="Skip Pillow aspect-ratio padding (use raw output)",
    )

    args = parser.parse_args()

    api_key = load_api_key()

    prompt = build_pizarra_prompt(
        args.concept,
        aspect=args.aspect,
        include_text=not args.no_text,
        accent=args.accent,
    )

    print("Generating pizarra image...", file=sys.stderr)
    print(f"  Concept: {args.concept[:80]}{'...' if len(args.concept) > 80 else ''}", file=sys.stderr)
    print(f"  Aspect:  {args.aspect}", file=sys.stderr)
    print(f"  Text:    {'yes' if not args.no_text else 'no'}", file=sys.stderr)
    print(f"  Accent:  {args.accent}", file=sys.stderr)

    image_bytes = call_openai(api_key, prompt, args.model, args.aspect, args.quality)

    if not args.no_pad:
        image_bytes = strip_gray_bands(image_bytes)
        image_bytes = force_aspect_ratio(image_bytes, args.aspect)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_bytes)

    size_kb = len(image_bytes) / 1024
    final_img = Image.open(BytesIO(image_bytes))
    print(
        f"\nOK Saved: {output_path.resolve()} "
        f"({size_kb:.1f} KB, {final_img.size[0]}x{final_img.size[1]})",
        file=sys.stderr,
    )
    print(str(output_path))


if __name__ == "__main__":
    main()
