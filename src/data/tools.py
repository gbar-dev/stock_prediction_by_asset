import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from data.clean_dataset import *


def statistics(header,mnemo_list):
    list_asset = []
    for element in mnemo_list:
        #connection to yahoo asset
        response = requests.get(f"https://fr.finance.yahoo.com/quote/{element}/key-statistics?p={element}", headers=header)
        
        #transform to text
        soup = bs(response.text, 'html.parser')
        
        #assets scraping 
        for asset in soup.find("div", class_="Mstart(a) Mend(a)").find_all("td", class_="Fw(500) Ta(end) Pstart(10px) Miw(60px)"):
            list_asset.append(asset.text)
        
    asset = pd.DataFrame([list_asset[i:i + 60] for i in range(0, len(list_asset), 60)])
    asset = clean_asset(asset)
    asset["Abbrev"] = mnemo_list
    return asset

def profils(header,mnemo_list):
    profil_list = []
    for element in mnemo_list:
        profil = requests.get(f'https://fr.finance.yahoo.com/quote/{element}/profile?p={element}',headers=header)
        profil_soup = bs(profil.text, 'html.parser')
        for span in profil_soup.find("p",class_="D(ib) Va(t)").find_all("span",class_= "Fw(600)"):
            profil_list.append(span.text)
    profil_list = [profil_list[i:i + 3] for i in range(0, len(profil_list), 3)]
    profil = pd.DataFrame(profil_list)
    profil["Abbrev"]= mnemo_list
    profil = clean_profil(profil)
    return profil

def variation(header,mnemo_list):
    variation_list = []
    for element in mnemo_list:
        # Connection to yahoo history variation
        growth = requests.get(f"https://fr.finance.yahoo.com/quote/{element}/history?period1=1661695037&period2=1693231037&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true", headers=header)
        growth_soup = bs(growth.text, "html.parser")
        
        cours_list = []
        #variation stock scraping
        for cours in growth_soup.find("tbody").find_all("td", "Py(10px) Pstart(10px)"):
            cours_list.append(cours.text)
            
        # dataframe with stock variation, opening, close, etc...
        df_adj = pd.DataFrame([cours_list[i:i + 6] for i in range(0, len(cours_list), 6)])
        df_adj[4] = df_adj[4].str.replace(",", ".")
        df_adj[4] = df_adj[4].str.replace("\u202f", "").astype(float)
        
        #stock_variation egal to first and last history of stock
        stock_variation = (df_adj[4].iloc[0] - df_adj[4].iloc[-1]) / df_adj[4].iloc[0] * 100
        variation_list.append(stock_variation)
        
    df_variation = pd.DataFrame(variation_list)
    df_variation["Abbrev"] = mnemo_list
    df_variation = clean_var(df_variation)
    return df_variation

def split_list(a_list):
    quarter = len(a_list) // 4
    return a_list[:quarter], a_list[quarter:2*quarter], a_list[2*quarter:3*quarter], a_list[3*quarter:]

def financial(header,mnemo_list):
    financial_list = []
    for element in mnemo_list:
        # Connection to yahoo history variation
        growth = requests.get(f"https://fr.finance.yahoo.com/quote/{element}/financials?p={element}", headers=header)
        growth_soup = bs(growth.text, "html.parser")
        cours_list = []
        quarter_list = []
        #variation stock scraping
        for cours in growth_soup.find_all("div",attrs={"data-test":"fin-col"}):
            cours_list.append(cours.text)
            
        one_on_four, two_on_four, three_on_four, four_on_four = split_list(cours_list)
        quarter_list.append(one_on_four)
        quarter_list.append(two_on_four)
        quarter_list.append(three_on_four)
        quarter_list.append(four_on_four)
        
        financial_list.append(quarter_list)
    df_financial = pd.DataFrame(financial_list)
        
    return df_financial
    