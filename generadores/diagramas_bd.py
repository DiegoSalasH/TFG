"""Utilidades comunes para los diagramas de base de datos (conceptual, lógico).

Una `Caja` es una entidad o una tabla: título y una lista de líneas (atributos
o columnas). Las cajas se colocan en una rejilla de columnas y filas; las
líneas entre cajas se dibujan como polilíneas con codos, a partir de puntos que
se calculan con los lados de las cajas y con los huecos entre filas y columnas.
"""

from __future__ import annotations

import estilo as E

ANCHO_CAJA = 262
PASO_X = 330
X0 = 30
Y0 = 40
ALTO_CAB = 30
ALTO_LINEA = 18
HUECO_FILA = 120


class Caja:
    def __init__(self, titulo: str, lineas: list[str], col: int, fila: int, ancho: int = ANCHO_CAJA, destacada: bool = False):
        self.titulo, self.lineas, self.col, self.fila = titulo, lineas, col, fila
        self.w = ancho
        self.h = ALTO_CAB + len(lineas) * ALTO_LINEA + 10
        self.destacada = destacada
        self.x = self.y = 0

    # Puntos sobre los lados (frac entre 0 y 1)
    def arriba(self, f=0.5):
        return (self.x + self.w * f, self.y)

    def abajo(self, f=0.5):
        return (self.x + self.w * f, self.y + self.h)

    def izq(self, f=0.5):
        return (self.x, self.y + self.h * f)

    def der(self, f=0.5):
        return (self.x + self.w, self.y + self.h * f)


class Rejilla:
    """Coloca las cajas y da coordenadas de los huecos para trazar líneas."""

    def __init__(self, cajas: list[Caja], hueco_fila: int = HUECO_FILA):
        self.cajas = cajas
        nfilas = max(c.fila for c in cajas) + 1
        self.alto_fila = [max((c.h for c in cajas if c.fila == f), default=0) for f in range(nfilas)]
        self.y_fila = []
        y = Y0
        for f in range(nfilas):
            self.y_fila.append(y)
            y += self.alto_fila[f] + hueco_fila
        for c in cajas:
            c.x = X0 + c.col * PASO_X
            c.y = self.y_fila[c.fila]
        self.ancho = X0 * 2 + (max(c.col for c in cajas)) * PASO_X + ANCHO_CAJA
        self.alto = y - hueco_fila + 90

    def col_x(self, col: int) -> float:
        return X0 + col * PASO_X

    def hueco_x(self, col: int) -> float:
        """Centro del hueco vertical a la izquierda de la columna `col`."""
        return X0 + col * PASO_X - (PASO_X - ANCHO_CAJA) / 2

    def hueco_y(self, fila: int, k: int = 0) -> float:
        """Línea horizontal k-ésima dentro del hueco que hay debajo de la fila `fila`."""
        return self.y_fila[fila] + self.alto_fila[fila] + 24 + k * 22


def dibujar_caja(d, c: Caja, tam_titulo=13, tam_linea=11) -> None:
    borde = E.ACENTO if c.destacada else E.LINEA
    cab = E.ACENTO_SUAVE if c.destacada else E.CABECERA
    d.rectangle((E.px(c.x), E.px(c.y), E.px(c.x + c.w), E.px(c.y + c.h)), fill=E.FONDO, outline=borde, width=E.px(E.GROSOR_LINEA))
    d.rectangle((E.px(c.x), E.px(c.y), E.px(c.x + c.w), E.px(c.y + ALTO_CAB)), fill=cab, outline=borde, width=E.px(E.GROSOR_LINEA))
    E.texto_centrado(d, (c.x, c.y, c.x + c.w, c.y + ALTO_CAB), c.titulo, E.fuente(tam_titulo, negrita=True))
    f = E.fuente(tam_linea)
    fn = E.fuente(tam_linea, negrita=True)
    for i, linea in enumerate(c.lineas):
        y = c.y + ALTO_CAB + 5 + i * ALTO_LINEA
        negrita = linea.startswith("*")   # las claves primarias se marcan con *
        texto = linea.lstrip("*")
        d.text((E.px(c.x + 8), E.px(y)), texto, font=fn if negrita else f, fill=E.TEXTO)


def polilinea(d, pts, color=E.LINEA, flecha_final=False, discontinua=False) -> None:
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        ultimo = (x1, y1) == pts[-1]
        if flecha_final and ultimo:
            E.flecha(d, x0, y0, x1, y1, color=color, punta=9, discontinua=discontinua)
        elif discontinua:
            E.flecha(d, x0, y0, x1, y1, color=color, punta=0.01, discontinua=True)
        else:
            d.line((E.px(x0), E.px(y0), E.px(x1), E.px(y1)), fill=color, width=E.px(E.GROSOR_LINEA))


def etiqueta(d, x, y, texto, tam=11, color=E.TEXTO, cursiva=False) -> None:
    """Texto pequeño con fondo blanco para que se lea sobre las líneas."""
    f = E.fuente(tam, cursiva=cursiva)
    ancho = d.textlength(texto, font=f) / E.ESCALA
    d.rectangle((E.px(x - 2), E.px(y - 1), E.px(x + ancho + 2), E.px(y + tam + 3)), fill=E.FONDO)
    d.text((E.px(x), E.px(y)), texto, font=f, fill=color)


def etiqueta_extremo(d, pts, texto, en_inicio=True) -> None:
    """Coloca la multiplicidad junto al extremo de una polilínea."""
    if not texto:
        return
    (x0, y0), (x1, y1) = (pts[0], pts[1]) if en_inicio else (pts[-1], pts[-2])
    if abs(x1 - x0) < 1:          # tramo vertical
        y = y0 + 6 if y1 > y0 else y0 - 20
        etiqueta(d, x0 + 6, y, texto)
    else:                          # tramo horizontal: inicio encima, final debajo
        f = E.fuente(11)
        ancho = d.textlength(texto, font=f) / E.ESCALA
        x = x0 + 5 if x1 > x0 else x0 - ancho - 5
        etiqueta(d, x, y0 - 18 if en_inicio else y0 + 4, texto)
