"""Convierte la memoria (.docx exportado del Google Doc) a LaTeX.

Uso:
    python trabajo_en_curso/week5/latex/convertir.py

Pasos:
1. Ejecuta Pandoc para obtener el AST JSON del .docx (en el directorio temporal).
2. Recorre el AST y escribe un .tex por capítulo en
   Documentation/Docu_Final/Memoria/Latex_Memoria/capitulos/ y la bibliografía en
   Latex_Memoria/bibliografia.tex.

Es una herramienta de migración de un solo uso: cuando el .tex pase a ser la
fuente de la memoria, los cambios se hacen en el .tex y no se vuelve a
ejecutar este script (lo sobrescribiría).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DOCX = RAIZ / "Documentation" / "Docu_Final" / "Memoria" / "Memoria_TFG_Diego_Salas.docx"
DESTINO = RAIZ / "Documentation" / "Docu_Final" / "Memoria" / "Latex_Memoria"
PANDOC = Path(os.environ.get("LOCALAPPDATA", "")) / "Pandoc" / "pandoc.exe"

INICIO_CUERPO = "1. Contexto"          # primer título que se convierte
TITULO_BIBLIO = "Bibliografía"

IMAGENES = {  # orden de aparición de las imágenes de contenido -> fichero en imagenes/
    1: "pert.png",
    2: "gantt.png",
}

FICHEROS_CAPITULO = {
    1: "01_contexto.tex",
    2: "02_planificacion.tex",
    3: "03_presupuesto.tex",
    4: "04_especificacion.tex",
    5: "05_sostenibilidad.tex",
}

PENDIENTES_BIBLIO = {
    31: r"Cornell University, «Check-In/Check-Out Procedures», Cornell Youth Safety. [En línea]. Disponible: \url{https://youthsafety.cornell.edu/program-directors/check-incheck-out-procedures}.",
    32: r"BatOnRoute (Grupo Nunsys), «Student Attendance Control: Digital Solutions for a More Efficient Management», 29 de agosto de 2024. [En línea]. Disponible: \url{https://batonroute.com/en/blog/student-attendance-control-digital-solutions-efficient-management}.",
    33: r"Redacción Educación 3.0, «La recogida de los menores del colegio, con seguridad», Educación 3.0, 23 de enero de 2023. [En línea]. Disponible: \url{https://www.educaciontrespuntocero.com/noticias/recogida-qualla-kids/}.",
}

# --------------------------------------------------------------------------
# Escapado y texto en línea
# --------------------------------------------------------------------------
_ESCAPES = {
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
    "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    "≥": r"$\geq$", "≤": r"$\leq$", "Σ": r"$\Sigma$", "×": r"$\times$", "−": r"$-$",
    "→": r"$\rightarrow$", "<": r"\textless{}", ">": r"\textgreater{}", "\u00a0": "~",
}


def esc(s: str) -> str:
    return "".join(_ESCAPES.get(ch, ch) for ch in s)


def inline(inls, url_mode=False) -> str:
    out = []
    for x in inls:
        t = x["t"]
        c = x.get("c")
        if t == "Str":
            out.append(esc(c))
        elif t in ("Space", "SoftBreak"):
            out.append(" ")
        elif t == "LineBreak":
            out.append(r"\newline ")
        elif t == "Strong":
            out.append(r"\textbf{" + inline(c) + "}")
        elif t == "Emph":
            out.append(r"\textit{" + inline(c) + "}")
        elif t == "Underline":
            out.append(r"\underline{" + inline(c) + "}")
        elif t in ("Superscript",):
            out.append(r"\textsuperscript{" + inline(c) + "}")
        elif t in ("Subscript",):
            out.append(r"\textsubscript{" + inline(c) + "}")
        elif t in ("SmallCaps", "Strikeout"):
            out.append(inline(c))
        elif t == "Span":
            out.append(inline(c[1]))
        elif t == "Link":
            texto = inline(c[1])
            destino = c[2][0]
            if destino.startswith("http"):
                out.append(r"\href{" + destino.replace("%", r"\%").replace("#", r"\#") + "}{" + texto + "}")
            else:
                out.append(texto)
        elif t == "Quoted":
            out.append("«" + inline(c[1]) + "»")
        elif t == "Code":
            out.append(r"\texttt{" + esc(c[1]) + "}")
        elif t == "Image":
            out.append("")  # las imágenes se tratan a nivel de bloque
        elif t == "Note":
            out.append(r"\footnote{" + bloques_simples(c) + "}")
        else:
            out.append("")
    return "".join(out)


def plano(inls) -> str:
    """Texto plano (sin formato) de una lista de elementos en línea."""
    out = []
    for x in inls:
        t = x["t"]
        c = x.get("c")
        if t == "Str":
            out.append(c)
        elif t in ("Space", "SoftBreak", "LineBreak"):
            out.append(" ")
        elif t in ("Strong", "Emph", "Underline", "SmallCaps", "Strikeout", "Superscript", "Subscript"):
            out.append(plano(c))
        elif t in ("Span",):
            out.append(plano(c[1]))
        elif t in ("Link", "Quoted"):
            out.append(plano(c[1]))
        elif t == "Image":
            out.append("[IMG]")
    return "".join(out)


def bloques_simples(blocks) -> str:
    return " ".join(inline(b["c"]) for b in blocks if b["t"] in ("Para", "Plain"))


# --------------------------------------------------------------------------
# Citas y referencias cruzadas
# --------------------------------------------------------------------------
def clave(n: int) -> str:
    return f"ref{n:02d}"


def citas(s: str) -> str:
    """[n], [n]-[m], [n][m] y [n], [m] -> \\cite{...}."""
    def rango(m):
        a, b = int(m.group(1)), int(m.group(2))
        return r"\cite{" + ",".join(clave(i) for i in range(a, b + 1)) + "}"
    s = re.sub(r"\[(\d{1,2})\]\s*[-–]\s*\[(\d{1,2})\]", rango, s)
    s = re.sub(r"\[(\d{1,2})\]", lambda m: r"\cite{" + clave(int(m.group(1))) + "}", s)
    # Fusionar citas consecutivas: \cite{a}\cite{b}, \cite{a} \cite{b}, \cite{a}, \cite{b}
    patron = re.compile(r"\\cite\{([^}]*)\}(\s*,?\s*)\\cite\{([^}]*)\}")
    while patron.search(s):
        s = patron.sub(lambda m: r"\cite{" + m.group(1) + "," + m.group(3) + "}", s)
    # Espacio irrompible antes de la cita
    s = re.sub(r"(\S) \\cite\{", r"\1~\\cite{", s)
    s = re.sub(r"([^\s~{(])\\cite\{", r"\1~\\cite{", s)
    return s


def num_a_etiqueta(num: str) -> str:
    return "sec:" + num.strip(".").replace(".", "-")


def referencias(s: str) -> str:
    """Tabla N, Tablas N y M, Tablas N a M, Figura N y apartado X.Y -> \\ref."""
    s = re.sub(r"\bTablas (\d+) a (\d+)", r"Tablas~\\ref{tab:\1} a~\\ref{tab:\2}", s)
    s = re.sub(r"\bTablas (\d+) y (\d+)", r"Tablas~\\ref{tab:\1} y~\\ref{tab:\2}", s)
    s = re.sub(r"\bTabla (\d+)\b", r"Tabla~\\ref{tab:\1}", s)
    s = re.sub(r"\bFigura (\d+)\b", r"Figura~\\ref{fig:\1}", s)
    s = re.sub(r"\bapartado (\d+(?:\.\d+)+)\b", lambda m: "apartado~\\ref{" + num_a_etiqueta(m.group(1)) + "}", s)
    return s


def texto_cuerpo(inls) -> str:
    return referencias(citas(inline(inls)))


# --------------------------------------------------------------------------
# Títulos
# --------------------------------------------------------------------------
RE_NUM = re.compile(r"^\s*(\d+(?:\.\s?\d+)*)\.?\s+(.*)$")
NIVELES = {1: "chapter", 2: "section", 3: "subsection", 4: "subsubsection"}


def titulo(nivel: int, inls):
    texto = plano(inls).strip()
    m = RE_NUM.match(texto)
    if m:
        num = m.group(1).replace(" ", "")
        cuerpo = m.group(2).strip()
    else:
        num, cuerpo = None, texto
    return num, cuerpo


# --------------------------------------------------------------------------
# Tablas
# --------------------------------------------------------------------------
def celda_tex(cell, mono=False) -> str:
    blocks = cell[4]
    partes = []
    for b in blocks:
        if b["t"] in ("Para", "Plain"):
            if mono:
                partes.append(r"{\footnotesize\ttfamily " + esc(plano(b["c"])).replace("  ", r"\ \ ") + "}")
            else:
                partes.append(texto_cuerpo(b["c"]))
        elif b["t"] in ("BulletList", "OrderedList"):
            items = b["c"] if b["t"] == "BulletList" else b["c"][1]
            partes.extend(r"\textbullet~" + bloques_simples(it) for it in items)
    return r" \newline ".join(p for p in partes if p.strip())


def filas(table):
    head = table["c"][3][1]
    bodies = table["c"][4]
    rows = list(head)
    for body in bodies:
        rows.extend(body[2])
        rows.extend(body[3])
    return rows


ANCHO_TEXTO_PT = 455.0   # \textwidth con márgenes de 2,5 cm en A4
SEP_COLUMNA_PT = 12.0    # 2 x \tabcolsep
PT_POR_CARACTER = 6.0    # ancho medio por carácter en \small (10 pt), con margen


def anchos(rows, ncols, mono=frozenset(), escala=1.0):
    """Valores de \\hsize para cada columna X.

    Reparte el ancho según la longitud media del texto de cada columna, pero
    garantiza que la palabra más larga de cada columna (que LaTeX no puede
    partir) quepa entera.
    """
    tot = [0.0] * ncols
    cnt = [0] * ncols
    palabra = [0.0] * ncols
    for n, r in enumerate(rows):
        negrita = 1.12 if n == 0 else 1.0   # la cabecera va en negrita
        for k, cell in enumerate(r[1][:ncols]):
            txt = " ".join(plano(b["c"]) for b in cell[4] if b["t"] in ("Para", "Plain"))
            tot[k] += len(txt)
            cnt[k] += 1
            for w in txt.split():
                palabra[k] = max(palabra[k], len(w) * negrita)
    medias = [max(tot[k] / max(cnt[k], 1), 3) for k in range(ncols)]
    pesos = [m ** 0.75 for m in medias]
    disponible = ANCHO_TEXTO_PT - ncols * SEP_COLUMNA_PT
    s = sum(pesos)
    ancho = [disponible * p / s for p in pesos]
    # El código OCL va en \footnotesize monoespaciado (unos 4,8 pt por carácter)
    factor = [(4.9 if k in mono else PT_POR_CARACTER * escala) for k in range(ncols)]
    minimo = [palabra[k] * factor[k] + 4 for k in range(ncols)]
    # Subir las columnas por debajo de su mínimo y quitar ese espacio a las demás
    for _ in range(10):
        bajos = [k for k in range(ncols) if ancho[k] < minimo[k] - 0.01]
        if not bajos:
            break
        for k in bajos:
            ancho[k] = minimo[k]
        fijos = sum(ancho[k] for k in range(ncols) if ancho[k] <= minimo[k] + 0.01)
        libres = [k for k in range(ncols) if ancho[k] > minimo[k] + 0.01]
        resto = disponible - fijos
        suma_libres = sum(pesos[k] for k in libres) or 1
        for k in libres:
            ancho[k] = max(resto * pesos[k] / suma_libres, minimo[k])
    media = disponible / ncols
    return [a / media for a in ancho]


def tabla_tex(table, numero: int | None, titulo_pie: str | None) -> str:
    ncols = len(table["c"][2])
    rows = [r for r in filas(table) if any(plano_celda(c).strip() for c in r[1])]
    mono = set()
    if rows:
        cab = [plano_celda(c).strip().lower() for c in rows[0][1]]
        mono = {k for k, h in enumerate(cab) if "expresión ocl" in h}
    # Las tablas anchas (5 o más columnas) van en \footnotesize para que quepan
    ancha = ncols >= 5
    pesos = anchos(rows, ncols, frozenset(mono), escala=0.88 if ancha else 1.0)
    especificacion = "".join(r">{\hsize=%.3f\hsize\raggedright\arraybackslash}X" % w for w in pesos)
    tam = r"\footnotesize" if ancha else r"\small"
    cabecera = None
    if rows:
        cabecera = " & ".join(r"\textbf{" + plano_esc(c) + "}" for c in rows[0][1]) + r" \\"
    cuerpo = []
    for r in rows[1:]:
        celdas = [celda_tex(c, mono=(k in mono)) for k, c in enumerate(r[1])]
        cuerpo.append(" & ".join(celdas) + r" \\")

    # Las tablas que caben en una página van en un bloque que no se parte y se queda
    # en su sitio ([H], como en el Doc); las que no caben, en xltabular
    alto = lineas_estimadas(rows, pesos, ancha)
    tabla_tex.ultimo_alto = alto
    if alto <= 55:   # una página de texto en \small da para unas 55 líneas
        lineas = [r"\begin{table}[H]", r"\centering" + tam,
                  r"\begin{tabularx}{\textwidth}{" + especificacion + "}", r"\toprule"]
        if cabecera:
            lineas += [r"\rowcolor{cabeceratabla} " + cabecera, r"\midrule"]
        lineas += cuerpo + [r"\bottomrule", r"\end{tabularx}"]
        if numero is not None:
            lineas.append(r"\caption{" + titulo_pie + r"}\label{tab:" + str(numero) + "}")
        lineas.append(r"\end{table}")
        return "\n".join(lineas)

    lineas = [r"\begingroup" + tam,
              r"\begin{xltabular}{\textwidth}{" + especificacion + "}"]
    if cabecera:
        lineas += [r"\toprule", r"\rowcolor{cabeceratabla} " + cabecera, r"\midrule", r"\endfirsthead",
                   r"\toprule", r"\rowcolor{cabeceratabla} " + cabecera, r"\midrule", r"\endhead",
                   r"\bottomrule"]
        if numero is not None:
            lineas.append(r"\caption{" + titulo_pie + r"}\label{tab:" + str(numero) + r"}")
        lineas.append(r"\endlastfoot")
    lineas += cuerpo
    lineas.append(r"\end{xltabular}")
    lineas.append(r"\endgroup")
    return "\n".join(lineas)


def lineas_estimadas(rows, pesos, ancha) -> float:
    """Estimación de la altura de la tabla en líneas de texto (para decidir si cabe en una página)."""
    disponible = ANCHO_TEXTO_PT - len(pesos) * SEP_COLUMNA_PT
    media = disponible / len(pesos)
    pt_car = PT_POR_CARACTER * (0.88 if ancha else 1.0) * 0.85
    total = 0.0
    for r in rows:
        alto = 1
        for k, cell in enumerate(r[1][:len(pesos)]):
            cap = max(int(pesos[k] * media / pt_car), 1)
            n = 0
            for b in cell[4]:
                if b["t"] in ("Para", "Plain"):
                    n += max(1, -(-len(plano(b["c"])) // cap))
            alto = max(alto, n)
        total += alto + 0.35
    return total


def plano_celda(cell) -> str:
    return " ".join(plano(b["c"]) for b in cell[4] if b["t"] in ("Para", "Plain"))


def plano_esc(cell) -> str:
    return esc(plano_celda(cell).strip())


# --------------------------------------------------------------------------
# Recorrido principal
# --------------------------------------------------------------------------
RE_PIE_TABLA = re.compile(r"^Tabla\s+(\d+)\.?\s+(.*)$")
RE_PIE_FIGURA = re.compile(r"^Figura\s+(\d+)\.?\s+(.*)$")
RE_MARCADOR = re.compile(r"^\[Insertar aquí la Figura (\d+):")


def es_vacio(b) -> bool:
    if b["t"] == "Header":
        return not plano(b["c"][2]).strip()
    if b["t"] in ("Para", "Plain"):
        return not plano(b["c"]).strip()
    return False


def quitar_punto(s: str) -> str:
    return s.strip().rstrip(".").strip()


def convertir(blocks):
    capitulos: dict[int, list[str]] = {}
    actual: list[str] | None = None
    cap_num = 0
    biblio = []
    en_cuerpo = False
    en_biblio = False
    img_contador = 0
    i = 0
    lista_guiones: list[str] = []

    def vaciar_guiones():
        if lista_guiones and actual is not None:
            actual.append(r"\begin{itemize}")
            actual.extend(r"  \item " + x for x in lista_guiones)
            actual.append(r"\end{itemize}" + "\n")
        lista_guiones.clear()

    # Aplanar BlockQuotes del cuerpo (son párrafos sangrados o la bibliografía)
    plano_blocks = []
    for b in blocks:
        if b["t"] == "BlockQuote":
            plano_blocks.extend(b["c"])
        else:
            plano_blocks.append(b)
    blocks = plano_blocks

    while i < len(blocks):
        b = blocks[i]
        t = b["t"]
        if t == "Header":
            nivel = b["c"][0]
            texto = plano(b["c"][2]).strip()
            if not en_cuerpo:
                if texto == INICIO_CUERPO:
                    en_cuerpo = True
                else:
                    i += 1
                    continue
            if not texto:
                i += 1
                continue
            vaciar_guiones()
            if texto == TITULO_BIBLIO:
                en_biblio = True
                i += 1
                continue
            num, cuerpo = titulo(nivel, b["c"][2])
            if nivel == 1:
                cap_num = int(num) if num else cap_num + 1
                actual = capitulos.setdefault(cap_num, [])
            etiqueta = (r"\label{" + num_a_etiqueta(num) + "}") if num else ""
            # Evitar títulos solos al pie de página: exigir sitio para unas líneas más
            prefijo = "" if nivel == 1 else r"\needspace{6\baselineskip}" + "\n"
            actual.append(prefijo + "\\" + NIVELES.get(nivel, "paragraph") + "{" + esc(cuerpo) + "}" + etiqueta + "\n")
            i += 1
            continue

        if not en_cuerpo:
            i += 1
            continue

        if en_biblio:
            if t in ("Para", "Plain"):
                txt = plano(b["c"]).strip()
                m = re.match(r"^\[(\d+)\]\s*(.*)$", txt)
                if m:
                    biblio.append((int(m.group(1)), entrada_biblio(b["c"])))
            i += 1
            continue

        if t == "Table":
            vaciar_guiones()
            numero, pie = None, None
            # El pie puede venir tras títulos o párrafos vacíos que el Doc deja en medio
            j = i + 1
            while j < len(blocks) and es_vacio(blocks[j]):
                j += 1
            if j < len(blocks) and blocks[j]["t"] in ("Para", "Plain"):
                m = RE_PIE_TABLA.match(plano(blocks[j]["c"]).strip())
                if m:
                    numero, pie = int(m.group(1)), esc(quitar_punto(m.group(2)))
                    i = j
            tex = tabla_tex(b, numero, pie)
            # Si la tabla va justo después de un título, reservar sitio para los dos juntos
            if actual and actual[-1].startswith(r"\needspace{"):
                alto = min(getattr(tabla_tex, "ultimo_alto", 6), 40)
                reserva = int(alto * 0.8 + 5)
                actual[-1] = re.sub(r"^\\needspace\{\d+\\baselineskip\}", r"\\needspace{" + str(reserva) + r"\\baselineskip}", actual[-1])
            actual.append(tex + "\n")
            i += 1
            continue

        if t in ("Para", "Plain"):
            txt = plano(b["c"]).strip()
            if not txt:
                i += 1
                continue
            # Imagen seguida de su pie
            if txt == "[IMG]":
                img_contador += 1
                nombre = IMAGENES.get(img_contador)
                pie_num, pie_largo = None, ""
                if i + 1 < len(blocks) and blocks[i + 1]["t"] in ("Para", "Plain"):
                    m = RE_PIE_FIGURA.match(plano(blocks[i + 1]["c"]).strip())
                    if m:
                        pie_num, pie_largo = int(m.group(1)), m.group(2)
                        i += 1
                vaciar_guiones()
                actual.append(figura(nombre, pie_num, pie_largo))
                i += 1
                continue
            # Marcador de figura pendiente seguido de su pie
            m = RE_MARCADOR.match(txt)
            if m:
                pie_num, pie_largo = int(m.group(1)), ""
                if i + 1 < len(blocks) and blocks[i + 1]["t"] in ("Para", "Plain"):
                    m2 = RE_PIE_FIGURA.match(plano(blocks[i + 1]["c"]).strip())
                    if m2:
                        pie_largo = m2.group(2)
                        i += 1
                vaciar_guiones()
                actual.append(figura(None, pie_num, pie_largo, marcador=txt.strip("[]")))
                i += 1
                continue
            # Párrafos que empiezan por un guion escrito a mano -> lista
            if re.match(r"^-\s", txt):
                contenido = list(b["c"])
                while contenido and contenido[0]["t"] in ("Space",) or (contenido and contenido[0]["t"] == "Str" and contenido[0]["c"] == "-"):
                    contenido.pop(0)
                lista_guiones.append(texto_cuerpo(contenido).strip())
                i += 1
                continue
            vaciar_guiones()
            actual.append(texto_cuerpo(b["c"]).strip() + "\n")
            i += 1
            continue

        if t in ("BulletList", "OrderedList"):
            vaciar_guiones()
            items = b["c"] if t == "BulletList" else b["c"][1]
            entorno = "itemize" if t == "BulletList" else "enumerate"
            actual.append(r"\begin{" + entorno + "}")
            for it in items:
                actual.append(r"  \item " + " ".join(texto_cuerpo(x["c"]).strip() for x in it if x["t"] in ("Para", "Plain")))
            actual.append(r"\end{" + entorno + "}\n")
            i += 1
            continue

        i += 1

    vaciar_guiones()
    return capitulos, biblio


def figura(nombre, num, pie_largo, marcador=None) -> str:
    pie_largo = pie_largo.strip()
    corto = quitar_punto(pie_largo.split(". ")[0]) if pie_largo else ""
    largo = quitar_punto(pie_largo)
    lineas = [r"\begin{figure}[htbp]", r"\centering"]
    if nombre:
        lineas.append(r"\includegraphics[width=\textwidth]{imagenes/" + nombre + "}")
    else:
        lineas.append(r"\figurapendiente{" + esc(marcador or "Figura pendiente") + "}")
    if num is not None:
        if corto and corto != largo:
            lineas.append(r"\caption[" + esc(corto) + "]{" + esc(largo) + r"}\label{fig:" + str(num) + "}")
        else:
            lineas.append(r"\caption{" + esc(largo) + r"}\label{fig:" + str(num) + "}")
    lineas.append(r"\end{figure}" + "\n")
    return "\n".join(lineas)


def entrada_biblio(inls) -> str:
    # Quitar el "[n]" inicial
    inls = list(inls)
    while inls and (inls[0]["t"] == "Space" or (inls[0]["t"] == "Str" and re.match(r"^\[\d+\]$", inls[0]["c"]))):
        inls.pop(0)
    texto = inline(inls).strip()
    # URLs sueltas -> \url{}
    texto = re.sub(r"(https?://[^\s]+?)(\.?)(\s|$)", lambda m: r"\url{" + m.group(1).replace(r"\_", "_").replace(r"\%", "%").replace(r"\#", "#") + "}" + m.group(2) + m.group(3), texto)
    return texto


def escribir(capitulos, biblio):
    (DESTINO / "capitulos").mkdir(parents=True, exist_ok=True)
    cabecera = "% Generado por trabajo_en_curso/week5/latex/convertir.py a partir del .docx de la memoria.\n% A partir de ahora este fichero es la fuente: edítalo directamente.\n\n"
    for n, lineas in capitulos.items():
        nombre = FICHEROS_CAPITULO.get(n, f"{n:02d}_capitulo.tex")
        (DESTINO / "capitulos" / nombre).write_text(cabecera + "\n".join(lineas) + "\n", encoding="utf-8")
    numeros = {n for n, _ in biblio}
    todos = dict(biblio)
    for n, txt in PENDIENTES_BIBLIO.items():
        if n not in numeros:
            todos[n] = txt + r" \pendiente{Referencia pendiente de confirmar.}"
    maximo = max(todos)
    out = [cabecera.rstrip() + "\n", r"\begin{thebibliography}{" + str(maximo) + "}", r"\raggedright"]
    for n in range(1, maximo + 1):
        if n in todos:
            out.append(r"\bibitem{" + clave(n) + "} " + todos[n])
        else:
            out.append(r"\bibitem{" + clave(n) + r"} \pendiente{Referencia sin datos en la memoria original.}")
    out.append(r"\end{thebibliography}")
    (DESTINO / "bibliografia.tex").write_text("\n\n".join(out) + "\n", encoding="utf-8")
    return sorted(capitulos), maximo


def main():
    if not PANDOC.exists():
        sys.exit(f"No se encuentra Pandoc en {PANDOC}")
    with tempfile.TemporaryDirectory() as tmp:
        json_path = Path(tmp) / "memoria.json"
        subprocess.run([str(PANDOC), str(DOCX), "-t", "json", "-o", str(json_path)], check=True)
        ast = json.loads(json_path.read_text(encoding="utf-8"))
    capitulos, biblio = convertir(ast["blocks"])
    caps, maximo = escribir(capitulos, biblio)
    print(f"Capítulos escritos: {caps}; entradas de bibliografía: {len(biblio)} (hasta [{maximo}])")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
