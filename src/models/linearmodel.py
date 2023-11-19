import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score 

def linear_model(dataframe,variation):
    while score < 0.70:
        x_train, x_test, y_train, y_test = train_test_split(dataframe,variation, test_size =0.2)
        LR = LinearRegression()
        LR.fit(x_train,y_train)
        y_prediction = LR.predict(x_test)
        score = r2_score(y_test, y_prediction)
    print(LR)
    print(score)