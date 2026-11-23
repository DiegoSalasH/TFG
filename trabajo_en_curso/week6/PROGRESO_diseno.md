# Progreso: capítulo 5 «Diseño» y reorganización de los RNF

Encargado el 23/11/2026 (Week 6). Instrucciones del estudiante: **no hacer commit**; al acabar, recompilar el PDF. Usar las skills (humanizer, etc.).

## Pasos

- [x] 1. Verificar en fuentes oficiales la licencia y el coste de los CRM que se comparan: EspoCRM (AGPLv3, coste 0 autoalojado, extensiones de pago), Vtiger CE (VPL, derivada de MPL, no aprobada por la OSI), CiviCRM (AGPLv3 con excepción), Zoho CRM (edición gratuita para 3 usuarios, propietario), HubSpot (plan gratuito, SaaS propietario)
- [x] 2. Sostenibilidad pasa al capítulo 6 (`06_sostenibilidad.tex` con `git mv`, etiquetas `sec:sost-*`; `main.tex` incluye `05_diseno` y `06_sostenibilidad`)
- [x] 3. Capítulo 5 «Diseño» (`capitulos/05_diseno.tex`): 5.1 selección de la plataforma CRM (proceso, comparación con el mercado, criterio «gratuito y código abierto», adecuación)
- [x] 4. 5.2 Diseño conceptual de la base de datos (diagrama + explicación)
- [x] 5. 5.3 Diseño lógico (esquema relacional + diagrama)
- [x] 6. 5.4 Diseño físico (MariaDB/SuiteCRM: tipos, índices, restricciones, auditoría, DDL). Paquetes `listings` y `rotating` añadidos a `main.tex`
- [x] 7. Generadores de los diagramas nuevos (`gen_seleccion_crm.py`, `gen_bd_conceptual.py`, `gen_bd_logico.py`, `gen_bd_fisico.py` + módulo común `diagramas_bd.py`), con los PNG en `Latex_Memoria/imagenes/` (`estilo.SALIDA` apunta ahora ahí). Todos revisados visualmente
- [x] 8. Fichas Volere: quitadas del capítulo 4 (antes 4.3) y puestas en 1.3.4 en lugar de la tabla resumen de RNF
- [x] 9. RNF divididos: RNF01 Seguridad, RNF02 Privacidad, RNF03 Rendimiento, RNF04 Recuperación, RNF05 Mantenibilidad, RNF06 Usabilidad y accesibilidad (contenido igual que el antiguo RNF03). Se añade la fila «Prioridad» a cada ficha (estaba solo en la tabla resumen eliminada). Etiquetas `tab:rnf01`…`tab:rnf06`
- [x] 10. Referencias actualizadas: CU01, CU02 y CU05–CU07 → «RNF01, RNF02»; CU03 y CU04 → «RNF01, RNF02, RNF06»; P09 → «RNF01-RNF06»; sostenibilidad → RNF06; introducción y Tabla de enfoque del capítulo 4 remiten a 1.3.4
- [x] 11. Bibliografía nueva y citas (ref42–ref52)
- [x] 12. Recompilar el PDF y revisarlo visualmente (74 páginas, sin referencias sin resolver; diagramas de BD en página apaisada)

## Decisiones tomadas en esta tarea

(se anotan aquí y en `trabajo_en_curso/week6/DECISIONES.md`)
