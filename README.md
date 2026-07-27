# Skills de presentaciones Gravity — instalación

Cuatro skills de Claude Code para producir presentaciones con la marca Gravity
(paleta navy `#051367` + verde `#004714`, Montserrat/Open Sans, logo oficial) y las
imágenes que las acompañan.

| Skill | Qué hace | Necesita |
|---|---|---|
| **gravity-deck** | Decks en HTML (animados, se abren en el navegador, se publican con URL o se exportan a PDF) | Nada extra |
| **gravity-pptx** | PowerPoint `.pptx` editable, mismo diseño | Python 3.10+ |
| **image-generation** | Genera o edita imágenes con IA (fondos, ilustraciones, visuales para slides) | Python 3.10+ y API key de OpenAI |
| **pizarra** | Diagramas estilo pizarra dibujada a mano, para explicar conceptos | Python 3.10+ y API key de OpenAI |

## 0. Descargar

Botón verde **Code → Download ZIP** arriba en esta página, y descomprimir. O por consola:

```bash
git clone https://github.com/jttriana86/gravity-presentation-skills.git
cd gravity-presentation-skills
```

## 1. Instalar las skills

Copiar las cuatro carpetas dentro de la carpeta de skills de Claude Code:

**macOS / Linux**
```bash
mkdir -p ~/.claude/skills
cp -r gravity-deck gravity-pptx image-generation pizarra ~/.claude/skills/
chmod +x ~/.claude/skills/gravity-deck/scripts/*.sh
```

**Windows (PowerShell)**
```powershell
mkdir "$env:USERPROFILE\.claude\skills" -Force
Copy-Item gravity-deck,gravity-pptx,image-generation,pizarra "$env:USERPROFILE\.claude\skills\" -Recurse
```

Debe quedar así (el `SKILL.md` tiene que estar directamente dentro de cada carpeta):

```
~/.claude/skills/
├── gravity-deck/SKILL.md
├── gravity-pptx/SKILL.md
├── image-generation/SKILL.md
└── pizarra/SKILL.md
```

Reiniciar Claude Code después de copiarlas.

## 2. Dependencias de Python (solo para pptx e imágenes)

```bash
pip install python-pptx lxml Pillow requests
```

En Windows, si `pip` no responde, usar `py -m pip install ...`.

## 3. API key de OpenAI (solo para las dos skills de imágenes)

Las skills `image-generation` y `pizarra` generan las imágenes con el modelo
`gpt-image-1` de OpenAI, y se facturan a la cuenta dueña de la key. **Hay que poner una
key propia** — se saca en https://platform.openai.com/api-keys.

```bash
echo 'OPENAI_API_KEY=sk-...' >> ~/.claude/.env
```

En Windows, crear el archivo `%USERPROFILE%\.claude\.env` con esa misma línea dentro.

Costo aproximado por imagen: `--quality medium` ≈ USD 0.06, `--quality high` ≈ USD 0.25.
`gravity-deck` y `gravity-pptx` no consumen nada de esto.

## 4. Cómo se usan

No hay comandos que memorizar: se le pide a Claude en lenguaje normal y él carga la
skill que corresponda.

- *"Hazme un deck estilo Gravity para el pitch de [cliente], con estas métricas..."*
- *"Necesito el reporte mensual de [cliente] en PowerPoint editable, estilo Gravity"*
- *"Genera una imagen de fondo abstracta navy para la portada del deck"*
- *"Hazme una imagen estilo pizarra que explique cómo funciona [X]"*

Regla práctica: **HTML** (`gravity-deck`) cuando la presentación la maneja uno mismo y
quiere impacto; **PPTX** (`gravity-pptx`) cuando el cliente o el equipo tiene que editarla
después.

## 5. Verificar que quedó bien

```bash
# PPTX: genera un deck de ejemplo
python3 ~/.claude/skills/gravity-pptx/scripts/build_deck.py \
  ~/.claude/skills/gravity-pptx/examples/corponovo-agosto.json /tmp/prueba.pptx

# Imágenes: genera un PNG de prueba
python3 ~/.claude/skills/image-generation/scripts/generate_image.py \
  --prompt "A simple blue paper airplane on white background" \
  --aspect 16:9 --quality low --output /tmp/prueba.png
```

Si los dos archivos se crean, todo está listo.

## Notas

- El diseño no es negociable dentro de las skills: fondo claro, navy dominante, verde solo
  para datos positivos, rojo solo para lo crítico, logo oficial de Gravity siempre presente.
  Está documentado en el `SKILL.md` y en `references/brand-palette.md` de cada skill.
- `gravity-deck` incluye scripts para publicar el deck en Vercel y exportarlo a PDF
  (`scripts/deploy.sh` / `deploy.ps1`, `scripts/export-pdf.sh` / `export-pdf.ps1`). Requieren
  Node.js y una cuenta de Vercel; son opcionales.
- Las skills están en español y pensadas para Gravity; se pueden editar libremente,
  son archivos de texto plano.
