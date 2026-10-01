# Dataset Card

## Identificación
- Nombre: DBpedia14 (DBpedia Ontology Classification Dataset), repositorio `fancyzhx/dbpedia_14`
- Fuente original: https://huggingface.co/datasets/fancyzhx/dbpedia_14
  - Repositorio del autor: https://github.com/zhangxiangxiao/Crepe
  - Paper: https://arxiv.org/abs/1509.01626
  - Datos de origen: DBpedia 2014 (https://wiki.dbpedia.org/develop/datasets)
- Responsable: Roberto Byas
- Versión o fecha: extracto de DBpedia 2014. Revisión de Hugging Face consultada el 30/09/2026: commit `9abd46cf7fc8b4c64290f26993c540b92aa145ac` (último cambio del README en la rama `main`). SHA-256 del CSV generado: `___` (completar con la salida de `prepare_dbpedia.py`).
- Licencia: CC BY-SA 3.0 y GNU Free Documentation License (declaradas en la ficha de Hugging Face). Exige atribución y compartir igual las obras derivadas del dataset.
- Idioma: inglés principalmente; pueden aparecer otros idiomas (por ejemplo, títulos de películas que no están originalmente en inglés).
- Autores del dataset: Xiang Zhang, Junbo Zhao, Yann LeCun (NeurIPS 2015). Datos fuente: DBpedia (Lehmann et al., 2015).

## Propósito y variable objetivo
**Uso previsto:** clasificación de temas (`topic-classification`). Dado el texto de un artículo de Wikipedia, predecir a cuál de 14 clases de la ontología de DBpedia pertenece. Se usa con fines académicos de comparación de modelos de clasificación de texto.

**Variable objetivo:** `label` (`TARGET_COLUMN=label`), 14 clases mutuamente excluyentes.

**Columna de texto utilizada:** `content` (`TEXT_COLUMN=content`). El título (`title`) no se usa como entrada del modelo en la configuración actual.

**Origen de las etiquetas:** generadas automáticamente (`machine-generated`) a partir de la ontología de DBpedia, no por anotadores humanos.

## Diccionario de datos

Columnas del archivo `data/raw/dataset.csv` (630,000 filas: 560,000 de `train` y 70,000 de `test`).

| Columna | Tipo | Descripción | Valores o unidad |
|---|---|---|---|
| `label` | entero (categórica) | Clase de la ontología DBpedia a la que pertenece la entidad. Es la variable objetivo. | 0 Company, 1 EducationalInstitution, 2 Artist, 3 Athlete, 4 OfficeHolder, 5 MeanOfTransportation, 6 Building, 7 NaturalPlace, 8 Village, 9 Animal, 10 Plant, 11 Album, 12 Film, 13 WrittenWork. En el CSV original del autor los índices van de 1 a 14; aquí van de 0 a 13. |
| `title` | texto | Título del artículo (nombre de la entidad). Puede venir vacío. | Texto libre, entre 2 y 171 caracteres según la vista previa de Hugging Face. Sin unidad. |
| `content` | texto | Resumen o cuerpo del artículo. Es la columna de entrada del modelo (`TEXT_COLUMN`). | Texto libre, entre 3 y 13,600 caracteres según la vista previa de Hugging Face. Sin saltos de línea. |
| `split` | texto (categórica) | División original del dataset a la que pertenece la fila. Columna agregada en este proyecto. | `train` (560,000 filas) o `test` (70,000 filas) |
| `text` | texto | Título y contenido unidos. Columna derivada, agregada en este proyecto. | `title. content` si hay título; solo `content` si el título está vacío |

Distribución por clase en los datos originales: 40,000 ejemplos de entrenamiento y 5,000 de prueba por cada una de las 14 clases. Este balance es artificial (muestreo uniforme por clase).

## Procedimiento de obtención
El dataset se distribuye en archivos parquet (train y test), no como un CSV descargable por URL, por lo que `download_data.py` se usa en modo `local` y el CSV se genera con un script auxiliar.

1. Instalar dependencias: `pip install datasets pandas pyarrow`
2. Ejecutar `python prepare_dbpedia.py`. Carga `fancyzhx/dbpedia_14` con `revision="9abd46cf7fc8b4c64290f26993c540b92aa145ac"` y escribe `data/raw/dataset.csv`.
3. Configuración en `.env`:

```
DATA_SOURCE=local
DATASET_PATH=data/raw/dataset.csv
DATASET_URL=https://huggingface.co/datasets/fancyzhx/dbpedia_14
TEXT_COLUMN=content
TARGET_COLUMN=label
RANDOM_STATE=42
```

4. Ejecutar `python download_data.py`, que en modo local confirma la ruta del archivo configurado.
5. Registrar la fecha de descarga y el SHA-256 que imprime el script.
6. Semilla aleatoria: `RANDOM_STATE=42` para cualquier muestreo o división adicional.

## Transformaciones realizadas
Solo se aplicaron estas transformaciones sobre los datos originales:

1. **Unión de divisiones:** se concatenaron `train` y `test` en un único CSV, y se agregó la columna `split` para poder recuperar la división original.
2. **Columna derivada `text`:** se creó uniendo `title` y `content` (con espacios recortados y valores nulos tratados como texto vacío). Si el título está vacío, `text` es igual a `content`.
3. **Formato:** se guardó en CSV sin índice. Las etiquetas se mantienen como enteros de 0 a 13, que es la codificación de Hugging Face (el CSV original del autor usaba 1 a 14).

No se aplicó limpieza de texto, cambio a minúsculas, eliminación de duplicados, filtrado de filas ni corrección de etiquetas. Cualquier preprocesamiento posterior (por ejemplo, vectorización) se documenta aparte.

## Ejemplos anonimizados
Los siguientes cinco ejemplos se tomaron de la vista previa pública del dataset en Hugging Face (cuatro de la clase `0 Company` del conjunto de entrenamiento y uno de la documentación del conjunto de prueba). Para esta ficha se reemplazaron los nombres de entidades y lugares por marcadores. La anonimización se aplica solo a estos ejemplos de la documentación; el archivo de datos no se modifica.

**Ejemplo 1** (`label` = 0, Company)
- `title`: `[ENTIDAD_1]`
- `content`: "[ENTIDAD_1] was a British coachbuilding business based in [LUGAR_1], trading under that name from 1929. A major part of their output was under sub-contract to motor vehicle manufacturers. Their business closed in 1972."

**Ejemplo 2** (`label` = 0, Company)
- `title`: `[ENTIDAD_2]`
- `content`: "[ENTIDAD_2] is a German maker of pens for writing, colouring and cosmetics as well as markers and highlighters for office use. It is the world's largest manufacturer of highlighter pens."

**Ejemplo 3** (`label` = 0, Company)
- `title`: `[ENTIDAD_3]`
- `content`: "[ENTIDAD_3] is a porcelain manufacturer in the Czech Republic."
- Observación: texto muy corto (una sola frase).

**Ejemplo 4** (`label` = 0, Company, etiqueta dudosa)
- `title`: `[ENTIDAD_4]`
- `content`: "[ENTIDAD_4] is a person who plays wow"
- Observación: el texto describe a una persona y no a una empresa, pero el dataset la etiqueta como Company. Muestra ruido en las etiquetas automáticas.

**Ejemplo 5** (`label` = 0, Company, conjunto de prueba)
- `title`: (vacío)
- `content`: " [ENTIDAD_5] is an American alcoholic beverage company that specializes in sake and other spirits. The privately-held company was founded in 2004 and is headquartered in [LUGAR_2]. [...]"
- Observación: el título viene vacío y el contenido empieza con un espacio.

Limitación de esta sección: los cinco ejemplos pertenecen a la clase `0 Company` porque son los que se veían en la vista previa. Conviene reemplazarlos por ejemplos de otras clases (por ejemplo, `2 Artist`, `9 Animal`, `12 Film`) tras ejecutar `prepare_dbpedia.py`, aplicando la misma anonimización.

## Calidad observada
Lo que confirma la documentación de la fuente:
- Clases balanceadas: 40,000 ejemplos de entrenamiento y 5,000 de prueba por clase. No hay clases extremadamente pequeñas. El balance es artificial y no refleja la proporción real de cada tipo de entidad en Wikipedia.
- Las etiquetas son automáticas y la ficha original no documenta proceso de anotación ni tasa de error.
- Pueden existir títulos vacíos y textos en idiomas distintos del inglés.

Lo que se observó en la vista previa (primeras filas de la clase Company; no es una medición sobre todo el dataset):
- Etiquetas dudosas: una fila etiquetada Company dice solo que alguien "plays wow" (Ejemplo 4).
- Texto que no presenta a la entidad: el contenido de una fila habla de inversiones de una cervecera en lugar de describir a la empresa titulada.
- Restos de la sintaxis de Wikipedia en el texto, como la cadena "Template:What?".
- Longitudes muy variables: `title` de 2 a 171 caracteres y `content` de 3 a 13,600.

Pendiente de verificar al ejecutar el análisis (completar con los resultados reales):
- Nulos o vacíos en `title` y `content`: ___
- Filas duplicadas (mismo `title` + `content`) y duplicados entre `train` y `test`: ___
- Longitud de `content` (mínimo, mediana, máximo): ___
- Revisión manual de una muestra por clase para estimar la ambigüedad de las etiquetas: ___

## Población cubierta y excluida
**Cubierta:** entidades de 14 tipos (empresas, instituciones educativas, artistas, atletas, cargos públicos, medios de transporte, edificios, lugares naturales, pueblos, animales, plantas, álbumes, películas y obras escritas) con artículo en Wikipedia según DBpedia 2014, muestreadas de forma uniforme por clase.

**Excluida:**
- Cualquier tema fuera de esas 14 clases (ciencia, eventos, conceptos abstractos, etc.).
- Otros idiomas, salvo fragmentos aislados.
- Contenido posterior a 2014: no refleja entidades, cargos ni hechos actuales.
- Entidades sin artículo o sin resumen en Wikipedia.
- Texto informal o de redes sociales: el estilo es enciclopédico.
- Personas, regiones y temas poco cubiertos por Wikipedia en inglés.

## Riesgos, sesgos y usos prohibidos
**Sesgos previsibles:**
- Sesgo de Wikipedia: la cobertura depende de quién edita y tiende a favorecer temas y regiones anglosajones y occidentales.
- Etiquetas automáticas: los errores de la ontología se heredan al dataset (Ejemplo 4).
- Datos desactualizados: es un corte de 2014.
- Balance artificial: el modelo verá las 14 clases con la misma frecuencia, lo que no ocurre en textos reales.
- Tarea probablemente fácil: muchos resúmenes nombran el tipo de entidad en la primera frase ("is a ... company"), por lo que las métricas pueden sobreestimar el desempeño en textos menos explícitos. Es una inferencia a partir de los ejemplos vistos, no una medición.

**Riesgos de privacidad:** no hay datos privados, pero los textos de las clases Artist, Athlete y OfficeHolder describen a personas reales con información ya pública en Wikipedia. La ficha original no documenta este punto, por lo que es una inferencia y debe revisarse.

**Riesgo de licencia:** CC BY-SA 3.0 y GFDL exigen atribución y compartir igual las obras derivadas del dataset. Conviene revisarlo antes de redistribuir versiones transformadas de los datos.

**Usos prohibidos o desaconsejados:**
- Tomar decisiones sobre personas (perfilado, evaluación, vigilancia) a partir de los textos o de las predicciones del modelo.
- Presentar el contenido como información vigente o verificada.
- Redistribuir el dataset o versiones derivadas sin atribuir la fuente ni aplicar la misma licencia.
- Usar el dataset o un modelo entrenado con él en dominios distintos de artículos enciclopédicos sin una validación propia.

## Cita
- Zhang, X., Zhao, J., LeCun, Y. (2015). Character-level Convolutional Networks for Text Classification. Advances in Neural Information Processing Systems 28 (NeurIPS 2015).
- Lehmann, J., Isele, R., Jakob, M., Jentzsch, A., Kontokostas, D., Mendes, P. N., Hellmann, S. et al. (2015). DBpedia: a large-scale, multilingual knowledge base extracted from Wikipedia. Semantic Web 6(2), 167–195.