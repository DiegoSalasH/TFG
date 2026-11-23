"""Figura: diseño físico del almacenamiento (despliegue de SuiteCRM y MariaDB).

Uso: python generadores/gen_bd_fisico.py
Salida: Documentation/Docu_Final/Memoria/Latex_Memoria/imagenes/bd_fisico.png
"""

import estilo as E

img, d = E.lienzo(1400, 690)
ft = E.fuente(14, negrita=True)
f = E.fuente(12)
fp = E.fuente(11)


def contenedor(x0, y0, x1, y1, titulo, color=E.ACENTO):
    d.rounded_rectangle((E.px(x0), E.px(y0), E.px(x1), E.px(y1)), radius=E.px(10), fill=E.FONDO, outline=color, width=E.px(E.GROSOR_LINEA))
    E.texto_centrado(d, (x0, y0 + 4, x1, y0 + 30), titulo, ft, color=color)


def bloque(x0, y0, x1, y1, titulo, texto, relleno=E.RELLENO):
    E.caja(d, x0, y0, x1, y1, relleno=relleno, redondeada=False)
    E.texto_centrado(d, (x0, y0 + 2, x1, y0 + 24), titulo, E.fuente(12, negrita=True))
    E.texto_centrado(d, (x0 + 6, y0 + 22, x1 - 6, y1 - 4), texto, fp)


# Cliente
E.caja(d, 20, 120, 220, 200, "Navegador de coordinación, monitores y dirección", relleno=E.RELLENO, f=f)

# Servidor de aplicación
contenedor(290, 20, 770, 360, "Servidor de aplicación (Apache + PHP)")
bloque(310, 60, 750, 165, "SuiteCRM 8 (núcleo)", "Usuarios, roles, grupos de seguridad, flujos de trabajo, auditoría de campos y API")
bloque(310, 185, 750, 340, "Paquete «Gestión de Extraescolares» (custom/)", "Módulos ext_*, campos y relaciones creados con Module Builder; logic hooks before_save para OCL02, OCL05 y OCL08; workflows de aviso y escalado", relleno=E.ACENTO_SUAVE)

# Base de datos
contenedor(850, 20, 1380, 520, "MariaDB · InnoDB · utf8mb4")
bloque(870, 60, 1360, 140, "Tablas del núcleo", "users, acl_roles, securitygroups, securitygroups_records, contacts, contacts_cstm")
bloque(870, 155, 1360, 250, "Tablas de la extensión", "ext_alumnos, ext_autorizaciones, ext_actividades, ext_grupos, ext_inscripciones, ext_sesiones, ext_asistencias, ext_entregas, ext_incidencias, ext_actuaciones, ext_comunicaciones", relleno=E.ACENTO_SUAVE)
bloque(870, 265, 1360, 320, "Tablas de relación", "ext_grupos_users (monitor asignado a grupo)")
bloque(870, 335, 1360, 415, "Tablas de auditoría", "ext_autorizaciones_audit, ext_asistencias_audit, ext_entregas_audit, ext_incidencias_audit")
bloque(870, 430, 1360, 505, "Restricciones físicas", "CHECK (OCL01, OCL07) e índices únicos sobre columnas generadas (OCL03, OCL04); índices en todas las claves ajenas")

# Copias y repositorio
bloque(850, 590, 1380, 670, "Copias de seguridad", "Volcado cifrado de la base de datos en un almacenamiento separado; restauración probada (RNF04)")
bloque(290, 430, 770, 510, "Repositorio Git", "Código del paquete y configuración versionados (RNF05); nunca contiene datos personales")

# Flujos
E.flecha(d, 220, 160, 290, 160)
d.text((E.px(228), E.px(136)), "HTTPS", font=fp, fill=E.TEXTO)
E.flecha(d, 770, 250, 850, 250)
E.texto_centrado(d, (772, 196, 848, 246), "usuario de BD con permisos mínimos", fp)
E.flecha(d, 1115, 520, 1115, 590)
E.flecha(d, 530, 430, 530, 360, discontinua=True)
d.text((E.px(540), E.px(385)), "despliegue del paquete", font=fp, fill=E.TEXTO)

ruta = E.guardar(img, "bd_fisico.png")
print(ruta, img.size)
