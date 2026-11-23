"""Estilo común de los diagramas de la memoria.

Todos los generadores (gen_*.py) importan este módulo para que los diagramas
compartan tipografía, colores, grosores y resolución. Si hay que cambiar el
aspecto de los diagramas, se cambia aquí y se regeneran todos.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --- Rutas -------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parent.parent
FUENTES = Path(__file__).resolve().parent / "fuentes"
# La memoria se escribe en LaTeX (D-07): las figuras van junto al .tex
SALIDA = RAIZ / "Documentation" / "Docu_Final" / "Memoria" / "Latex_Memoria" / "imagenes"

# --- Resolución --------------------------------------------------------------
# Se dibuja a escala 2 para que el PNG se vea nítido al insertarlo en la memoria.
ESCALA = 2
DPI = 200

# --- Colores (coherentes con las tablas de la memoria) -----------------------
FONDO = (255, 255, 255)
TEXTO = (33, 33, 33)
LINEA = (80, 80, 80)
CABECERA = (204, 204, 204)   # mismo gris que la cabecera de las tablas
RELLENO = (242, 242, 242)
ACENTO = (46, 94, 140)       # azul sobrio para resaltar elementos clave
ACENTO_SUAVE = (220, 230, 241)

# --- Grosores y tamaños (en píxeles lógicos, antes de aplicar ESCALA) -------
GROSOR_LINEA = 2
RADIO_ESQUINA = 8
TAM_TITULO = 20
TAM_TEXTO = 15
TAM_PEQUENO = 12


def px(valor: float) -> int:
    """Convierte una medida lógica a píxeles reales según la escala."""
    return int(round(valor * ESCALA))


def fuente(tamano: int = TAM_TEXTO, negrita: bool = False, cursiva: bool = False) -> ImageFont.FreeTypeFont:
    """Devuelve la fuente Lora incluida en el repositorio, en el peso pedido."""
    archivo = FUENTES / ("Lora-Italic-Variable.ttf" if cursiva else "Lora-Variable.ttf")
    f = ImageFont.truetype(str(archivo), px(tamano))
    try:
        f.set_variation_by_name("Bold" if negrita else "Regular")
    except (OSError, ValueError):
        pass  # Si la variación no existe, se usa el peso por defecto.
    return f


def lienzo(ancho: int, alto: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Crea un lienzo blanco del tamaño lógico indicado."""
    img = Image.new("RGB", (px(ancho), px(alto)), FONDO)
    return img, ImageDraw.Draw(img)


def ajustar_texto(draw: ImageDraw.ImageDraw, texto: str, f: ImageFont.FreeTypeFont, ancho_max: int) -> list[str]:
    """Parte el texto en líneas que quepan en ancho_max (píxeles lógicos)."""
    lineas: list[str] = []
    for parrafo in texto.split("\n"):
        palabras = parrafo.split()
        actual = ""
        for palabra in palabras:
            prueba = f"{actual} {palabra}".strip()
            if draw.textlength(prueba, font=f) <= px(ancho_max):
                actual = prueba
            else:
                if actual:
                    lineas.append(actual)
                actual = palabra
        lineas.append(actual)
    return lineas or [""]


def texto_centrado(draw, caja: tuple[float, float, float, float], texto: str, f=None, color=TEXTO, interlineado: float = 1.25) -> None:
    """Escribe texto centrado (horizontal y verticalmente) dentro de una caja lógica (x0, y0, x1, y1)."""
    f = f or fuente()
    x0, y0, x1, y1 = caja
    lineas = ajustar_texto(draw, texto, f, int(x1 - x0) - 12)
    alto_linea = f.size * interlineado
    total = alto_linea * len(lineas)
    y = px((y0 + y1) / 2) - total / 2
    for linea in lineas:
        ancho = draw.textlength(linea, font=f)
        draw.text((px((x0 + x1) / 2) - ancho / 2, y), linea, font=f, fill=color)
        y += alto_linea


def caja(draw, x0, y0, x1, y1, texto: str = "", relleno=RELLENO, borde=LINEA, f=None, redondeada: bool = True) -> None:
    """Dibuja una caja con borde y, opcionalmente, texto centrado."""
    forma = (px(x0), px(y0), px(x1), px(y1))
    if redondeada:
        draw.rounded_rectangle(forma, radius=px(RADIO_ESQUINA), fill=relleno, outline=borde, width=px(GROSOR_LINEA))
    else:
        draw.rectangle(forma, fill=relleno, outline=borde, width=px(GROSOR_LINEA))
    if texto:
        texto_centrado(draw, (x0, y0, x1, y1), texto, f)


def flecha(draw, x0, y0, x1, y1, color=LINEA, punta: float = 10, discontinua: bool = False) -> None:
    """Dibuja una línea con punta de flecha al final (coordenadas lógicas)."""
    import math

    if discontinua:
        largo = math.hypot(x1 - x0, y1 - y0)
        pasos = max(int(largo // 8), 1)
        for i in range(0, pasos, 2):
            a, b = i / pasos, min((i + 1) / pasos, 1)
            draw.line((px(x0 + (x1 - x0) * a), px(y0 + (y1 - y0) * a), px(x0 + (x1 - x0) * b), px(y0 + (y1 - y0) * b)), fill=color, width=px(GROSOR_LINEA))
    else:
        draw.line((px(x0), px(y0), px(x1), px(y1)), fill=color, width=px(GROSOR_LINEA))
    ang = math.atan2(y1 - y0, x1 - x0)
    izq = (x1 - punta * math.cos(ang - math.pi / 7), y1 - punta * math.sin(ang - math.pi / 7))
    der = (x1 - punta * math.cos(ang + math.pi / 7), y1 - punta * math.sin(ang + math.pi / 7))
    draw.polygon([(px(x1), px(y1)), (px(izq[0]), px(izq[1])), (px(der[0]), px(der[1]))], fill=color)


def guardar(img: Image.Image, nombre: str) -> Path:
    """Guarda el PNG en la carpeta de imágenes de la memoria y devuelve la ruta."""
    SALIDA.mkdir(parents=True, exist_ok=True)
    ruta = SALIDA / nombre
    img.save(ruta, dpi=(DPI, DPI), optimize=True)
    return ruta
