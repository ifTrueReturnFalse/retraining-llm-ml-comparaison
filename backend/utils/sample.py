import pandas as pd
from utils.ml_utils import uniform_sample

if __name__ == "__main__":
    # Get data
    print("Chargement du dataframe")
    data = pd.read_parquet("../datasets/dataset.parquet")
    print("Chargement terminé\n")

    # Sample data
    print("Echantillonage du dataframe")
    sample = uniform_sample(data)
    print("Echantillonage terminé\n")

    # Output
    print("Export des échantillons")
    sample.to_parquet("../datasets/sample.parquet", engine="pyarrow")
    print("Fin de l'opération\n")
