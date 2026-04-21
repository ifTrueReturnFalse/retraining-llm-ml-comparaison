# /// script
# dependencies = [
#   "pandas",
#   "pyarrow",  # <--- C'est lui qui manquait !
# ]
# ///

import pandas as pd
import sys
from pathlib import Path


def export_csv_to_feather(csv_path: str, typed_dict=None, dates_columns=None):
    if typed_dict is None:
        typed_dict = {}
    if dates_columns is None:
        dates_columns = {}

    path = Path(csv_path)
    output_path = path.with_suffix(".feather")

    print(f"Chargement de {path.name}")

    temp_dtype = {
        k: (v if v != "category" else "string") for k, v in typed_dict.items()
    }

    df = pd.read_csv(path, dtype=temp_dtype, parse_dates=dates_columns)

    cat_cols = [k for k, v in typed_dict.items() if v == "category"]
    if cat_cols:
        df[cat_cols] = df[cat_cols].astype("category")

    print(f"Export vers {output_path.name}")
    df.to_feather(output_path)
    print("Terminé")


if __name__ == "__main__":
    THIS_DATASET_TYPES = {
        "Tag": "category",
        "Consumer Claim": "string",
        "Company public response": "category",
        "Company": "string",
        "State": "string",
        "ZIP code": "string",
        "Tags": "category",
        "Consumer consent provided?": "category",
        "Submitted via": "category",
        "Company response to consumer": "category",
        "Timely response?": "category",
        "Consumer disputed?": "category",
        "Complaint ID": "int64",
    }

    THIS_DATASET_DATES = ["Date received", "Date sent to company"]

    export_csv_to_feather("../datasets/dataset.csv", THIS_DATASET_TYPES, THIS_DATASET_DATES)
