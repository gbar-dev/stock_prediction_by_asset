from data.make_dataset import YahooFinanceScraper
from data.clean_dataset import pretraitement
from models.linearmodel import LinearModels
import os
import pandas as pd

def main():
    if not os.path.exists("src/data/database/bourse.csv"):
        scraper = YahooFinanceScraper(0)
        list_action = scraper.scraper_action()
        print(list_action)
        scraper.scraper_asset(list_action)
    else : 
        # assets = pd.read_csv("C:/Users/Guillaume Baroin/Documents/Programs/asset_prediction/data/processed/action.csv")
        action_asset,variation = pretraitement(chemin="src/data/database/bourse.csv")
        model = LinearModels(action_asset,variation)
        scikit_model = model.scikit_linear_model()
        sm_model = model.sm_linear_model()


if __name__ =="__main__":
    main()

