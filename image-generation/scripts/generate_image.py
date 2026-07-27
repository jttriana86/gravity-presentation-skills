#!/usr/bin/env python3
"""
Image generator / editor — OpenAI Images API (gpt-image-1).

Text-to-image and image editing. Portable: no hardcoded machine paths.

Usage:
  python generate_image.py --prompt "..." --output ./assets/foo.png
  python generate_image.py --prompt "..." --output ./foo.png --aspect 16:9 --quality high
  python generate_image.py --prompt "add a rainbow" --image ./photo.png --output ./out.png

Requirements:
  - pip install requests
  - OPENAI_API_KEY: environment variable, or a line OPENAI_API_KEY=... in
    ~/.claude/.env or in a .env file of the current directory.
"""

import argparse
import base64
import mimetypes
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: missing dependency 'requests'. Install: pip install requests", file=sys.stderr)
    sys.exit(1)


GENERATIONS_URL = "https://api.openai.com/v1/images/generations"
EDITS_URL = "https://api.openai.com/v1/images/edits"
DEFAULT_MODEL = "gpt-image-1"

# gpt-image-1 only accepts these canvas sizes.
SIZES = {
    "1:1": "1024x1024",
    "16:9": "1536x1024",
    "9:16": "1024x1536",
}

ENV_CANDIDATES = [
    Path.home() / ".claude" / ".env",
    Path.cwd() / ".env",
]


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


def decode_response(data: dict) -> bytes:
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


def generate(api_key: str, prompt: str, model: str, size: str, quality: str) -> bytes:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model, "prompt": prompt, "size": size, "quality": quality, "n": 1}

    print(f"  -> POST {GENERATIONS_URL} (model {model}, size {size}, quality {quality})", file=sys.stderr)
    r = requests.post(GENERATIONS_URL, json=payload, headers=headers, timeout=300)
    if r.status_code != 200:
        print(f"ERROR: OpenAI returned {r.status_code}", file=sys.stderr)
        print(f"Response: {r.text[:800]}", file=sys.stderr)
        sys.exit(2)
    return decode_response(r.json())


def edit(api_key: str, prompt: str, model: str, size: str, quality: str, image_path: Path) -> bytes:
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"model": model, "prompt": prompt, "size": size, "quality": quality, "n": "1"}

    # The API only accepts png / jpeg / webp, and rejects a generic mimetype.
    mime = mimetypes.guess_type(image_path.name)[0]
    if mime not in ("image/png", "image/jpeg", "image/webp"):
        print(f"ERROR: unsupported input image '{image_path.name}'. Use .png, .jpg or .webp", file=sys.stderr)
        sys.exit(1)

    print(f"  -> POST {EDITS_URL} (editing {image_path.name})", file=sys.stderr)
    with image_path.open("rb") as fh:
        files = {"image": (image_path.name, fh, mime)}
        r = requests.post(EDITS_URL, data=data, files=files, headers=headers, timeout=300)

    if r.status_code != 200:
        print(f"ERROR: OpenAI returned {r.status_code}", file=sys.stderr)
        print(f"Response: {r.text[:800]}", file=sys.stderr)
        sys.exit(2)
    return decode_response(r.json())


def main():
    parser = argparse.ArgumentParser(description="Generate or edit an image with OpenAI gpt-image-1")
    parser.add_argument("--prompt", required=True, help="What to generate, or how to edit the input image")
    parser.add_argument("--output", required=True, help="Path to save the PNG (e.g. ./assets/foo.png)")
    parser.add_argument("--aspect", default="1:1", choices=list(SIZES.keys()), help="Aspect ratio (default: 1:1)")
    parser.add_argument("--quality", default="medium", choices=["low", "medium", "high"], help="Render quality / cost (default: medium)")
    parser.add_argument("--image", help="Path to an existing image to edit instead of generating from scratch")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"OpenAI image model (default: {DEFAULT_MODEL})")

    args = parser.parse_args()

    api_key = load_api_key()
    size = SIZES[args.aspect]

    print("Generating image...", file=sys.stderr)
    print(f"  Prompt: {args.prompt[:90]}{'...' if len(args.prompt) > 90 else ''}", file=sys.stderr)

    if args.image:
        image_path = Path(args.image)
        if not image_path.is_file():
            print(f"ERROR: input image not found: {image_path}", file=sys.stderr)
            sys.exit(1)
        image_bytes = edit(api_key, args.prompt, args.model, size, args.quality, image_path)
    else:
        image_bytes = generate(api_key, args.prompt, args.model, size, args.quality)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_bytes)

    print(f"\nOK Saved: {output_path.resolve()} ({len(image_bytes) / 1024:.1f} KB)", file=sys.stderr)
    print(str(output_path))


if __name__ == "__main__":
    main()
