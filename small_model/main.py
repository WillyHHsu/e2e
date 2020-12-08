from fastapi import FastAPI
from pydantic import BaseModel

from sklearn.ensemble import RandomForestClassifier
import pickle

"""
data_teste= {'sepal_length':4.6
             , 'sepal_width':3
             , 'petal_length':2 
             , 'petal_width':1.2}
"""

pickle.load('small_model/pickle.sav')

class jsonData(Basemodel):
	values: object


app = FastAPI()

@app.get("/")
async def root():
    return {"I am": "alive"}

@app.post("/predict"):
async def predict(predict:values):
	return predict
