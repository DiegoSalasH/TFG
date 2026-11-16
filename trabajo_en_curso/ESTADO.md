# Estado del TFG (actualizado el 16/11/2026, semana 5 del plan)

Carpeta de trabajo para retomar el proyecto. No es un entregable del TFG: al terminar se puede borrar, o mover lo útil a `validacion/` o a `Documentation/`.

## Qué está hecho

| Fase | Estado | Dónde |
|---|---|---|
| GEP1–GEP4 | Entregados | `Documentation/GEP/` |
| Análisis y preparación (proceso de referencia, reglas R01–R07, guion de PoC PC01–PC07) | Terminado el 02/11/2026; el proceso sigue siendo una hipótesis | `Documentation/Docu_Final/Docu_Parcial/01_Analisis_y_preparacion.docx` |
| Especificación (CU01–CU07, modelo conceptual, OCL01–OCL08, Volere, HU01–HU13, pruebas P01–P09) | Versión del 16/11/2026 | `Documentation/Docu_Final/Docu_Parcial/02_Especificacion.docx` |
| Memoria | Borrador basado en el GEP4 ampliado | `Documentation/Docu_Final/Memoria/Memoria_TFG_Diego_Salas.docx` |

## Hitos

| Hito | Fecha | Estado |
|---|---|---|
| H1 Requisitos y procesos validados | 08/11 | Pendiente: no hay centro colaborador identificado (riesgo R1) |
| H2 CRM seleccionado y justificado | 22/11 | Pendiente: falta instalar SuiteCRM y ejecutar PC01–PC07 |
| H3 Modelo, permisos y configuración base | 13/12 | — |
| H4 Módulos de asistencia, custodia e incidencias | 02/01 | — |
| H5 Pruebas y validación funcional | 05/01 | — |
| H6 Memoria cerrada y entrega | 10/01 | — |

## Pendiente

### Memoria
- [ ] Cambiar la portada, que sigue siendo la del GEP4 («Entregable 4», 12/10/2026).
- [ ] Redactar Resum, Resumen y Summary.
- [ ] Bibliografía: añadir [31]–[33], que se citan pero no aparecen en la lista; revisar [14], [15], [21], [22] y [30], que están en la lista pero no se citan.
- [ ] Numeración de tablas: hay dos «Tabla 6», y las páginas del índice de tablas no coinciden.
- [ ] En 4.3, los 12.501,58 € son el coste del TFG, no el de una puesta en producción.
- [ ] Añadir el estado del arte y los capítulos de análisis, diseño, implementación, pruebas y conclusiones.

### Planificación y presupuesto
- [ ] H4→H5 (3 días para 62 h) y H5→H6 (5 días para 60 h) no se pueden cumplir; además, la validación con usuarios cae en Navidad.
- [ ] Contingencia: las 45 h se reparten entre R1–R4 en 2.4.1, pero R1–R4 se presupuestan aparte como imprevistos. Elegir un único criterio.
- [ ] Unificar los nombres de R3 y R4 entre la Tabla 12 y la Tabla 18.

### Especificación
- [ ] Unificar la numeración RF/RNF: la del documento de Análisis no coincide con la de la Memoria y la Especificación.
- [ ] OCL02 usa `vigente()`, cuyo `def:` se perdió en la versión final; `toDate()` no es OCL estándar.
- [ ] OCL03 (asistencia única) choca con R07 (conservar las correcciones): hace falta una entidad de historial o un atributo `activa`.
- [ ] Añadir al diccionario de entidades: Inscripción, Actividad, Grupo, Contacto/PersonaAutorizada, Usuario y Actuación.
- [ ] Decidir si la lista de la sesión sale de la actividad o del grupo.
- [ ] Recuperar en las fichas Volere los campos Prioridad, Fuente y Riesgo.
- [ ] Justificar o rebajar los 10.000 alumnos de RNF02.

### Prototipo
- [ ] Instalar SuiteCRM 8 en local y ejecutar PC01–PC07 (hito H2).
- [ ] Instalar Git e inicializar el repositorio; publicarlo en GitHub cuando se pueda iniciar sesión.
