# /// script
# dependencies = [
#   "pandas",
#   "pyarrow",
# ]
# ///

import pandas as pd
from pathlib import Path
from utils.constants import DATASET_TYPES, DATASET_DATES


def export_csv_to_feather():
    """
    Converts the source CSV dataset to Parquet format.

    Reads the dataset from '../datasets/dataset.csv' using predefined types and date columns,
    converts specified columns to categorical types, and saves the result as a Parquet file.
    """
    path = Path("../datasets/dataset.csv")

    print(f"Chargement de {path.name}")

    temp_dtype = {
        k: (v if v != "category" else "string") for k, v in DATASET_TYPES.items()
    }

    df = pd.read_csv(path, dtype=temp_dtype, parse_dates=DATASET_DATES)

    cat_cols = [k for k, v in DATASET_TYPES.items() if v == "category"]
    if cat_cols:
        df[cat_cols] = df[cat_cols].astype("category")

    output_path = path.with_suffix(".parquet")
    print(f"Export vers {output_path.name}")
    df.to_parquet(output_path, engine="pyarrow")
    print("Terminé")


if __name__ == "__main__":
    export_csv_to_feather()
