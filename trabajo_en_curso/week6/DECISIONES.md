# Decisiones (Week 6)

Continúa la numeración de `trabajo_en_curso/week5/DECISIONES.md`. Si una decisión corrige otra, lo dice expresamente («corrige D-NN»).

---

## D-08 · La inscripción vincula alumno y grupo

- **Problema:** la memoria (1.2.7) dice que una inscripción vincula alumno y **grupo**; el caso de uso CU02 habla de las inscripciones de la **actividad**.
- **Opciones:** (a) inscripción en la actividad; (b) inscripción en el grupo, con la actividad obtenida a través del grupo.
- **Decisión:** (b).
- **Justificación:** una actividad puede tener varios grupos con horarios y monitores distintos, y la lista de una sesión solo debe contener a los alumnos de su grupo. La lista por actividad sigue siendo posible.
- **Cambios aplicados:** diseño conceptual, lógico y físico del capítulo 5 (`ext_inscripciones.grupo_id`).
- **Validación:** **pendiente de confirmar con la directora** (era una de las preguntas abiertas de la Week 5). Si se confirma, conviene ajustar el texto de CU02.

## D-09 · Correcciones de asistencia mediante la auditoría de SuiteCRM

- **Problema:** OCL03 exige un único registro de asistencia por alumno y sesión, y la regla R07 pide conservar el historial de las correcciones.
- **Opciones:** (a) una entidad propia de historial de asistencia; (b) un único registro por alumno y sesión con la auditoría de campos de SuiteCRM (`ext_asistencias_audit`).
- **Decisión:** (b).
- **Justificación:** cumple las dos reglas sin duplicar datos y usa un mecanismo que la plataforma ya ofrece y que también sirve para autorizaciones, entregas e incidencias.
- **Cambios aplicados:** capítulo 5 (5.2, 5.4.3) y diagrama físico.
- **Validación:** pendiente de confirmar con la directora; se comprobará en la prueba P03.

## D-10 · Criterio eliminatorio «gratuito y de código abierto» en la selección del CRM

- **Problema:** la matriz provisional (Tabla 3) trataba el coste y la licencia como un criterio más (10 %) y solo comparaba tres plataformas.
- **Decisión:** lista larga de 9 CRM; filtro eliminatorio (licencia aprobada por la OSI, sin coste por usuario, autoalojable); matriz de 6 criterios sobre la lista corta (SuiteCRM 8, Odoo Community, EspoCRM, CiviCRM), en la que «Comunidad y documentación» sustituye a «Coste y licencia»; análisis de sensibilidad.
- **Justificación:** lo pidió el estudiante (23/11/2026) y encaja con el presupuesto (3.1.1) y con RNF02.
- **Resultado:** SuiteCRM 4,00; EspoCRM 3,80; Odoo Community 3,75; CiviCRM 3,50. Con pesos iguales, SuiteCRM sigue primero.
- **Validación:** las notas son documentales; se confirman con las pruebas de concepto del apartado 1.2.5 de la memoria (equivalen al guion PC01–PC07 de `Docu_Parcial/01_Analisis_y_preparacion.docx`, que la memoria no recoge). Por decisión del estudiante (23/11/2026), las pruebas con los CRM distintos de SuiteCRM se harán más adelante.

## D-11 · Detalles del modelo de datos

- La autorización es una entidad asociativa entre alumno y persona autorizada.
- Las personas autorizadas reutilizan `contacts` del núcleo (campo `relacion_c`); los usuarios, `users`.
- El estado «vencida» de una autorización se calcula con las fechas; solo se guarda activa/revocada.
- No se declaran claves ajenas en la base de datos (convención de SuiteCRM); hay un índice en cada columna de clave ajena.
- OCL03 y OCL04 se implementan con índices únicos sobre columnas generadas que valen nulo cuando el registro está borrado (borrado lógico).
- Los diagramas de base de datos (figuras 6–8) van en página apaisada (`sidewaysfigure`) para que se puedan leer.
