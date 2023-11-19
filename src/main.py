from data.make_dataset import YahooFinanceScraper
from data.clean_dataset import pretraitement
from models.linearmodel import linear_model
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
        print(action_asset)
        linear_model(action_asset,variation)

if __name__ =="__main__":
    main()

