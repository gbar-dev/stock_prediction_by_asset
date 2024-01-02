import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from data.tools import *

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
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cookie": "GUC=AQAACAFlkbhlvkIjUwUk&s=AQAAAJhnjjV8&g=ZZByqg; A1=d=AQABBK92WmUCELxOFh1yaAizXUx-gPSMHG8FEgAACAG4kWW-ZeWnJm0AAiAAAAcIqnZaZXTJeaUID4_MubCInQjcOL0XndOVZgkBBwoBnQ&S=AQAAAqD3_CR-rqlsdQVi5tt1Fu4; A3=d=AQABBK92WmUCELxOFh1yaAizXUx-gPSMHG8FEgAACAG4kWW-ZeWnJm0AAiAAAAcIqnZaZXTJeaUID4_MubCInQjcOL0XndOVZgkBBwoBnQ&S=AQAAAqD3_CR-rqlsdQVi5tt1Fu4; cmp=t=1703965004&j=1&u=1---&v=103; OTH=v=2&s=2&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiMjJMQTZRTzNSWTVFTUs2…eJp9D1iuf4m.z6dKxD.iM51J41MbWrbltQs56nebL4_PEo-~E; F=d=8IK1kyM9vGVSVBXSsn9r1MHOHF5daxD1xga47a9ZYO.jsFATHHM-; PH=l=fr-FR; Y=v=1&n=360r7k259fedj&l=1acd63p1mop1le4uwhg6clm76evgdsm8t2uxkn22/o&p=n34vvfr00000000&r=1c9&intl=fr; ucs=tr=1704047324000; PRF=t%3DADTX%252BAAPL%252BAGOAF%252BCS.PA; A1S=d=AQABBK92WmUCELxOFh1yaAizXUx-gPSMHG8FEgAACAG4kWW-ZeWnJm0AAiAAAAcIqnZaZXTJeaUID4_MubCInQjcOL0XndOVZgkBBwoBnQ&S=AQAAAqD3_CR-rqlsdQVi5tt1Fu4; EuConsent=CPxNuMAPxNuMAAOACKFRDfCgAAAAAAAAACiQAAAAAABhoAMAARBQEQAYAAiCgKgAwABEFAA",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
        }
        #assertion
        self.header = {key: value.encode('utf-8') if isinstance(value, str) else value for key, value in self.header.items()}

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
        mnemo_link = []
        
        # Loop to scrap abbreviation of stock 
        for page in range(self.nb_page + 1):
            response = requests.get(f"https://fr.finance.yahoo.com/screener/predefined/undervalued_large_caps?count=25&offset={page*25}", headers=self.header)
            print(response.status_code)
            
            soup = bs(response.text, "html.parser")
            for Mnemo in soup.find_all("a", attrs={"data-test": "quoteLink"}):
                mnemo_link.append(Mnemo.text)
            
        return mnemo_link

    def scraper_asset(self, mnemo_link):
        """
        Scraping of assets from stocks

        Args:
            Mnemo_link: list of stocks abbreviation
        return: 
            DataFrame contenant les informations sur les actions and csv with datas
        """
        
        #assertion
        if len(mnemo_link)==0: 
            raise ValueError("list is empty")
        if not isinstance(mnemo_link,list):
            raise TypeError("Must be a list")

        # asset = statistics(self.header,mnemo_link)
        # print(asset)
        # profil = profils(self.header,mnemo_link)
        # print(profil)
        # variations = variation(self.header,mnemo_link)
        # print(variations)
        financials = financial(self.header,mnemo_link)
        print(financials)
        #creation of csv with assets
        # asset.to_csv("src/data/database/bourse.csv")
        # return asset
