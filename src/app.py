from data.make_dataset import crawler
from data.clean_dataset import pretraitement
from models.linearmodel import linear_model
import os
import pandas as pd

def main():
    if not os.path.exists("data/database/action.csv"):
        scraper = crawler(5)
        list_action = scraper.scraper_action()
        print(list_action)
        scraper.scraper_asset(list_action)
    else : 
        # assets = pd.read_csv("C:/Users/Guillaume Baroin/Documents/Programs/asset_prediction/data/processed/action.csv")
        action_asset,variation = pretraitement(chemin="data/database/action.csv")
        linear_model(action_asset,variation)

if __name__ =="__main__":
    main()
