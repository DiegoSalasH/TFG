"""Figura: diseño lógico de la base de datos (esquema relacional).

Misma disposición que el diagrama conceptual. Cada caja es una tabla; la clave
primaria va en negrita y las flechas van de la clave ajena a la tabla
referenciada. Las claves ajenas hacia `users` (autor, responsable) se indican
en la columna y no se dibujan, para no llenar el diagrama de líneas.

Uso: python generadores/gen_bd_logico.py
Salida: Documentation/Docu_Final/Memoria/Latex_Memoria/imagenes/bd_logico.png
"""

import estilo as E
from diagramas_bd import Caja, Rejilla, dibujar_caja, polilinea

C = {
    "persona": Caja("contacts (núcleo)", ["*id : CHAR(36)", "first_name : VARCHAR", "last_name : VARCHAR", "phone_mobile : VARCHAR", "relacion_c : VARCHAR (contacts_cstm)"], 0, 0),
    "autorizacion": Caja("ext_autorizaciones", ["*id : CHAR(36)", "alumno_id → ext_alumnos", "contact_id → contacts", "tipo, estado : VARCHAR", "valida_desde : DATE", "valida_hasta : DATE", "metodo_comprobacion : VARCHAR"], 1, 0),
    "alumno": Caja("ext_alumnos", ["*id : CHAR(36)", "codigo : VARCHAR (único)", "nombre, apellidos : VARCHAR", "fecha_nacimiento : DATE", "curso : VARCHAR"], 2, 0, destacada=True),
    "inscripcion": Caja("ext_inscripciones", ["*id : CHAR(36)", "alumno_id → ext_alumnos", "grupo_id → ext_grupos", "fecha_alta : DATE", "fecha_baja : DATE (nulo)", "estado : VARCHAR"], 3, 0),
    "actividad": Caja("ext_actividades", ["*id : CHAR(36)", "name : VARCHAR", "description : TEXT", "curso_escolar : VARCHAR", "entidad_organizadora : VARCHAR"], 4, 0),
    "entrega": Caja("ext_entregas", ["*id : CHAR(36)", "sesion_id → ext_sesiones", "alumno_id → ext_alumnos", "receptor_id → contacts (nulo)", "autorizacion_id → ext_autorizaciones", "responsable_id → users", "hora_entrega : DATETIME", "resultado : VARCHAR", "observaciones : TEXT"], 1, 1),
    "asistencia": Caja("ext_asistencias", ["*id : CHAR(36)", "sesion_id → ext_sesiones", "alumno_id → ext_alumnos", "estado : VARCHAR", "hora_registro : DATETIME", "motivo : VARCHAR (nulo)", "registrada_por → users"], 2, 1),
    "sesion": Caja("ext_sesiones", ["*id : CHAR(36)", "grupo_id → ext_grupos", "fecha : DATE", "hora_inicio : TIME", "hora_fin : TIME", "estado : VARCHAR"], 3, 1),
    "grupo": Caja("ext_grupos", ["*id : CHAR(36)", "actividad_id → ext_actividades", "name : VARCHAR", "horario : VARCHAR", "plazas : INT"], 4, 1),
    "comunicacion": Caja("ext_comunicaciones", ["*id : CHAR(36)", "incidencia_id → ext_incidencias", "destinatario_id → contacts", "canal, estado : VARCHAR", "enviada_en : DATETIME", "acuse_en : DATETIME (nulo)", "enviada_por → users"], 1, 2),
    "actuacion": Caja("ext_actuaciones", ["*id : CHAR(36)", "incidencia_id → ext_incidencias", "descripcion : TEXT", "fecha_hora : DATETIME", "autor_id → users"], 2, 2),
    "incidencia": Caja("ext_incidencias", ["*id : CHAR(36)", "alumno_id → ext_alumnos (nulo)", "sesion_id → ext_sesiones (nulo)", "tipo, prioridad, estado : VARCHAR", "descripcion : TEXT", "fecha_hora : DATETIME", "responsable_id → users (nulo)"], 3, 2),
    "grupos_users": Caja("ext_grupos_users", ["*id : CHAR(36)", "grupo_id → ext_grupos", "user_id → users"], 4, 2),
    "usuario": Caja("users (núcleo)", ["*id : CHAR(36)", "user_name : VARCHAR", "rol: acl_roles, securitygroups"], 4, 3),
}

# Notación de clave ajena en texto ASCII (Lora no tiene la flecha →): «columna [FK tabla]»
import re
for _c in C.values():
    _c.lineas = [re.sub(r"(\S+) → (\S+)", r"\1 [FK \2]", l) for l in _c.lineas]

R = Rejilla(list(C.values()))
img, d = E.lienzo(R.ancho, R.alto)

y0 = R.y_fila[0] + 70
y1 = R.y_fila[1] + 70
y2 = R.y_fila[2] + 70
p, a, al, ins, act = C["persona"], C["autorizacion"], C["alumno"], C["inscripcion"], C["actividad"]
en, asi, se, gr = C["entrega"], C["asistencia"], C["sesion"], C["grupo"]
co, ac, inc, gu, us = C["comunicacion"], C["actuacion"], C["incidencia"], C["grupos_users"], C["usuario"]
base2 = R.y_fila[2] + R.alto_fila[2] + 32

# Cada ruta va de la tabla con la clave ajena a la tabla referenciada (la flecha apunta a la clave primaria)
fks = [
    [(a.x, y0), (p.x + p.w, y0)],                                              # autorizaciones.contact_id
    [(a.x + a.w, y0), (al.x, y0)],                                             # autorizaciones.alumno_id
    [(ins.x, y0), (al.x + al.w, y0)],                                          # inscripciones.alumno_id
    [ins.abajo(0.8), (ins.abajo(0.8)[0], R.hueco_y(0, 0)), (gr.arriba(0.25)[0], R.hueco_y(0, 0)), gr.arriba(0.25)],
    [gr.arriba(0.75), act.abajo(0.75)],                                        # grupos.actividad_id
    [(se.x + se.w, y1), (gr.x, y1)],                                           # sesiones.grupo_id
    [(asi.x + asi.w, y1), (se.x, y1)],                                         # asistencias.sesion_id
    [asi.arriba(0.5), al.abajo(0.5)],                                          # asistencias.alumno_id
    [en.arriba(0.5), a.abajo(0.5)],                                            # entregas.autorizacion_id
    [en.arriba(0.88), (en.arriba(0.88)[0], R.hueco_y(0, 1)), (al.abajo(0.18)[0], R.hueco_y(0, 1)), al.abajo(0.18)],
    [en.izq(0.5), (p.x + p.w * 0.72, en.izq(0.5)[1]), p.abajo(0.72)],         # entregas.receptor_id
    [en.abajo(0.72), (en.abajo(0.72)[0], R.hueco_y(1, 0)), (se.abajo(0.22)[0], R.hueco_y(1, 0)), se.abajo(0.22)],
    [inc.arriba(0.62), se.abajo(0.62)],                                        # incidencias.sesion_id
    [(inc.x, inc.y + 34), (R.hueco_x(3), inc.y + 34), (R.hueco_x(3), R.hueco_y(0, 2)), (al.abajo(0.84)[0], R.hueco_y(0, 2)), al.abajo(0.84)],
    [(ac.x + ac.w, y2 + 20), (inc.x, y2 + 20)],                                # actuaciones.incidencia_id
    [co.abajo(0.5), (co.abajo(0.5)[0], base2), (inc.abajo(0.3)[0], base2), inc.abajo(0.3)],
    [co.izq(0.5), (p.x + p.w * 0.32, co.izq(0.5)[1]), p.abajo(0.32)],         # comunicaciones.destinatario_id
    [gu.arriba(0.5), gr.abajo(0.5)],                                           # grupos_users.grupo_id
    [gu.abajo(0.5), us.arriba(0.5)],                                           # grupos_users.user_id
]

for pts in fks:
    polilinea(d, pts, flecha_final=True)
for c in C.values():
    dibujar_caja(d, c, tam_linea=10)

ruta = E.guardar(img, "bd_logico.png")
print(ruta, img.size)
