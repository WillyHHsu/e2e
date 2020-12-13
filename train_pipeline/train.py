import pandas as pd
import joblib
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV 
from sklearn.pipeline import Pipeline
import boto3

class retrain():
    def __init__(self, data):
        self.x = data[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
        self.y = data['species']
        #TODO: colocar a conexão com o db para ter os dados
        
    def train(self):
        
        pipeline = Pipeline([
        ('randomforestclassifier', RandomForestClassifier())])

        params = {
                'randomforestclassifier__criterion': ["gini","entropy"]
                ,'randomforestclassifier__max_features':['auto', 'sqrt', 'log2']
                ,'randomforestclassifier__max_depth': [None, 8, 9,10, 20, 30 ] 
                ,'randomforestclassifier__min_samples_leaf': [None,3, 5,10 ]
                ,'randomforestclassifier__n_estimators':[20,60,70,80, 100, 120]
                ,'randomforestclassifier__random_state':[42]}

        grid = GridSearchCV(estimator=pipeline
                            ,param_grid=params
                            ,n_jobs=-1
                            ,scoring='accuracy')
        self.grid=grid.fit(self.x,self.y)
        return 'trained'
    
    def save_params(self, model_name='randomforestclassifier'):
        
        params_dict = self.grid.best_params_
        params_dict['best_score_']= self.grid.best_score_
        params_dict['dtime']= datetime.today().strftime("%d-%m-%Y")
        params_dict['model']= model_name
        
        try:
        # Acho que aqui faz sentido usar um MongoDB da vida para colocaar todos os hiper parâmetros. Dado que há N tipos de schemas para N tipos de modelos
            dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8005",region_name='us-west-2')
            table = dynamodb.Table('params')
            response = table.put_item(
            Item={
                    'model': 'randomforestclassifier'
                    ,'criterion': self.grid.best_params_['randomforestclassifier__criterion'] 
                    ,'max_depth':self.grid.best_params_['randomforestclassifier__max_depth']
                    ,'max_features':self.grid.best_params_['randomforestclassifier__max_features']
                    ,'min_samples_leaf':self.grid.best_params_['randomforestclassifier__min_samples_leaf']
                    ,'n_estimators': self.grid.best_params_['randomforestclassifier__n_estimators']
                    ,'score': str(self.grid.best_score_)
                    ,'dtime': datetime.today().strftime("%d-%m-%Y")
                })
            print('deu certo')
            return 'saved'        
        except Exception as err:
            print(err)
            print('a imagem docker do Dynamo está rodando?')
            return 'not saved'
                
        
    def save_model(self, file_name='train_pipeline/pickle.sav'):
        joblib.dump(self.grid.best_estimator_,file_name)
        return 'model_created'
    
if __name__ == '__main__':

    iris =pd.read_csv("iris.csv", header=None)
    iris.columns=['sepal_length','sepal_width','petal_length','petal_width','species']
    
    train = retrain(iris)
    train.train()
    train.save_params()
    train.save_model()
    
    print('done')