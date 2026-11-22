# Decisiones (Week 5)

Fuente única de las decisiones del proyecto. Cada decisión tiene un ID (`D-NN`). Si una decisión corrige otra, lo dice expresamente («corrige D-NN»).

---

## D-01 · Gestión de GitHub desde la web

- **Problema:** hay que crear issues, milestones y etiquetas sin tener `gh` instalado.
- **Opciones:** (a) instalar `gh` y gestionarlo desde la terminal; (b) gestionarlo desde la web de GitHub.
- **Decisión:** (b). El estudiante crea issues, milestones y etiquetas en la web, con el texto preparado de antemano.
- **Justificación:** preferencia del estudiante; así no hace falta instalar ni autenticar `gh`.
- **Cambios aplicados:** ninguno en el repositorio.
- **Validación:** después de crearlos, se revisan con la API pública de GitHub.

## D-02 · Repositorio público

- **Problema:** el repositorio contiene la memoria y los entregables GEP.
- **Opciones:** (a) privado durante el TFG; (b) público.
- **Decisión:** (b) público.
- **Justificación:** decisión del estudiante. El repositorio solo contiene documentación y datos sintéticos, nunca datos reales de menores (ver README).
- **Cambios aplicados:** ninguno.
- **Validación:** el `.gitignore` excluye volcados `.sql` y salidas de pruebas.

## D-03 · Diagramas generados con Pillow y la fuente Lora

- **Problema:** las Figuras 3 y 4 de la memoria están pendientes, y los diagramas tienen que poder regenerarse cuando cambie el modelo.
- **Opciones:** (a) dibujarlos a mano con una herramienta gráfica; (b) PlantUML o Mermaid; (c) scripts de Python con Pillow.
- **Decisión:** (c). Un script `gen_*.py` por diagrama y un estilo común en `generadores/estilo.py`.
- **Justificación:** se pueden regenerar, quedan versionados y tienen un estilo uniforme. Lora es la tipografía de la memoria, y los `.ttf` (licencia OFL) van incluidos en `generadores/fuentes/`, así que funcionan igual en Windows y en Linux.
- **Cambios aplicados:** `generadores/estilo.py`, `generadores/README.md` y `generadores/fuentes/`.
- **Validación:** se generó una imagen de prueba fuera del repositorio con negrita, cursiva, tildes, cajas y flechas, y se revisó visualmente.

## D-04 · Entorno: Python en Windows y SuiteCRM en WSL2

- **Problema:** hacen falta Python para los generadores y un servidor para SuiteCRM 8.
- **Opciones:** (a) todo en Windows (XAMPP); (b) Python en Windows y SuiteCRM en WSL2 con Ubuntu; (c) Docker Desktop.
- **Decisión:** (b).
- **Justificación:** SuiteCRM está pensado para Linux, y el equipo ya tiene Ubuntu 24.04 en WSL2. Con Docker habría que instalar otra capa más, y el equipo tiene 8 GB de RAM.
- **Cambios aplicados:** Python 3.12.10 instalado en Windows y `requirements.txt` con las versiones mínimas probadas.
- **Validación:** `pip install -r requirements.txt` terminó sin errores.

## D-05 · Paso de la memoria a LaTeX

- **Problema:** el estudiante quiere la memoria en LaTeX. Convertir desde el PDF pierde la estructura (títulos, tablas, listas).
- **Opciones:** (a) convertir el PDF; (b) convertir el .docx exportado del Google Doc con Pandoc (`-t latex`) y retocar a mano; (c) leer el AST JSON de Pandoc con un conversor propio.
- **Decisión:** (c), con `trabajo_en_curso/week5/latex/convertir.py`.
- **Justificación:** controla de forma sistemática lo que más trabajo daría a mano en 40 tablas y 41 referencias: quitar la numeración escrita en los títulos, pasar las tablas a booktabs con pie y etiqueta, convertir las citas `[n]` a `\cite` y las referencias «Tabla N» o «apartado X» a `\ref`.
- **Cambios aplicados:** `Documentation/Docu_Final/Memoria/Latex_Memoria/` (`main.tex`, 5 capítulos, `bibliografia.tex`, `imagenes/`, `compilar.sh`, `README.md`).
- **Validación:** compila con Tectonic 0.17.0 sin errores, sin referencias ni citas sin resolver, sin caracteres que falten y con 2 avisos de caja de menos de 1 pt. Se revisaron visualmente las páginas.

## D-06 · Formato del LaTeX

- **Problema:** hay que decidir cómo se numeran y se colocan tablas y figuras, y cómo se trata la bibliografía.
- **Decisión:**
  - Tablas y figuras con numeración global (Tabla 1–40), como en el Google Doc, para que las dos versiones coincidan.
  - Tablas como bloque que no se parte y que se queda en su sitio (`table[H]` + `tabularx`). Cuando un título va justo antes de una tabla, se reserva espacio con `\needspace` para que no quede solo al pie de la página.
  - Bibliografía con `thebibliography`, conservando el texto exacto de cada entrada; pasar a BibTeX queda como mejora opcional.
  - Fuente Latin Modern, la que usa fontspec por defecto. Lora no se usa en el PDF porque Tectonic no admite bien fuentes variables.
- **Justificación:** con `xltabular` aparecían cabeceras sueltas y pies separados de su tabla; ninguna tabla supera una página.
- **Cambios aplicados:** `main.tex` y `convertir.py`.
- **Validación:** revisión visual de las 55 páginas.

## D-07 · Fuente del contenido a partir de ahora

- **Problema:** la memoria existe a la vez en el Google Doc y en el `.tex`.
- **Decisión:** el `.tex` es la fuente de la memoria desde el 22/11/2026 (confirmado por el estudiante). El Google Doc queda como copia donde comenta la directora: cada cambio del `.tex` se replica, localizado, en el Doc, sin regenerarlo entero. `convertir.py` no se vuelve a ejecutar.
- **Cambios aplicados:** `README.md` de `Latex_Memoria` (apartados «Convenciones» y «Origen»).
- **Validación:** —.
