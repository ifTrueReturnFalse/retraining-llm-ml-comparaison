from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import joblib
from pathlib import Path
from utils.constants import CATEGORY_COLUMNS
import pandas as pd


class ClaimRequest(BaseModel):
    """
    Data model for a claim prediction request.

    Attributes:
        user_claim (str): The text content of the claim to be classified.
    """

    user_claim: str


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model.pkl"

ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to handle the startup and shutdown events of the FastAPI application.
    Loads the machine learning model into memory on startup and clears it on shutdown.
    """
    try:
        ml_models["classifier"] = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        print(f"Erreur: Fichier introuvable au chemin {MODEL_PATH}")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle: {e}")
    yield
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.post("/tag")
async def predict_tag(request: ClaimRequest):
    """
    Predicts the tag/category of a given user claim using the loaded ML model.

    Args:
        request (ClaimRequest): The request body containing the user claim.

    Returns:
        dict: A dictionary containing the original claim and the model's prediction.
    """
    if "classifier" not in ml_models:
        raise HTTPException(status_code=503, detail="Modèle non chargé")

    try:
        input_data = {"text_clean": [request.user_claim]}

        for col in CATEGORY_COLUMNS:
            input_data[col] = ["unknown"]

        df_input = pd.DataFrame(input_data)
        prediction = ml_models["classifier"].predict(df_input)

        return {"prediction": str(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur ML: {str(e)}")
