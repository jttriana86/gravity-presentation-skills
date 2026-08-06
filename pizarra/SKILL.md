---
name: pizarra
description: Genera imágenes estilo whiteboard / sketchnote (pizarra hand-drawn con marker, ilustraciones simples, texto manuscrito y acentos naranja/verde/amarillo) para presentaciones explicativas o didácticas. Usar cuando el usuario pida "imagen estilo pizarra", "sketchnote", "explicar con muñequitos", "imagen whiteboard", "doodle explicativo", "imagen para explicar X a mi jefe", "estilo hand-drawn", "imagen tipo dibujo a mano" o "infografía dibujada". NO confundir con `gravity-deck` (presentaciones polished para clientes) ni con `image-generation` (imágenes libres, cualquier estilo). Genera el PNG en aspect ratio 16:9 estricto (con padding blanco si hace falta) y lo guarda en la ruta indicada para que el usuario lo inserte manualmente en su deck/PPTX/Slack.
allowed-tools: [Bash, Write, Read]
---

# Pizarra — Generador de imágenes whiteboard / sketchnote

Skill para producir imágenes con look de pizarra dibujada a mano: trazos wobbly de marker negro sobre fondo blanco, ilustraciones simples (personajes, flechas, libretas, iconos), texto manuscrito en español y acentos limitados de color (naranja / verde / amarillo).

Pensada para presentaciones donde el usuario quiere **explicar** un concepto a alguien (jefe, equipo, cliente educativo) — NO para storytelling polished tipo agencia.

## Cuándo usar esta skill

| Usar | NO usar |
|------|---------|
| Explicar un concepto técnico a un no-técnico | Pitch a cliente importante (usar `gravity-deck`) |
| Sketchnotes para enseñar o entrenar | Imagen libre / foto / fondo (usar `image-generation`) |
| Slides educativas internas | Reportes formales con datos duros |
| Memes de explicación didáctica | Marketing brand-forward |

## Instrucciones para el Agente

### 1. Generación

> **Motor: OpenAI `gpt-image-1`.** La key es `OPENAI_API_KEY` y el script la busca en
> este orden: variable de entorno → `~/.claude/.env` → `.env` de la carpeta actual.
> Si el script se queja de que falta la key, es un problema de configuración
> (ver README.md), no del modelo.

```bash
python3 ~/.claude/skills/pizarra/scripts/generate_pizarra.py \
  --concept "Cómo funciona un agente de WhatsApp con IA: usuario manda mensaje, webhook lo recibe, Claude responde, se guarda en Supabase" \
  --output ./assets/pizarra/agente-wa.png \
  --aspect 16:9
```

### 2. Parámetros del script

- `--concept` (requerido): qué se quiere explicar. Sé específico sobre los elementos visuales y los conceptos a conectar.
- `--output` (requerido): ruta del PNG de salida. Crear carpetas si no existen.
- `--aspect` (opcional): `16:9` (default, slides), `1:1` (Slack/post), `4:3` (presentaciones viejas).
- `--no-text` (opcional, flag): si se pasa, pide a la IA que NO meta texto en la imagen (solo ilustraciones). Default: SÍ intenta meter texto manuscrito.
- `--accent` (opcional): colores de acento. Default: `orange,green,yellow`. Para look más sobrio: `black-only`. Para que combine con un deck Gravity (navy): `green`.
- `--quality` (opcional): `low` / `medium` / `high`. Default: `medium` (buen trazo, costo bajo).
- `--model` (opcional): modelo de imagen de OpenAI. Default: `gpt-image-1`.

**Nota de tamaños:** `gpt-image-1` solo acepta lienzos `1024x1024` y `1536x1024`. El script pide el más cercano y luego Pillow lo rellena con blanco hasta el aspect ratio exacto que pediste. Por eso `16:9` sale como `1820x1024`, no como `1920x1080` — es correcto y no hay que arreglarlo.

### 3. Convenciones

- Guardar siempre en una carpeta dedicada del proyecto, ej: `assets/pizarra/`, `public/pizarra/`, o `imagenes-explicativas/`.
- Nombres en kebab-case ASCII, sin acentos. Ej: `agente-whatsapp.png`, `flujo-webhook.png`.
- Aspect ratio 16:9 garantizado por post-process con Pillow (padding blanco si la IA falla en respetar el ratio).

### 4. Bandas grises del modelo (auto-fix)

A veces el modelo devuelve la sketch enmarcada por bandas grises sólidas (RGB ~111) en lugar de blanco puro. Eso se nota feo cuando la imagen va sobre fondo blanco de una slide.

El script ya las detecta y recorta automáticamente antes del padding de aspect ratio (`strip_gray_bands` en `generate_pizarra.py`). No hay que hacer nada manual. Si necesitas saltarte ese paso usa `--no-pad`.

### 5. Prompt wrapping

El script envuelve automáticamente el `--concept` con guías de estilo whiteboard. NO duplicar las instrucciones de estilo en el concept — solo describir QUÉ se quiere mostrar y QUÉ conceptos conectar.

**Ejemplo correcto:**
```
--concept "Tres pasos para deployar a Vercel: 1) git push, 2) Vercel detecta cambios, 3) preview URL lista. Conectados con flechas."
```

**Ejemplo incorrecto (redundante):**
```
--concept "Hand-drawn marker sketch, white background, with three steps for Vercel deploy..."  ❌
```

### 5. Sobre el texto manuscrito

Los modelos de imagen tienen problemas conocidos de ortografía cuando intentan escribir texto. Esperable:
- Letras invertidas o mal formadas ocasionalmente
- Typos en palabras largas o con acentos
- "WhatsApp" puede salir como "WhatSAPP", "Satisfecho" como "Satisfchto"

**Estrategia:** generar con texto, revisar visualmente, regenerar si los typos son inaceptables, o usar `--no-text` y agregar texto encima en el deck con HTML/PPTX.

## Costo

Se factura a la cuenta de OpenAI dueña de la key (la misma que usa la skill `image-generation`).
Orden de magnitud por imagen 16:9: `--quality medium` centavos; `--quality high` unas 3x más.
Para diagramas de deck, `medium` es suficiente — no subir a `high` sin razón.

## Estructura típica de un concept bien formulado

```
[QUÉ se muestra] + [LOS ELEMENTOS visuales] + [CÓMO se conectan] + [TÍTULO opcional]
```

Ejemplo:
```
"Flujo de webhook de WhatsApp en Next.js. Mostrar: smartphone con burbuja
de WhatsApp, flecha hacia un servidor (caja con engranaje), flecha hacia
una base de datos (cilindro), flecha de regreso al smartphone. Título
arriba: 'CÓMO LLEGA UN MENSAJE'."
```

## Ejemplo de flujo completo

**Usuario:** *"Hazme una imagen pizarra que explique cómo funciona prompt caching en Claude API para mi presentación a mi jefe."*

**Agente:**
1. Decide la estructura visual: 2 escenarios comparados (sin caching vs con caching)
2. Ejecuta:
   ```bash
   python ~/.claude/skills/pizarra/scripts/generate_pizarra.py \
     --concept "Comparativa de prompt caching en Claude API. Lado izquierdo: 'SIN CACHING' con un robot leyendo un libro grande lleno de texto, signo de dólar grande $$$ y reloj con tiempo largo. Lado derecho: 'CON CACHING' con el mismo robot pero el libro está en una nube etiquetada CACHE, signo de dólar pequeño $ y reloj con tiempo corto. Una flecha gigante entre los dos escenarios mostrando la mejora. Título arriba: 'PROMPT CACHING = 90% AHORRO'." \
     --output ./assets/pizarra/prompt-caching.png \
     --aspect 16:9
   ```
3. Verifica que el PNG se creó (`Read` o `ls`)
4. Reporta al usuario la ruta del archivo y previsualiza la imagen leyéndola

## Anti-patrones

| ❌ No hacer | ✅ Hacer |
|------------|---------|
| Pasar instrucciones de estilo en `--concept` | El script las inyecta automáticamente; solo describe el contenido |
| Pedir texto largo en la imagen (>4 palabras por línea) | Mantener texto corto, los modelos fallan con frases largas |
| Generar y olvidar revisar typos | Siempre `Read` el PNG después para verificar texto manuscrito |
| Guardar en root del proyecto | Usar carpeta dedicada (`assets/pizarra/`, etc.) |
| Insertar la imagen automáticamente en código | Esta skill solo GENERA; el usuario decide dónde meterla |
| Pedir aspect ratios raros (21:9, 9:16) | Usar 16:9, 1:1 o 4:3 — son los soportados |
| Mezclar el estilo pizarra con el estilo Gravity | Estilos incompatibles; usar la skill correcta para cada uno |

## Referencias

- [`scripts/generate_pizarra.py`](scripts/generate_pizarra.py) — Generador OpenAI `gpt-image-1` + post-process Pillow
- [`requirements.txt`](requirements.txt) — Dependencias Python (`requests`, `Pillow`)
- [`README.md`](README.md) — Setup inicial y troubleshooting
