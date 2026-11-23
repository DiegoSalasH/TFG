# Generadores de diagramas

Los diagramas de la memoria se generan con scripts de Python (Pillow) para poder regenerarlos cuando cambie el modelo y para que todos tengan el mismo aspecto.

## Reglas

- Cada diagrama tiene su script `gen_<nombre>.py`, que guarda un PNG en `Documentation/Docu_Final/Memoria/Latex_Memoria/imagenes/` (carpeta definida en `estilo.SALIDA`).
- **Los PNG generados no se editan a mano.** Si hay que cambiar algo, se cambia el script y se regenera.
- El estilo común (tipografía, colores, grosores y resolución) está en `estilo.py`. Si se cambia ahí, hay que regenerar todos los diagramas.
- La tipografía es **Lora**, la misma que el texto de la memoria. Los ficheros `.ttf` están en `fuentes/`, con su licencia SIL Open Font License (`OFL.txt`), así que los scripts funcionan igual en Windows y en Linux sin instalar nada.
- Después de regenerar, revisa la imagen: que se lea bien, que nada se solape y que la letra tenga un tamaño suficiente.

## Uso

```powershell
python -m pip install -r requirements.txt   # una vez
python generadores/gen_<nombre>.py
```

## Diagramas

`diagramas_bd.py` es un módulo común (cajas en rejilla, líneas ortogonales y etiquetas) que usan los tres diagramas de base de datos.

| Script | Figura de la memoria | Estado |
|---|---|---|
| `gen_casos_uso.py` | Figura 3. Diagrama de casos de uso del sistema | Pendiente |
| `gen_modelo_conceptual.py` | Figura 4. Modelo conceptual de asistencia, custodia e incidencias | Pendiente |
| `gen_seleccion_crm.py` | Figura 5. Proceso de selección de la plataforma CRM | Hecho |
| `gen_bd_conceptual.py` | Figura 6. Diseño conceptual de la base de datos | Hecho |
| `gen_bd_logico.py` | Figura 7. Diseño lógico de la base de datos | Hecho |
| `gen_bd_fisico.py` | Figura 8. Diseño físico del almacenamiento | Hecho |
| `gen_secuencia_*.py` | Secuencias de asistencia, custodia e incidencia | Pendiente |
