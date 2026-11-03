# IRWA Project — Part 2: Indexing and Evaluation

## Plan por etapas

| Etapa | Contenido | Punto del PDF |
| --- | --- | --- |
| 1 | Reutilizar el preprocesado de la parte 1, construir los dos índices invertidos y recuperar productos con consultas AND. | Part 1, punto 1 |
| 2 | Definir cinco consultas de prueba a partir del vocabulario del corpus y comprobar sus coincidencias. | Part 1, punto 2 |
| 3 | Implementar TF-IDF y ordenar los productos recuperados. | Part 1, punto 3 |
| 4 | Implementar P@K, R@K, AP@K, F1@K, MAP, MRR y NDCG, siguiendo las operaciones de NumPy y pandas del notebook de evaluación. | Part 2, punto 1 |
| 5 | Evaluar las dos consultas oficiales con `data/validation_labels.csv` y mostrar únicamente valores numéricos con tres decimales en la sección de resultados. | Part 2, punto 2 |
| 6 | Etiquetar manualmente la relevancia de las cinco consultas propias, evaluar y analizar métricas, resultados, limitaciones y posibles mejoras. | Part 2, punto 3 |

## Continuidad con la parte 1

Se mantienen el identificador `pid`, el preprocesado de texto, la limpieza de atributos y la separación entre `text_index` (título y descripción) y `detail_index` (atributos de `product_details`). Para cada término se unen las coincidencias de los dos campos y, después, se intersectan los conjuntos de todos los términos de la consulta. Así, cada producto recuperado contiene todos los términos procesados, aunque estén repartidos entre ambos campos.

Rating, precio, descuento y stock se conservan como metadatos numéricos para fases posteriores. La propuesta `quality_score = rating / 5`, con rating medio cuando falta, se mantiene. Su incorporación al ranking debe evaluarse en una fase posterior.

## Alcance implementado

`IRWA_part2.ipynb` completa las etapas 1 a 6: toda la Part 1 y la Part 2 del PDF, incluido el apartado 2.3 con etiquetas propias, evaluación y análisis.

El ranking usa TF-IDF con `TF = 1 + log(frecuencia)`, `IDF = log(N / DF) + 1` y similitud coseno. Las frecuencias de ambos campos se suman, sin pesos adicionales. Solo se ordenan productos que cumplen AND.

## Ejecución

Usar el entorno de la parte 1, con Python 3.8 o posterior y NumPy, pandas, NLTK, IPython, Jinja2 e ipykernel disponibles. Para ejecutar desde terminal también se necesitan nbformat y nbclient. Si falta el recurso de stopwords, ejecutar una vez `nltk.download("stopwords")`.

Abrir `IRWA_part2.ipynb`, seleccionar el kernel del entorno y ejecutar todas las celdas en orden. El notebook encuentra automáticamente el corpus y `validation_labels.csv` desde esta carpeta o desde la raíz del repositorio. No necesita ejecutar el notebook anterior.

## Convenciones de evaluación

Se evalúa con K = 3, 5 y 10. Las etiquetas oficiales cubren un subconjunto de productos. El ranking se genera sobre todo el corpus y se filtra a los productos juzgados, sin cambiar su orden. Los relevantes etiquetados que no cumplen AND siguen contando en el denominador de recall y AP y en el ideal de NDCG. No se asignan etiquetas a los productos no juzgados. Este protocolo mide el rendimiento dentro del conjunto juzgado.

P@K divide entre K incluso con menos resultados. AP@K divide entre `min(K, relevantes conocidos)`, en lugar de usar solo los relevantes recuperados como en el ejemplo del laboratorio. MAP y MRR promedian las dos consultas oficiales. NDCG usa la ganancia exponencial del laboratorio y todas las etiquetas disponibles para el ideal. Los cálculos no se redondean hasta su presentación.

La sección Part2-2 de validación oficial contiene solamente resultados numéricos con tres decimales, sin interpretación ni estadísticas adicionales. Los encabezados identifican las métricas y los índices identifican consulta y K.


## Apartado 2.3: evaluación propia

- `own_relevance_labels.csv`: 140.400 etiquetas binarias, una por cada combinación de los 28.080 productos y las cinco consultas.
- `own_review_examples.csv`: los diez primeros resultados de cada consulta, con título, atributos y etiqueta, para revisar las decisiones.
- La sección Part2-3 del notebook define los criterios de relevancia, calcula métricas propias para K = 3, 5 y 10, explica cada métrica y analiza resultados y limitaciones con ejemplos concretos.

Las etiquetas propias se generan mediante reglas explícitas sobre campos originales, separadas del score y del preprocesado del buscador. Se revisan ejemplos, pero no se presentan como una anotación humana exhaustiva. Los valores ausentes y contradictorios pueden introducir errores; se requiere validación humana independiente para considerar estos juicios definitivos. El notebook explica esta limitación y evita atribuir mejoras al sistema por comparar protocolos distintos.

Ambos CSV se regeneran al ejecutar la sección Part2-3. No se modifica el buscador ni el archivo de etiquetas oficiales. Todo el código del notebook permanece sin comentarios.

## Idioma e informe

Los apartados, explicaciones y etiquetas de salida del notebook están en inglés. `IRWA_part2_informe_es.pdf` contiene el informe en español, organizado según los puntos del enunciado original, con una introducción breve de lo reutilizado de la parte 1, fragmentos del código y los resultados de la ejecución.

## Organización según el enunciado

El notebook y el informe comparten la estructura `Previous`, `Part1-1`, `Part1-2`, `Part1-3`, `Part2-1`, `Part2-2` y `Part2-3`, con los subapartados `Part2-3.a`, `Part2-3.b` y `Part2-3.c`. Previous reúne la carga, el preprocesado y los metadatos reutilizados de la parte 1.
