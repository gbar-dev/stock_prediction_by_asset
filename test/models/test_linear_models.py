import unittest
import pandas as pd
import numpy as np
import sys
sys.path.append(".")
from src.models.linearmodel import *  

class TestLinearModels(unittest.TestCase):
    def setUp(self):
        # Create a sample dataframe for testing
        data = {'feature1': [1, 2, 3, 4, 5],
                'feature2': [5, 4, 3, 2, 1],
                'target': [10, 20, 30, 40, 50]}
        self.df = pd.DataFrame(data)
        self.variation = self.df['target']

    def test_initialization(self):
        # Test if the LinearModels class initializes correctly
        model = LinearModels(self.df, self.variation)
        self.assertIsInstance(model, LinearModels)

    def test_scikit_linear_model(self):
        # Test the scikit-learn linear regression model fitting
        model = LinearModels(self.df, self.variation)
        model.scikit_linear_model()  # This will print the R-squared score

    def test_sm_linear_model(self):
        # Test the statsmodels linear regression model fitting
        model = LinearModels(self.df, self.variation)
        model.sm_linear_model()  # This will print the summary of the regression results

if __name__ == '__main__':
    unittest.main()
