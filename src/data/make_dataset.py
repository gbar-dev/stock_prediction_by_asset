import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

class YahooFinanceScraper:
    """
    This class instance the scraper to scrap assets and statistics of stocks

    Args:
        header: header for the website, {accept,accept-encoding,accept-language,etc...}
        nb_page: number of page to scrap, start to 0 for the first page

    Returns:
        pd.DataFrame : dataframe with assets of stock

    Assertition:
        TypeError: nb_page must be integer.
    """

    def __init__(self, nb_page):
        # Header must for the website
        self.header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cookie": "F=d=9Yw7Xxc9vNbwF.JX.5S0M8f9Jo1mmK20Y9zZ1fskR1NLNQKFi8He0evq1O8toBylqV8-; PH=l=fr-FR; Y=v=1&n=01q31l92lte96&l=avtdodtl8664bpcl9lxo6fb4fhn0l7hlsns5k4ih/o&p=n34vvfr00000000&r=1bt&intl=fr; GUC=AQAACAFlW5ZljkIgxAS5&s=AQAAAHYlc1O7&g=ZVpSwQ; A1=d=AQABBP25OmQCEM1fKs_f0F5IGor0oJd7eQoFEgAACAGWW2WOZeWjJm0AAiAAAAcI-7k6ZKAwxK8ID6aTWTK88apXGucEEhYT5QkBBwoBKQ&S=AQAAAlxmCpqwT1RQ_PN78ljs15M; A3=d=AQABBP25OmQCEM1fKs_f0F5IGor0oJd7eQoFEgAACAGWW2WOZeWjJm0AAiAAAAcI-7k6ZKAwxK8ID6aTWTK88apXGucEEhYT5QkBBwoBKQ&S=AQAAAlxmCpqwT1RQ_PN78ljs15M; ucs=tr=1703864398000; A1S=d=AQABBP25OmQCEM1fKs_f0F5IGor0oJd7eQoFEgAACAGWW2WOZeWjJm0AAiAAAAcI-7k6ZKAwxK8ID6aTWTK88apXGucEEhYT5QkBBwoBKQ&S=AQAAAlxmCpqwT1RQ_PN78ljs15M; OTH=v=2&s=2&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiU1FMVUI1TldFRFlRWllQWUk1R0paM0VBMzQiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiJQdVRzY3JreG45dHAifX0.aL3DqLsyGe2FGFI52l-sXeu7oiqbh23iMK8oqUynoSnv0Os9FqkMypPuWYAFXgIsv9KpTfHFSrBiT81MvQCpJPb7aaTWdDuTfekJU02Fcv2o6fi67-TkGPxiNdZLUhmFIjSPTiaNI9g_UcHgG7e1F8OJx818l-LnVvw-NsxlZJI; T=af=JnRzPTE3MDM3Nzc5OTgmcHM9YTZ3Rzd5RVl3ZUJZcERGcVNNV04uQS0t&d=bnMBeWFob28BZwFTUUxVQjVOV0VEWVFaWVBZSTVHSlozRUEzNAFhYwFBSklRa2l3NwFhbAFiYXJvaW4uZ3VpbGxhdW1lLnByb0BnbWFpbC5jb20Bc2MBZGVza3RvcF93ZWIBZnMBQjc5c0Y3cGtmeGJxAXp6AU9iWmpsQkE3RQFhAVFBRQFsYXQBeUtsV2xCAW51ATA-&kt=EAAOc8Oj8ssInHdj6kEY.TmuA--~I&ku=FAAtB6YVwbcKuzFd1pihJEOemxG1OXKSmVhpi1p0CeaXeYxpGPfCzVQ0U1gEDScW_ht1QUuH_ccmurjwiB24EDw.0dL_wyz_hoeSzQEq9YaSe_mBZqYbcNV1.E7SYJ79LNO79.hSOcS9TElGRIKxiHB99HYKN1aecOKkFZQYGll5AQ-~E; cmp=t=1703778001&j=1&u=1---&v=103; EuConsent=CPs8KYAPs8KYAAOACKFRDfCgAAAAAAAAACiQAAAAAABhoAMAARBQEQAYAAiCgKgAwABEFAA; PRF=t%3DMDT%252BCICHY%252BWFC-PL%252BNVDA%252BATE.PA%252BCOV.PA%252BFR.PA%252BSCR.PA%252BALO.PA%252BFDJ.PA%252BGFC.PA%252BWLN.PA%252BRE.PA%252BTEP.PA%252BNOKIA.PA%26newChartbetateaser%3D1",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54"
        }
        #assertion
        assert isinstance(nb_page,int),"nb_page must be an integer"
        
        # number of page to scrap
        self.nb_page = nb_page

    def scraper_action(self):
        """
        Scrap abrevation of action 
        
        Returns:
            list of mnemo
        """
        # instanciation of list
        Mnemo_link = []

        # Loop to scrap abbreviation of stock 
        for page in range(self.nb_page + 1):
            response = requests.get(f"https://fr.finance.yahoo.com/screener/1afec95a-fe45-4ba2-bee3-5ef40bdf1322?count=100&offset={page*100}", headers=self.header)
            assert isinstance(response,requests.Response)
            
            soup = bs(response.text, "html.parser")
            for Mnemo in soup.find_all("a", attrs={"data-test": "quoteLink"}):
                Mnemo_link.append(Mnemo.text)
            
        return Mnemo_link

    def scraper_asset(self, Mnemo_link):
        """
        Scraping of assets from stocks

        Args:
            Mnemo_link: list of stocks abbreviation
        return: 
            DataFrame contenant les informations sur les actions and csv with datas
        """
        
        #assertion
        if len(Mnemo_link)==0: 
            raise ValueError("list is empty")
        if not isinstance(Mnemo_link,list):
            raise TypeError("Must be a list")
        
        # Instanciation des listes
        list_asset = []
        variation_list = []

        # initialize i to 0 
        i = 0

        # Loop to scrap assets
        for element in Mnemo_link:
            
            i += 1
            print(i)
            
            #connection to yahoo asset
            response = requests.get(f"https://fr.finance.yahoo.com/quote/{element}/key-statistics?p={element}", headers=self.header)
            
            #transform to text
            soup = bs(response.text, 'html.parser')
            
            #assets scraping 
            for asset in soup.find("div", class_="Mstart(a) Mend(a)").find_all("td", class_="Fw(500) Ta(end) Pstart(10px) Miw(60px)"):
                list_asset.append(asset.text)

            #connection to yahoo history variation
            growth = requests.get(f"https://fr.finance.yahoo.com/quote/{element}/history?period1=1661695037&period2=1693231037&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true", headers=self.header)
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

            #dataframe of all assets
            asset = pd.DataFrame([list_asset[i:i + 60] for i in range(0, len(list_asset), 60)])
            
            #ajout of variation with assets
            asset["variation"] = variation_list
            
        #creation of csv with assets
        asset.to_csv("src/data/database/bourse.csv")
        return asset
