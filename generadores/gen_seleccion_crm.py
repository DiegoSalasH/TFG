"""Figura: proceso de selección de la plataforma CRM.

Uso: python generadores/gen_seleccion_crm.py
Salida: Documentation/Docu_Final/Memoria/Latex_Memoria/imagenes/seleccion_crm.png
"""

import estilo as E

img, d = E.lienzo(1400, 400)
f = E.fuente(13)
fn = E.fuente(13, negrita=True)
fp = E.fuente(11)

etapas = [
    ("1. Lista larga", "9 CRM del mercado: 5 de código abierto y 4 propietarios", E.RELLENO, E.LINEA),
    ("2. Criterio eliminatorio", "Gratuito y de código abierto: licencia libre, sin coste por usuario y autoalojable", E.ACENTO_SUAVE, E.ACENTO),
    ("3. Lista corta", "SuiteCRM 8, Odoo Community, EspoCRM y CiviCRM", E.RELLENO, E.LINEA),
    ("4. Matriz ponderada", "6 criterios con pesos fijados antes de puntuar y análisis de sensibilidad", E.RELLENO, E.LINEA),
    ("5. Selección", "SuiteCRM 8, a confirmar con las pruebas de concepto del apartado 1.2.5", E.ACENTO_SUAVE, E.ACENTO),
]
x, ancho, hueco, y0, y1 = 20, 232, 45, 40, 200
for i, (titulo, texto, relleno, borde) in enumerate(etapas):
    E.caja(d, x, y0, x + ancho, y1, relleno=relleno, borde=borde)
    E.texto_centrado(d, (x, y0 + 6, x + ancho, y0 + 40), titulo, fn)
    E.texto_centrado(d, (x + 8, y0 + 40, x + ancho - 8, y1 - 8), texto, f)
    if i < len(etapas) - 1:
        E.flecha(d, x + ancho, (y0 + y1) / 2, x + ancho + hueco, (y0 + y1) / 2)
    if i == 1:
        xe = x
    x += ancho + hueco

# Candidatos descartados por el criterio eliminatorio
E.flecha(d, xe + ancho / 2, y1, xe + ancho / 2, 260, discontinua=True)
E.caja(d, 20, 260, 1380, 380, relleno=E.FONDO, borde=E.LINEA, redondeada=True)
E.texto_centrado(d, (30, 266, 1370, 296), "Descartados en la fase 2", fn)
E.texto_centrado(
    d, (40, 296, 1360, 374),
    "Salesforce Education Cloud, Microsoft Dynamics 365, HubSpot CRM y Zoho CRM: software propietario con licencia o suscripción "
    "y alojamiento del proveedor (HubSpot y Zoho tienen planes gratuitos, pero no son de código abierto). "
    "Vtiger CE: su licencia (VPL) no está aprobada por la Open Source Initiative.",
    fp,
)

ruta = E.guardar(img, "seleccion_crm.png")
print(ruta, img.size)
