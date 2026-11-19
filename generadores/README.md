# Generadores de diagramas

Los diagramas de la memoria se generan con scripts de Python (Pillow) para poder regenerarlos cuando cambie el modelo y para que todos tengan el mismo aspecto.

## Reglas

- Cada diagrama tiene su script `gen_<nombre>.py`, que guarda un PNG en `Documentation/Docu_Final/Memoria/imagenes/`.
- **Los PNG generados no se editan a mano.** Si hay que cambiar algo, se cambia el script y se regenera.
- El estilo común (tipografía, colores, grosores y resolución) está en `estilo.py`. Si se cambia ahí, hay que regenerar todos los diagramas.
- La tipografía es **Lora**, la misma que el texto de la memoria. Los ficheros `.ttf` están en `fuentes/`, con su licencia SIL Open Font License (`OFL.txt`), así que los scripts funcionan igual en Windows y en Linux sin instalar nada.
- Después de regenerar, revisa la imagen: que se lea bien, que nada se solape y que la letra tenga un tamaño suficiente.

## Uso

```powershell
python -m pip install -r requirements.txt   # una vez
python generadores/gen_<nombre>.py
```

## Diagramas previstos

| Script | Figura de la memoria | Estado |
|---|---|---|
| `gen_casos_uso.py` | Figura 3. Diagrama de casos de uso del sistema | Pendiente |
| `gen_modelo_conceptual.py` | Figura 4. Modelo conceptual de asistencia, custodia e incidencias | Pendiente |
| `gen_arquitectura.py` | Arquitectura del sistema (capítulo de diseño) | Pendiente |
| `gen_er.py` | Esquema de la base de datos | Pendiente |
| `gen_secuencia_*.py` | Secuencias de asistencia, custodia e incidencia | Pendiente |
