from starlette.testclient import TestClient
from main import app
import json   


client = TestClient(app)

def test_main():
    response = client.get('/')
    assert response.status_code == 200 

def test_main_alive():
    response = client.get('/')
    assert response.json() == {"I am": "alive"}

def test_predict():
    response = client.post('/predict/',data = json.dumps({'sepal_length':4.6, 'sepal_width':2, 'petal_length':1 , 'petal_width':1.2}))
    assert response.status_code == 200

def test_predict_setosa():
    response = client.post('/predict/',data = json.dumps({'sepal_length':4.6, 'sepal_width':2, 'petal_length':1 , 'petal_width':1.2}))
    assert response.json() == {"label":"Iris-setosa"}  
