# INF-8239 · Unidad 02 · Proyecto NLP

Autor académico: Edwin Ramón José Nolasco

Proyecto base para LAB04. No sustituya la comprensión por ejecución mecánica.

## Inicio rápido

```bash
uv python install 3.12
uv sync
uv run pytest -q
uv run python scripts/audit_data.py
```

Copie `.env.example` como `.env` y configure el dataset aprobado.

## Dataset

- Dataset aprobado: DBpedia14 (`fancyzhx/dbpedia_14`), clasificación de temas en 14 clases.
- Fuente original: https://huggingface.co/datasets/fancyzhx/dbpedia_14
- Licencia: CC BY-SA 3.0 y GNU FDL (ver `docs/DATASET_CARD.md`).
- Versión fijada: commit `9abd46cf7fc8b4c64290f26993c540b92aa145ac` de Hugging Face.

### Cómo obtener los datos

Los datos no se incluyen en Git (`data/raw/` está excluido). Se obtienen así:

1. Copie `.env.example` como `.env` y use esta configuración:

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

Complete `docs/DATASET_CARD.md`, el diccionario, la licencia y el procedimiento de obtención.
El archivo `data/sample/demo_text.csv` solamente comprueba la arquitectura.

## Entrenamiento

```bash
uv run python scripts/train_text.py
uv run streamlit run app/streamlit_app.py
```

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

## Interpretación

Toda conclusión debe separar observación, evidencia, interpretación y decisión.