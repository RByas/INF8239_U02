# Declaración de uso de IA · Ejercicio 03

## Herramientas
- Claude (Anthropic), en la interfaz web claude.ai, con búsqueda web. Modelo `Sonney versión: 5.5 
- Uso: apoyo para buscar y comparar datasets, explicar errores de ejecución, proponer pruebas, revisar la lectura de métricas y mejorar la redacción. El estudiante conserva la responsabilidad sobre datos, código, referencias y conclusiones.

## Prompts relevantes (resumidos)
1. Seleccionar dos datasets que cumplan los criterios de la guía (texto, etiqueta interpretable, licencia, reproducibilidad, riesgo) y completar `dataset_candidates.csv`.
2. Buscar corpus de texto con licencias claras y de uso libre.
3. Completar `DATASET_CARD.md` con el dataset elegido, incluido el diccionario de datos.
4. Adaptar la descarga: `download_data.py` no podía obtener DBpedia14 desde la URL de Hugging Face.
5. «Ejecutando `train_text.py` recibo este error» (`ArrayMemoryError` en la regresión logística).
6. «Esta prueba me da error» (`test_text_model.py`, `ValueError` por `min_df`).
7. Validar la lectura de métricas, la matriz de confusión y un borrador de cierre interpretativo.
8. Proponer una muestra reproducible de 20 errores con categorías sugeridas.
9. «Esta validación está fallando» (la comprobación del notebook que dio 19 de 20 filas).

## Código y documentos elaborados con apoyo de IA
- `scripts/prepare_dbpedia.py`: genera `data/raw/dataset.csv` desde Hugging Face.
- Cambio de `build_models` en `modeling.py` (parámetros `min_df` y `max_features`).
- `notebooks/ejercicio03.ipynb`: borrador generado con IA; el estudiante lo ejecutó y verificó sus salidas.
- Borradores de `docs/DATASET_CARD.md`, `README.md` y de la conclusión.
- Muestra de 20 errores (`reports/error_sample_20.csv`) con categorías sugeridas.

## Partes verificadas por el estudiante
- Licencia, versión y enlaces del dataset en la página original (confirmar).
- Auditoría ejecutada con `audit_data.py`: 630,000 filas, 0 nulos y 138 duplicados de texto.
- `uv run pytest -q`: 6 pruebas pasan.
- Que `text_metrics.csv`, `confusion_text.png` y `error_analysis.csv` provienen de una misma ejecución (2,452 errores, coincidentes con la matriz) y que la comprobación del notebook confirma las 20 filas de la muestra.
- Lectura de las 20 filas de error y asignación de su categoría final (confirmar o corregir las categorías sugeridas en `reports/error_sample_20.csv`).

## Correcciones realizadas a respuestas de la IA
- La IA sugirió inicialmente SMS Spam como candidato; yo lo descarte y eligi DBpedia14.
- La IA supuso que existía una columna `text`; el dataset trae `label`, `title` y `content`. Se usó `content` (el CSV generado incluye también `text`).
- La primera corrección del vectorizador (`min_df=5` fijo) rompió `test_text_model.py`, que entrena con 4 textos. Se corrigió haciendo `min_df` y `max_features` parámetros de `build_models`, con valores permisivos por defecto.
- La IA indicó que el modelo guardado se había entrenado con `max_features=None`, pero `train_text.py` pasaba `max_features=200_000`. La comprobación del notebook (19 de 20 filas) destapó que `reports/` venía de esa ejecución; se cambió a `max_features=None` y se reentrenó, de modo que todos los archivos provienen de una misma ejecución.
- La IA conjeturó una confusión Artist→Album; la matriz muestra que el cruce relevante es Artist↔OfficeHolder.
- Cifras de una ejecución anterior (F1 de Naive Bayes 0.9686, 459 falsos negativos de Company) se reemplazaron por las de la ejecución final (0.9696 y 446) tras detectar que `error_analysis.csv` y la matriz no coincidían.
- La IA citó 156,462 filas tras eliminar duplicados; el valor correcto es 629,862 (472,396 de entrenamiento y 157,466 de prueba).

## Alcance
- Las categorías de los 20 errores fueron sugeridas por la IA y revisadas por el estudiante.
- La IA no ejecutó el código sobre los datos del estudiante: las cifras provienen de los archivos y capturas que él aportó.