import pandas as pd
import joblib
import json
from utils.ml_utils import (
    clean_text,
    combine_text_columns,
    uniform_sample,
    get_pipeline,
)
from utils.constants import CATEGORY_COLUMNS

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def train_and_export():
    print("Lecture du dataset...")
    data = pd.read_parquet("../datasets/dataset.parquet")
    print("Dataset chargé !\n")
    # Sample
    print("Début échantillonage...")
    data_sampled = uniform_sample(data)
    print("Echantillonage terminé !\n")

    # Clean
    print("Nettoyage de la data...")
    data_sampled["text_raw"] = combine_text_columns(data_sampled)
    data_sampled["text_clean"] = clean_text(data_sampled["text_raw"])
    print("Datas nettoyées !\n")

    # Split
    print("Préparation de la data...")
    X = data_sampled.drop(["Tag", "Complaint ID", "text_raw"], axis=1)
    y = data_sampled["Tag"]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=1357, stratify=y_encoded
    )
    print("Datas prêtes !\n")

    # Pipeline
    model_pipeline = get_pipeline(CATEGORY_COLUMNS)

    # Train
    print("Entrainement du modèle...")
    model_pipeline.fit(X_train, y_train)
    print("Modèle entrainé !\n")

    # Export model
    print("Export du modèle...")
    joblib.dump(model_pipeline, "model.pkl")
    joblib.dump(le, "label_encoder.pkl")
    print("Modèle exporté !\n")

    # Metrics
    print("Export des metrics...")
    y_pred = model_pipeline.predict(X_test)
    score = classification_report(
        y_test, y_pred, target_names=le.classes_, output_dict=True
    )
    with open("metrics.json", "w") as file:
        json.dump(score, file, indent=4)
    print("Metrics exportées !\n")


if __name__ == "__main__":
    train_and_export()
