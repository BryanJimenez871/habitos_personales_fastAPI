## Análisis exploratorio — Power BI

Los siguientes gráficos fueron desarrollados en **Power BI** 
a partir de los registros almacenados en PostgreSQL y exportados 
a Google BigQuery mediante el pipeline de Airflow de este proyecto.
El objetivo es identificar patrones de comportamiento personal 
a partir de los datos generados por la aplicación.

### Gráfico: Cantidad de hábitos
Se agregó el gráfico de **_cantidad de hábitos_** que 
está en la misma aplicación 'habitos personales' y expresa
cuantos hábitos buenos y malos existen en la base de datos.

### Gráfico: Hábito completado
Este gráfico sirve para un hábito específico y analizar
que días de la semana se completa, para empezar a reconocer un patrón,
en este ejemplo se infiere que 'salir a correr' no se completa los días lunes,
martes y sábado, por lo cual se debería dar más énfasis en esos días, y hacer preguntas como
"¿Quiero correr todos los días? o ¿Dejarlos como días de descanso?.
Y así con cualquier hábito que se quiera analizar. 

### Gráfico: Top 3 hábitos a lo largo del tiempo
Acá ya son más habitos, y podría ser más si así se requiera, pero para una mejor visualización, 
se utilizó 3 hábitos, en donde se enfatiza si los hábitos se cumplen
o cada vez se hacen menos, con la finalidad de estar más consciente si se está mejorando o no. 