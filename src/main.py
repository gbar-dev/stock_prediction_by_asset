from data.make_dataset import YahooFinanceScraper
from data.clean_dataset import Preprocessing
from models.linearmodel import LinearModels
import os
import pandas as pd

def main():
    """
    The main function of the program.

    This function checks if a CSV file containing stock market data exists.
    If the file does not exist, it uses the YahooFinanceScraper to fetch
    stock market data, processes the data, and builds linear models using
    scikit-learn and statsmodels. If the file exists, it reads the data from
    the CSV file and performs the same processing and modeling steps.

    The program aims to predict asset variations based on historical data.

    Parameters:
        None

    Returns:
        None
    """
    # if bourse.csv doesn't exist, run crawler
    if not os.path.exists("src/data/database/bourse.csv"):
        #crawler yahoo finance
        scraper = YahooFinanceScraper(0)
        #scrap abbreviation
        list_action = scraper.scraper_action()
        #scrap assets
        action_asset,variation = scraper.scraper_asset(list_action)
        #instance linearmodels
        model = LinearModels(action_asset,variation)
        #linear models
        scikit_model = model.scikit_linear_model()
        sm_model = model.sm_linear_model()
    # else, import csv 
    else: 
        action_asset,variation = Preprocessing(chemin="src/data/database/bourse.csv")
        #instance linearmodels
        model = LinearModels(action_asset,variation)
        #linear models
        scikit_model = model.scikit_linear_model()
        sm_model = model.sm_linear_model()


if __name__ =="__main__":
    main()

