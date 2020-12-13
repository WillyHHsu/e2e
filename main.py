from fastapi import FastAPI
from pydantic import BaseModel


import boto3
from  datetime import datetime
import random

from sklearn.ensemble import RandomForestClassifier
import joblib


model = joblib.load('train_pipeline/pickle.sav')


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




tags_metadata = [
    {
        "name": "default"
        ,"description": "just the hello world"
    },
	{
		"name":"predict"
	}
]

app = FastAPI(
	title='Inspirational Title'
	,description='meaningful description'
	,version='1.0.0'
	,openapi_tags=tags_metadata
	)

@app.get("/")
async def root():
    return {"I am": "alive"}

@app.post("/predict/", tags=['predict'])
async def ans(predict:Features):
	"""
		This function will predict the label
	"""

	pred_label = model.predict([[predict.sepal_length
		,predict.sepal_width
		,predict.petal_length
		,predict.petal_width]])[0]
	
	try:
	# para não precisar baixar a imagem docker e configurar, comentei essa parte do código 
	# O racional do pporquê disso é: basicamente precisamos logar as saídas para triggar o retreino 
	
	 
		dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8005",region_name='us-west-2')
		table = dynamodb.Table('logs')
	
		response = table.put_item(
		Item={
			'user_id': random.randint(0,42)
			,'value': pred_label
			,'dtime':datetime.today().strftime("%d-%m-%Y")
			}
		)

	except Exception as err:
		print(err)
		print('coloquei um docker para rodar dynamo localmente, ele está rodando?:')

	return {'label':pred_label}
