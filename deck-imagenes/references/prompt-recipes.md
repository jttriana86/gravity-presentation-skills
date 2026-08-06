# Recetas de prompt

El `--concept` es lo único que escribís vos; el script le pega la receta del estilo, el hex
de la marca y las guardas. Este archivo es para afinar ese concepto.

## Cómo derivar el concepto del slide

No describas la imagen que imaginás: describí **la escena o el objeto** del que habla el
slide. El estilo lo pone `--style`.

| El slide dice… | Mal concepto | Buen concepto |
|---|---|---|
| "Crecimos 150% en Facebook" | "gráfico de crecimiento con flecha verde" | "activación de marca en un evento al aire libre, gente con el celular en alto" |
| "Nuestro proceso de onboarding" | "proceso de onboarding" | "recorrido de un cliente: primer contacto, reunión de arranque, entrega" (con `--style pizarra`) |
| "Somos un equipo senior" | "equipo profesional sonriendo" | "tres personas discutiendo frente a una pizarra con post-its, luz de ventana" |
| "Automatización con IA" | "robot con inteligencia artificial" | "formas geométricas conectadas en flujo, una nodo destaca" (con `--style illustration`) |

Reglas:
- **Concreto vence a abstracto.** "Reunión de comité" da mejor imagen que "gobernanza".
- **Una idea por imagen.** Si el concepto tiene dos frases con "y", partilo en dos imágenes.
- **Nada de conceptos que exigen texto** (dashboards legibles, documentos, letreros): las
  guardas prohíben el texto y el modelo termina inventando garabatos.

## Ajustes finos con `--extra`

```bash
--extra "cámara a la altura de los ojos, sin mirar al lente"
--extra "vista cenital sobre una mesa de madera clara"
--extra "espacio vacío en el tercio derecho para poner texto encima"
```

El último es el más útil con `--pattern hero`: reserva la zona donde va el título.

## Personas

- Pedí **actitud**, no belleza: "concentrados en la pantalla", "una explica y dos escuchan".
- Colombia / LatAm: decilo explícito ("oficina en Bogotá, gente latinoamericana") o el modelo
  default se va a un genérico estadounidense.
- Nunca pidas una persona real, ni "estilo de [fotógrafo]".

## Diagramas (`--style pizarra`)

- Enumerá los pasos en orden: "formulario → llamada del agente → agenda → cierre".
- Máximo 5 nodos. Con más, el sketch se vuelve ilegible al tamaño de un slide.
- Sale sin texto: las etiquetas de cada paso las ponés vos en HTML/PPTX alrededor de la imagen,
  o dejás que la figura hable sola con el `--caption`.

## Costo

`medium` ≈ USD 0.06 por imagen; `high` ≈ USD 0.25. Un deck de 10 slides con 3 imágenes en
medium cuesta ~USD 0.18. Usá `high` solo para la portada de una propuesta importante.

Antes de gastar, `--dry-run` te muestra el prompt final armado.
