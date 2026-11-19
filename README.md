# TFG_Project

Proyecto de TFG: SELECCIÓN DEL CRM MÁS ADECUADO PARA EL CONTROL SEGURO DE ACTIVIDADES EXTRAESCOLARES EN PRIMARIA.

Trabajo Final de Grado del Grado en Ingeniería Informática (especialidad de Sistemas de Información), Facultat d'Informàtica de Barcelona (UPC).

- **Estudiante:** Diego Salas
- **Directora:** Carme Martín Escofet
- **Tutora de GEP:** Giovanna Lara
- **Periodo de ejecución:** 19/10/2026 – 10/01/2027

## Objetivo

Analizar el sistema de información de las actividades extraescolares de un centro de primaria, seleccionar la plataforma CRM más adecuada y adaptarla para:

- controlar la **asistencia** en cada sesión;
- mantener la **trazabilidad de la custodia** y la entrega del alumno a una persona autorizada;
- gestionar y comunicar **incidencias** con permisos por rol y protección de datos desde el diseño.

La plataforma candidata es **SuiteCRM 8** (matriz ponderada: 4,10 sobre 5, frente a Odoo con 3,85 y Salesforce Education Cloud con 3,80). La decisión definitiva depende de las pruebas de concepto equivalentes (hito H2).

## Estructura del repositorio

```
├── Documentation/
│   ├── GEP/                      Entregables de Gestión de Proyectos (GEP1–GEP4)
│   │   └── GEPn/versiones_anteriores/
│   ├── Docu_Final/
│   │   ├── Docu_Parcial/         Documentos intermedios (estado del arte, análisis, especificación)
│   │   └── Memoria/              Memoria final del TFG
│   └── Reuniones/                Actas de las reuniones con la directora
├── generadores/                  Scripts que generan los diagramas de la memoria (Pillow + Lora)
├── SuiteCRM/                     Paquete de extensión «Gestión de Extraescolares» (prototipo)
├── validacion/                   Datos sintéticos, pruebas P01–P09 y resultados
├── trabajo_en_curso/             Estado del trabajo y decisiones semanales (weekN/); no es un entregable
└── requirements.txt              Dependencias de Python
```

## Entorno

- **Python 3.12** en Windows: `python -m pip install -r requirements.txt`.
- **SuiteCRM 8** en WSL2 con Ubuntu 24.04 (Apache, PHP y MariaDB).

## Convención de commits

`[TIPO] Week_N #issue: descripción en castellano, en infinitivo`. Los tipos son `IMP` (contenido o funcionalidad nueva), `FIX` (corrección) y `REF` (reorganización). Si el commit resuelve una issue, el cuerpo incluye `Closes #N`.

## Datos

El proyecto trabaja **exclusivamente con datos sintéticos**. No se deben añadir al repositorio datos reales de menores, familias ni del centro colaborador: ni nombres, ni teléfonos, ni documentos de identidad, ni volcados de base de datos con datos reales.
