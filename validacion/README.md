# Validación

Pruebas del prototipo, siempre con **datos sintéticos** (tareas T11–T13).

| Prueba | Cobertura |
|---|---|
| P01 Alta y vigencia | RF01, HU01–HU02, OCL01 |
| P02 Sesión y lista | RF02, HU03, OCL07 |
| P03 Asistencia | RF03, HU04, OCL03 |
| P04 Entrega autorizada | RF04, HU05, OCL02, OCL04 |
| P05 Excepción de entrega | RF04, HU06 |
| P06 Incidencia | RF05, HU07–HU08, OCL05 |
| P07 Comunicación | RF06, HU09, OCL08 |
| P08 Permisos | RF07, HU10–HU11, OCL06 |
| P09 Calidad e incrementos | RNF01–RNF03, RF08–RF09, HU12–HU13 |

Estructura prevista:

- `datos_sinteticos/`: generador y conjuntos de prueba.
- `resultados/`: fecha, versión, resultado esperado, resultado obtenido y defecto asociado de cada prueba.
- `salida/`: salidas temporales; no se suben al repositorio.
