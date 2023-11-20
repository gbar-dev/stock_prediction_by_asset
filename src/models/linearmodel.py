import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score 
import statsmodels.api as sm
import numpy as np

class LinearModels:
    def __init__(self,dataframe,variation):
        #assertions
        assert isinstance(dataframe,pd.DataFrame), "dataframe must be a dataframe"
        assert isinstance(variation,pd.Series),"variation must be columns of dataframe"
        
        self.dataframe = dataframe
        dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
        self.variation = variation
        
        
    def scikit_linear_model(self):
        
        #split train set and test set
        x_train, x_test, y_train, y_test = train_test_split(self.dataframe,self.variation, test_size =0.2)
        
        #instance of linear regression model
        LR = LinearRegression()
        
        #training
        LR.fit(x_train,y_train)
        
        # prediction on test set
        y_prediction = LR.predict(x_test)
        
        #regression's fiability
        score = r2_score(y_test, y_prediction)
        
        print(score)
        
    def sm_linear_model(self):
        
        x_train, x_test, y_train, y_test = train_test_split(self.dataframe,self.variation, test_size =0.2)
        X_with_intercept = sm.add_constant(x_train)
        
        model = sm.OLS(np.asarray(y_train),X_with_intercept)
        
        result = model.fit()
        
        print(result.summary())