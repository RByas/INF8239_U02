# INF-8239 · Unidad 02 · Proyecto NLP

Autor académico: Edwin Ramón José Nolasco
Estudiante: Roberto Byas

Proyecto base para LAB04–LAB06. No sustituya la comprensión por ejecución mecánica.

**Pregunta de investigación.** ¿Puede un clasificador clásico (TF-IDF + modelo lineal) asignar el tipo de entidad de un resumen de Wikipedia entre 14 clases de DBpedia, y en qué clases y por qué se equivoca?

## Inicio rápido

```bash
uv python install 3.12
uv sync
cp .env.example .env          # y configure el dataset (ver "Dataset")
uv run pytest -q
uv run python scripts/audit_data.py
```

## Dataset

- Dataset aprobado: DBpedia14 (`fancyzhx/dbpedia_14`), clasificación de temas en 14 clases.
- Fuente original: https://huggingface.co/datasets/fancyzhx/dbpedia_14
- Licencia: CC BY-SA 3.0 y GNU FDL (ver `docs/DATASET_CARD.md`).
- Versión fijada: commit `9abd46cf7fc8b4c64290f26993c540b92aa145ac` de Hugging Face.
- Candidato descartado y justificación: `docs/dataset_candidates.csv`.

### Cómo obtener los datos

Los datos no se incluyen en Git (`data/raw/` está excluido). Se obtienen así:

1. Use esta configuración en `.env`:

```
DATA_SOURCE=local
DATASET_PATH=data/raw/dataset.csv
DATASET_URL=https://huggingface.co/datasets/fancyzhx/dbpedia_14
TEXT_COLUMN=content
TARGET_COLUMN=label
RANDOM_STATE=42
```

2. Genere el CSV desde la fuente pública (el dataset se distribuye en parquet, no como CSV descargable por URL):

```bash
uv run python scripts/prepare_dbpedia.py
```

   El script imprime el SHA-256 del archivo; regístrelo en `docs/DATASET_CARD.md`.

3. Confirme la configuración:

```bash
uv run python scripts/download_data.py
```

Para otro dataset que sí sea un CSV con enlace directo, use `DATA_SOURCE=url` y `DATASET_URL` en `.env`.

El archivo `data/sample/demo_text.csv` solamente comprueba la arquitectura.

## Entrenamiento

```bash
uv run python scripts/train_text.py
uv run streamlit run app/streamlit_app.py
```

`train_text.py` entrena el baseline, Complement Naive Bayes y regresión logística con el mismo vectorizador (TF-IDF de 1 a 2 gramas, `min_df=5`, sin límite de `max_features`) y la misma partición estratificada 75/25. Genera `reports/text_metrics.csv`, `reports/confusion_text.png`, `reports/error_analysis.csv` y `models/text_model.joblib` (unos 55 MB, comprimido con `compress=3`).

## Pruebas

```bash
uv run pytest -q
```

Resultado esperado: `6 passed`.

- `tests/test_text_model.py` ajusta cada pipeline (baseline, Naive Bayes y regresión logística) con cuatro textos de ejemplo y comprueba que predice una etiqueta y que contiene los pasos `tfidf` y `model`.
- `build_models()` usa por defecto `min_df=1` y sin límite de vocabulario para que esa prueba funcione con pocos textos. `scripts/train_text.py` pasa explícitamente `min_df=5` y `max_features=None` para el corpus real.
- Las pruebas no necesitan el dataset real ni red: usan datos de ejemplo.
- Las comprobaciones sobre los datos reales están en el notebook (ver "Reproducibilidad").

## Reproducibilidad

**Entorno.** Python 3.12 y las versiones exactas de `uv.lock` (`uv sync`). Ejecutado por el autor en Windows con Git Bash. `requirements.txt` se genera desde `uv.lock`:

```bash
uv export --format requirements-txt --no-hashes --no-emit-project --output-file requirements.txt
```

**Orden de ejecución completo:**

```bash
uv sync
uv run pytest -q
uv run python scripts/prepare_dbpedia.py     # genera data/raw/dataset.csv (no se versiona)
uv run python scripts/audit_data.py
uv run python scripts/train_text.py          # métricas, matriz, errores y modelo
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/ejercicio03.ipynb
uv run streamlit run app/streamlit_app.py
```

El notebook `notebooks/ejercicio03.ipynb` integra la auditoría, las métricas, la matriz de confusión y el análisis de 20 errores. Requiere `reports/error_sample_20.csv`. Para ejecutarlo se necesitan `jupyter`, `nbconvert` e `ipykernel` en el entorno (`uv add --dev jupyter nbconvert ipykernel`).

**Fuentes de aleatoriedad controladas.** `RANDOM_STATE=42` fija la partición estratificada y los modelos. La muestra de 20 errores también usa la semilla 42.

**Versión de los datos.** Commit `9abd46cf7fc8b4c64290f26993c540b92aa145ac` de Hugging Face. SHA-256 del CSV generado: `___` (copiar de la salida de `audit_data.py`).

**Resultados esperados** (ejecución con `min_df=5` y `max_features=None`):

| Dato | Valor |
|---|---|
| Filas del CSV / duplicados de texto | 630,000 / 138 |
| Filas tras limpiar (entrenamiento / prueba) | 629,862 (472,396 / 157,466) |
| F1 macro baseline / Naive Bayes / regresión logística | 0.0095 / 0.9696 / 0.9844 |
| Errores de la regresión logística | 2,452 de 157,466 |

**Cómo comprobar que obtuvo lo mismo.** El notebook incluye tres comprobaciones que detienen la ejecución si algo no cuadra:

1. No hay textos idénticos entre entrenamiento y prueba.
2. El F1 macro recalculado con `models/text_model.joblib` coincide con `reports/text_metrics.csv`.
3. Las 20 filas de `reports/error_sample_20.csv` aparecen en `reports/error_analysis.csv` (20 de 20), es decir, provienen de la misma ejecución.

**Qué puede variar.**

- Los tiempos: el ajuste de la regresión logística tarda varios minutos y necesita bastante memoria.
- Si aparece `ArrayMemoryError`, cambie en `scripts/train_text.py` a `max_features=200_000`. Eso reduce la memoria y el modelo a unos 30 MB, pero cambia ligeramente las métricas (Naive Bayes 0.9686 y 2,451 errores en la ejecución con ese límite), y obliga a regenerar `reports/` completo.
- El SHA-256 del CSV puede cambiar si cambian las versiones de `pandas` o `datasets`. En ese caso, compare el número de filas y el esquema antes de concluir que los datos son distintos.

## Portabilidad local/nube

- El código no contiene rutas absolutas ni credenciales: todo se configura en `.env`, que no se sube a Git (se versiona solo `.env.example`).
- Se conserva `uv.lock` en el repositorio. Se excluyen `.venv/`, `.env` y `data/raw/`.
- En Google Colab no se copia la carpeta `.venv`; se instalan las dependencias con `requirements-colab.txt`:

```python
!git clone <URL_DEL_REPOSITORIO>
%cd <CARPETA_DEL_REPOSITORIO>
!pip install -r requirements-colab.txt
# Cree el archivo .env con la configuración de arriba y ejecute los scripts con python.
```

## Uso de IA

La declaración de herramientas, prompts, partes verificadas y correcciones está en `docs/declaracion_ia.md`.

## Interpretación

Toda conclusión debe separar observación, evidencia, interpretación y decisión.