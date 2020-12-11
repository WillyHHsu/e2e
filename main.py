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
				,"petal_length": 2.0
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

@app.post("/predict/")
async def ans(predict:Features):
	"""
		This function will predict the label
	"""

	pred_label = model.predict([[predict.sepal_length
		,predict.sepal_width
		,predict.petal_length
		,predict.petal_width]])[0]
	
	"""
	# para não precisar baixar a imagem docker e configurar, basicamente precisamos logar as saídas para triggar o retreino 
	
	import boto3
	from datetime import datetime
	import random 
	 
	dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8005",region_name='us-west-2')
	table = dynamodb.Table('logs')
	
	response = table.put_item(
	Item={
			'user_id': random.randint(0,42)
			,'value': pred_label
			,'dtime':datetime.today().strftime("%d-%m-%Y")
		}
		)
	"""

	return {'label':pred_label}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)