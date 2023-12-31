import pickle
import pandas as pd
import uvicorn

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


app = FastAPI()

# Model
MODEL_PATH = "model/rf.pkl"
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Columnas
COLUMNS_PATH = "pickle_files/categories_ohe.pkl"
with open(COLUMNS_PATH, 'rb') as handle:
    ohe_tr = pickle.load(handle)


class Answer(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float


@app.get("/")
async def root():
    return {"message": "Proyecto Potabilidad Agua"}


@app.post("/prediccion")
def predict_water_potability(answer: Answer):
    answer_dict = jsonable_encoder(answer)
    for key, value in answer_dict.items():
        answer_dict[key] = [value]

    single_instance = pd.DataFrame.from_dict(answer_dict)

    # Reformat columns
    single_instance_ohe = pd.get_dummies(single_instance)
    single_instance_ohe = single_instance_ohe.reindex(columns=ohe_tr).fillna(0)

    prediction = model.predict(single_instance_ohe)
    # Cast numpy.int64 to just a int
    score = int(prediction[0])

    response = {"score": score}

    return response





