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
