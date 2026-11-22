# Progreso: paso de la memoria a LaTeX

Encargado el 19/11/2026. Instrucción del estudiante: hacer el LaTeX **sin subir nada a GitHub**; él lo subirá cuando esté terminado.

## Datos de partida

| Elemento | Valor |
|---|---|
| Fuente | Google Doc «Memória» (id `1VUixy-IEbLYGgAHP5kmElUfnJ_S56SKuhgdh0KhJblg`), exportado a `Documentation/Docu_Final/Memoria/Memoria_TFG_Diego_Salas.docx` |
| Destino | `Documentation/Docu_Final/Memoria/Latex_Memoria/` (`main.tex`, `capitulos/`, `bibliografia.bib`, `imagenes/`, `compilar.sh`) |
| Conversor | `trabajo_en_curso/week5/latex/convertir.py`: lee el AST JSON de Pandoc y escribe el LaTeX (títulos sin la numeración manual, tablas con booktabs y tabularx, pies con `\caption` y `\label`, citas con `\cite`) |
| Compilación | `tectonic main.tex`, desde la carpeta `Latex_Memoria` |

## Herramientas

- [x] Pandoc 3.14 (`%LOCALAPPDATA%\Pandoc\pandoc.exe`, instalado con winget)
- [x] Tectonic 0.17.0 (`%LOCALAPPDATA%\Programs\Tectonic\tectonic.exe`, en el PATH del usuario)
- [x] Extensión de VS Code LaTeX Workshop 10.14.0
- [x] Python 3.12.10 con el `requirements.txt` del repositorio

## Pasos

- [x] 1. Exportar el AST de Pandoc y extraer las imágenes (`imagenes/`: `logo_upc_fib.png`, `logo_fib.png`, `pert.png`, `gantt.png`)
- [x] 2. Plantilla `main.tex` (portada FIB, babel, geometry, booktabs, hyperref, índices automáticos)
- [x] 3. Conversor: títulos, párrafos, listas, negrita/cursiva y enlaces
- [x] 4. Conversor: tablas (`xltabular` + booktabs, cabecera gris) con `\caption` y `\label`
- [x] 5. Conversor: figuras (PERT, Gantt) y marcadores de las Figuras 3 y 4 (`\figurapendiente`)
- [x] 6. Bibliografía (`thebibliography`, claves `ref01`–`ref41`) y citas `[n]` convertidas a `\cite`
- [x] 7. Referencias cruzadas («Tabla N», «Figura N», «apartado X») convertidas a `\ref`
- [x] 8. Primera compilación con Tectonic sin errores (51 páginas; 0 referencias y 0 citas sin resolver)
- [x] 9. Revisión visual del PDF y corrección de defectos (55 páginas revisadas en hojas de contacto con PyMuPDF)
- [x] 10. `compilar.sh` (PDF y, con `--docx`, .docx con Pandoc) y `README.md` de la carpeta

**Estado: conversión terminada el 19/11/2026. No se ha subido nada a GitHub** (lo subirá el estudiante).

## Comprobaciones ejecutadas

| Comprobación | Resultado |
|---|---|
| Compilación con Tectonic 0.17.0 | Sin errores; 55 páginas |
| Referencias `\ref` sin resolver | 0 |
| Citas `\cite` sin resolver | 0 |
| Caracteres que faltan en la fuente | 0 |
| Cajas que se salen del margen | 2, de menos de 1 pt (no se ven) |
| Revisión visual | Portada, índices, los 5 capítulos y la bibliografía; sin cabeceras sueltas ni títulos separados de su tabla |
| `./compilar.sh --docx` | Genera `Memoria_TFG_Diego_Salas.pdf` y `Memoria_TFG_Diego_Salas_desde_latex.docx` |

## Pendiente (de contenido, no de la conversión)

- [ ] Figuras 3 y 4: generarlas con `generadores/` (casos de uso y modelo conceptual) y cambiar `\figurapendiente` por `\includegraphics`.
- [ ] Referencias [31]–[33]: el estudiante debe confirmar las fuentes propuestas (marcadas en rojo en la bibliografía).
- [ ] Resum, Resumen y Summary: están vacíos (marcados en rojo).
- [ ] Portada: sigue diciendo «GEP · Entregable 4» y «Fecha prevista de entrega: 12 de octubre de 2026».
- [x] D-07: el `.tex` es la fuente desde el 22/11/2026; el Google Doc es la copia para los comentarios.
- [ ] Opcional: pasar la bibliografía a `bibliografia.bib` (BibTeX, estilo IEEEtran).

## Problemas encontrados y decisiones

- **Estructura del AST de Pandoc.** Contiene 105 títulos (muchos vacíos, se descartan), 41 tablas (la primera es la de la portada, que se rehace en la plantilla), 2 imágenes de contenido y la bibliografía como un único `BlockQuote` con una entrada por párrafo (bloque 360). Los índices, la portada y los resúmenes del Doc (bloques 0–76) no se convierten: la plantilla los genera.
- **Bibliografía con `thebibliography`.** Se usa `thebibliography` con claves `refNN`, conservando el texto exacto de cada entrada, en lugar de pasarla a `.bib`. Así no hay que reinterpretar 41 entradas con formatos distintos. Pasar a BibTeX queda como mejora posterior.
- **Referencias [31]–[33].** Se citan en el texto pero no están en la bibliografía del Doc. Se añaden las fuentes propuestas (Cornell, BatOnRoute, Educación 3.0), marcadas como «pendiente de confirmar».
- **Contenido sin cambios.** La conversión no cambia el contenido: la portada (que sigue diciendo «Entregable 4») y los resúmenes vacíos se mantienen tal cual y quedan señalados como pendientes.
