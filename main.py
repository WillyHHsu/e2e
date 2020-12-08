#https://towardsdatascience.com/how-to-build-and-deploy-a-machine-learning-model-with-fastapi-64c505213857

from fastapi import FastAPI
from pydantic import BaseModel

from sklearn.ensemble import RandomForestClassifier
import pickle

model=pickle.load(open('small_model/pickle.sav', 'rb'))

class Features(BaseModel):
	sepal_length: float
	sepal_width: float
	petal_length: float
	petal_width: float

	class Config:
		schema_extra = {
			"example": {
				"sepal_length": 1.2
				,"sepal_width": 1.1
				,"petal_length": 2
                ,"petal_width": 2.34
            }}
        

app = FastAPI(
	title='Inspirational Title'
	,description='meaningful description'
	,version='1.0.0'
	)

@app.get("/")
async def root():
    return {"I am": "alive"}

@app.post("/predict", response_model=Features)
async def ans(predict:Features):
	"""
		This function will predict the label
	"""
	pred_label = model.predict([[predict.sepal_length
		,predict.sepal_width
		,predict.petal_length
		,predict.petal_width]])[0]
	
	return {'label':pred_label}


