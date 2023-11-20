import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score 
import statsmodels.api as sm
import numpy as np

class LinearModels:
    """A class for performing linear regression using scikit-learn and statsmodels.

    Args:
        dataframe (pd.DataFrame): The input dataframe containing the data.
        variation (pd.Series): The target variable to predict, usually a column in the dataframe.

    Raises:
        AssertionError: If the input types are not as expected.

    Attributes:
        dataframe (pd.DataFrame): The input dataframe containing the data.
        variation (pd.Series): The target variable to predict.

    Methods:
        scikit_linear_model():
            Fits a linear regression model using scikit-learn on the provided data and prints the R-squared score.

        sm_linear_model():
            Fits an ordinary least squares (OLS) linear regression model using statsmodels on the provided data
            and prints the summary of the regression results.
    """
    def __init__(self, dataframe, variation):
        # Assertions
        assert isinstance(dataframe, pd.DataFrame), "dataframe must be a dataframe"
        assert isinstance(variation, pd.Series), "variation must be columns of dataframe"

        self.dataframe = dataframe

        #replace infinite value to Nan
        dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)

        self.variation = variation

    def scikit_linear_model(self):
        """Fits a linear regression model using scikit-learn on the provided data and prints the R-squared score."""
        # Split train set and test set
        x_train, x_test, y_train, y_test = train_test_split(self.dataframe, self.variation, test_size=0.2)

        # Instance of linear regression model
        LR = LinearRegression()

        # Training
        LR.fit(x_train, y_train)

        # Prediction on test set
        y_prediction = LR.predict(x_test)

        # Regression's reliability
        score = r2_score(y_test, y_prediction)

        print(score)

    def sm_linear_model(self):
        """Fits an ordinary least squares (OLS) linear regression model using statsmodels
        on the provided data and prints the summary of the regression results."""

        # Split train set and test set
        x_train, x_test, y_train, y_test = train_test_split(self.dataframe, self.variation, test_size=0.2)
        X_with_intercept = sm.add_constant(x_train)

        #instance OLS model from statsmodels
        model = sm.OLS(np.asarray(y_train), X_with_intercept)

        #training module
        result = model.fit()

        #print summary
        print(result.summary())
