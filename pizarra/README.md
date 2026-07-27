# Pizarra — Skill de imágenes whiteboard / sketchnote

Genera imágenes con look de pizarra dibujada a mano (marker negro, fondo blanco, ilustraciones simples, texto manuscrito, acentos limitados de color) usando **OpenAI `gpt-image-1`**.

Pensada para presentaciones donde quieres **explicar** un concepto a alguien (jefe, equipo, cliente educativo). NO es para storytelling polished tipo agencia (eso es `gravity-deck`) ni para imágenes libres/fotos (eso es `image-generation`).

## Triggers

La skill se activa cuando dices algo como:
- "Imagen estilo pizarra de X"
- "Sketchnote para explicar X"
- "Imagen whiteboard de X"
- "Hazme un doodle explicando X"
- "Imagen para que mi jefe entienda X"
- "Estilo hand-drawn / dibujo a mano"

## Setup (una sola vez)

### 1. API key de OpenAI

El script busca la key en este orden: variable de entorno → `~/.claude/.env` → `.env` de
la carpeta actual. Lo más cómodo es dejarla fija en `~/.claude/.env`:

```bash
echo 'OPENAI_API_KEY=sk-...' >> ~/.claude/.env
```

O exportarla en la sesión del shell:

```bash
export OPENAI_API_KEY="sk-..."
```

### 2. Dependencias Python

```bash
pip install -r requirements.txt
```

(Necesitas `requests` y `Pillow` — Pillow se usa para forzar el aspect ratio 16:9 con padding blanco si el modelo no respeta el ratio nativamente.)

### 3. Verificar

```bash
python scripts/generate_pizarra.py \
  --concept "test smiley face en pizarra" \
  --output /tmp/test-pizarra.png
```

Si sale el PNG → todo OK.

## Costo

Se factura a la cuenta de OpenAI dueña de la key (la misma que `image-generation`). `--quality medium`
cuesta centavos por imagen; `--quality high` unas 3x más. Para diagramas de deck, `medium` basta.

## Limitaciones conocidas

1. **Texto manuscrito puede tener typos:** los modelos de imagen escriben texto con errores ortográficos ocasionalmente. `gpt-image-1` es bastante bueno en esto, pero **igual hay que revisar el PNG siempre**. Si sale mal: regenerar, o usar `--no-text` y poner el texto encima en el deck.

2. **Aspect ratio por padding:** `gpt-image-1` solo entrega lienzos `1024x1024` y `1536x1024`. La skill pide el más cercano y Pillow rellena con blanco hasta el ratio exacto. Un 16:9 sale como `1820x1024` — es lo esperado.

## Ver también

- [SKILL.md](SKILL.md) — Instrucciones para el agente
- [scripts/generate_pizarra.py](scripts/generate_pizarra.py) — Script de generación
