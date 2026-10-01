"""Genera data/raw/dataset.csv a partir de fancyzhx/dbpedia_14 (Hugging Face).

Script auxiliar: no reemplaza a download_data.py. Se usa porque el dataset se
distribuye en parquet (train/test) y no como un CSV descargable por URL.
Uso:  python prepare_dbpedia.py
Requiere: pip install datasets pandas pyarrow
"""
from __future__ import annotations

import os

import pandas as pd
from datasets import load_dataset

from inf8239_u02.config import ROOT
from inf8239_u02.data import sha256

REPO_ID = "fancyzhx/dbpedia_14"
# Revision fijada para reproducibilidad (consultada el 30/09/2026).
REVISION = os.getenv("DATASET_REVISION", "9abd46cf7fc8b4c64290f26993c540b92aa145ac")
OUTPUT = ROOT / "data/raw/dataset.csv"


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ds = load_dataset(REPO_ID, revision=REVISION)

    frames = []
    for split_name, split in ds.items():  # train y test, en ese orden
        df = split.to_pandas()
        df["split"] = split_name
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)

    # Columna `text` = titulo + contenido (el titulo puede venir vacio).
    title = df["title"].fillna("").str.strip()
    content = df["content"].fillna("").str.strip()
    df["text"] = content.where(title == "", title + ". " + content)

    df.to_csv(OUTPUT, index=False)
    print(f"Repositorio: {REPO_ID}")
    print(f"Revision: {REVISION}")
    print(f"Filas: {len(df)} | Columnas: {list(df.columns)}")
    print(f"Guardado: {OUTPUT}")
    print(f"SHA-256: {sha256(OUTPUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())