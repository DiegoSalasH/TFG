"""Figura: diseño conceptual de la base de datos (diagrama de clases UML).

Uso: python generadores/gen_bd_conceptual.py
Salida: Documentation/Docu_Final/Memoria/Latex_Memoria/imagenes/bd_conceptual.png
"""

import estilo as E
from diagramas_bd import Caja, Rejilla, dibujar_caja, polilinea, etiqueta, etiqueta_extremo

C = {
    "persona": Caja("PersonaAutorizada", ["nombre : Texto", "apellidos : Texto", "telefono : Texto", "email : Texto", "relacion : Texto"], 0, 0),
    "autorizacion": Caja("Autorizacion", ["tipo : TipoAutorizacion", "validaDesde : Fecha", "validaHasta : Fecha", "estado : EstadoAutorizacion", "metodoComprobacion : Texto"], 1, 0),
    "alumno": Caja("Alumno", ["codigo : Texto", "nombre : Texto", "apellidos : Texto", "fechaNacimiento : Fecha", "curso : Texto"], 2, 0, destacada=True),
    "inscripcion": Caja("Inscripcion", ["fechaAlta : Fecha", "fechaBaja : Fecha [0..1]", "estado : EstadoInscripcion"], 3, 0),
    "actividad": Caja("Actividad", ["nombre : Texto", "descripcion : Texto", "cursoEscolar : Texto", "entidadOrganizadora : Texto"], 4, 0),
    "entrega": Caja("EntregaCustodia", ["horaEntrega : FechaHora", "resultado : ResultadoEntrega", "observaciones : Texto [0..1]", "responsable : Usuario"], 1, 1),
    "asistencia": Caja("Asistencia", ["estado : EstadoAsistencia", "horaRegistro : FechaHora", "motivo : Texto [0..1]", "autor : Usuario"], 2, 1),
    "sesion": Caja("Sesion", ["fecha : Fecha", "horaInicio : Hora", "horaFin : Hora", "estado : EstadoSesion"], 3, 1),
    "grupo": Caja("Grupo", ["nombre : Texto", "horario : Texto", "plazas : Entero"], 4, 1),
    "comunicacion": Caja("Comunicacion", ["canal : Canal", "enviadaEn : FechaHora", "acuseEn : FechaHora [0..1]", "estado : EstadoComunicacion", "enviadaPor : Usuario"], 1, 2),
    "actuacion": Caja("Actuacion", ["descripcion : Texto", "fechaHora : FechaHora", "autor : Usuario"], 2, 2),
    "incidencia": Caja("Incidencia", ["tipo : TipoIncidencia", "prioridad : Prioridad", "estado : EstadoIncidencia", "descripcion : Texto", "fechaHora : FechaHora", "responsable : Usuario [0..1]"], 3, 2),
    "usuario": Caja("Usuario", ["nombre : Texto", "rol : Rol"], 4, 2),
}

R = Rejilla(list(C.values()))
img, d = E.lienzo(R.ancho, R.alto)

# --- Asociaciones: (puntos, multiplicidad inicio, multiplicidad fin, rol, posición del rol) ---
y0 = R.y_fila[0] + 70
y1 = R.y_fila[1] + 70
y2 = R.y_fila[2] + 70
p, a, al, ins, act = C["persona"], C["autorizacion"], C["alumno"], C["inscripcion"], C["actividad"]
en, asi, se, gr = C["entrega"], C["asistencia"], C["sesion"], C["grupo"]
co, ac, inc, us = C["comunicacion"], C["actuacion"], C["incidencia"], C["usuario"]

asoc = [
    ([(p.x + p.w, y0), (a.x, y0)], "1", "0..*", None),
    ([(a.x + a.w, y0), (al.x, y0)], "0..*", "1", None),
    ([(al.x + al.w, y0), (ins.x, y0)], "1", "0..*", None),
    ([ins.abajo(0.8), (ins.abajo(0.8)[0], R.hueco_y(0, 0)), (gr.arriba(0.25)[0], R.hueco_y(0, 0)), gr.arriba(0.25)], "0..*", "1", None),
    ([act.abajo(0.75), gr.arriba(0.75)], "1", "1..*", None),
    ([(gr.x, y1), (se.x + se.w, y1)], "1", "0..*", None),
    ([(se.x, y1), (asi.x + asi.w, y1)], "1", "0..*", None),
    ([al.abajo(0.5), asi.arriba(0.5)], "1", "0..*", None),
    ([en.arriba(0.5), a.abajo(0.5)], "0..*", "0..1", ("aplica", 0.5)),
    ([en.arriba(0.88), (en.arriba(0.88)[0], R.hueco_y(0, 1)), (al.abajo(0.18)[0], R.hueco_y(0, 1)), al.abajo(0.18)], "0..*", "1", None),
    ([en.izq(0.5), (p.x + p.w * 0.72, en.izq(0.5)[1]), p.abajo(0.72)], "0..*", "0..1", ("receptor", 1)),
    ([se.abajo(0.22), (se.abajo(0.22)[0], R.hueco_y(1, 0)), (en.abajo(0.72)[0], R.hueco_y(1, 0)), en.abajo(0.72)], "1", "0..*", None),
    ([se.abajo(0.62), inc.arriba(0.62)], "0..1", "0..*", None),
    ([(inc.x, inc.y + 34), (R.hueco_x(3), inc.y + 34), (R.hueco_x(3), R.hueco_y(0, 2)), (al.abajo(0.84)[0], R.hueco_y(0, 2)), al.abajo(0.84)], "0..*", "0..1", None),
    ([(inc.x, y2 + 20), (ac.x + ac.w, y2 + 20)], "1", "0..*", None),
    ([inc.abajo(0.3), (inc.abajo(0.3)[0], R.y_fila[2] + R.alto_fila[2] + 32), (co.abajo(0.5)[0], R.y_fila[2] + R.alto_fila[2] + 32), co.abajo(0.5)], "1", "0..*", None),
    ([co.izq(0.5), (p.x + p.w * 0.32, co.izq(0.5)[1]), p.abajo(0.32)], "0..*", "1", ("destinatario", 1)),
    ([gr.abajo(0.5), us.arriba(0.5)], "0..*", "1..*", ("monitor asignado", 0.5)),
]

for pts, m1, m2, rol in asoc:
    polilinea(d, pts)
for c in C.values():
    dibujar_caja(d, c)
for pts, m1, m2, rol in asoc:
    etiqueta_extremo(d, pts, m1, en_inicio=True)
    etiqueta_extremo(d, pts, m2, en_inicio=False)
    if rol:
        texto, k = rol
        if k == 1:      # junto al codo
            x, y = pts[1]
            etiqueta(d, x + 6, y + 6, texto, cursiva=True)
        else:           # mitad del primer tramo
            (xa, ya), (xb, yb) = pts[0], pts[1]
            etiqueta(d, (xa + xb) / 2 + 8, (ya + yb) / 2 - 7, texto, cursiva=True)

ruta = E.guardar(img, "bd_conceptual.png")
print(ruta, img.size)
