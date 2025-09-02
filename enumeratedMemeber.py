from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum): #Inheritence
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message":"Deep Learning Shit1"}
    if model_name is ModelName.lenet:
        return {"model_name": model_name, "message": "Lightweight"}
    if model_name is ModelName.resnet:
        return {"model_name":model_name, "message": "Image classification shit"}

