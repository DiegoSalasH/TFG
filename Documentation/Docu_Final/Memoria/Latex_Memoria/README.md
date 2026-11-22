# Memoria del TFG en LaTeX

## Estructura

| Fichero | Contenido |
|---|---|
| `main.tex` | Plantilla: paquetes, portada, resúmenes, índices automáticos y orden de los capítulos |
| `capitulos/01_contexto.tex` … `05_sostenibilidad.tex` | Un fichero por capítulo |
| `bibliografia.tex` | Bibliografía (`thebibliography`, claves `ref01`…`ref41`) |
| `imagenes/` | Logos, PERT y Gantt. Los diagramas nuevos salen de `generadores/` |
| `compilar.sh` | Compila el PDF y, con `--docx`, también un .docx |

## Compilar

Desde Git Bash (Windows) o bash (Linux):

```bash
./compilar.sh          # PDF  -> ../Memoria_TFG_Diego_Salas.pdf
./compilar.sh --docx   # PDF y .docx -> ../Memoria_TFG_Diego_Salas_desde_latex.docx
```

También se puede compilar a mano con `tectonic main.tex` desde esta carpeta. La primera vez, Tectonic descarga los paquetes que necesita (hace falta Internet); las siguientes funciona sin conexión. En VS Code, la extensión LaTeX Workshop muestra el PDF y los errores.

## Convenciones

- **Referencias cruzadas.** Nunca escribas «Tabla 12» o «apartado 4.5» a mano: usa `Tabla~\ref{tab:12}` y `apartado~\ref{sec:4-5}`. Las etiquetas siguen el número de la versión de la memoria convertida (`tab:N`, `fig:N`, `sec:X-Y-Z`). Si añades una tabla nueva, ponle una etiqueta con nombre, por ejemplo `tab:actores`.
- **Citas.** Usa `\cite{ref12}`. Las entradas nuevas se añaden al final de `bibliografia.tex` con la siguiente clave libre.
- **Tablas.** Se escriben con `table` + `tabularx` + `booktabs`, con la cabecera en gris (`\rowcolor{cabeceratabla}`) y el pie debajo con `\caption` y `\label`. Copia el formato de una tabla existente.
- **Pendientes.** `\pendiente{texto}` marca en rojo lo que falta por hacer, y `\figurapendiente{texto}` reserva el hueco de una figura. Antes de entregar, busca `\pendiente` y comprueba que no quede ninguno.
- **Apartados revisados.** Cuando la directora dé un apartado por cerrado, envuélvelo en `\begin{apartadoterminado} … \end{apartadoterminado}` y no lo toques sin consultarlo.
- **Google Doc.** El `.tex` es la fuente. El Google Doc es la copia en la que comenta la directora: cada cambio del `.tex` se aplica también, localizado, en el Doc, sin regenerarlo entero, para no perder los comentarios.

## Origen

La primera versión se generó automáticamente a partir del .docx exportado del Google Doc, con `trabajo_en_curso/week5/latex/convertir.py` (19/11/2026, a partir de la exportación del 16/11/2026). **No vuelvas a ejecutar ese script**: sobrescribiría los capítulos. Desde ahora se edita el `.tex` directamente.
