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
            "Cookie": "GUCS=Ac7FZdam; EuConsent=CP1fSAAP1fSAAAOACKFRAaEgAAAAAAAAACiQAAAAAAAA; GUC=AQAACAFlW8ZljEIjUwUk&s=AQAAACuOqVNt&g=ZVp2-A; A1=d=AQABBK92WmUCELxOFh1yaAizXUx-gPSMHG8FEgAACAHGW2WMZeWnJm0AAiAAAAcIqnZaZXTJeaUID48qV4zpQPA01BM9hVQrPAkBBwoBGQ&S=AQAAAjpUad4JWAwrW5z6967R-7E; A1S=d=AQABBK92WmUCELxOFh1yaAizXUx-gPSMHG8FEgAACAHGW2WMZeWnJm0AAiAAAAcIqnZaZXTJeaUID48qV4zpQPA01BM9hVQrPAkBBwoBGQ&S=AQAAAjpUad4JWAwrW5z6967R-7E; A3=d=AQABBK92WmUCELxOFh1yaAizXUx-gPSMHG8FEgAACAHGW2WMZeWnJm0AAiAAAAcIqnZaZXTJeaUID48qV4zpQPA01BM9hVQrPAkBBwoBGQ&S=AQAAAjpUad4JWAwrW5z6967R-7E; cmp=t=1700427441&j=1&u=1---&v=2; OTH=v=2&s=2&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiMjJMQTZRTzNSWTVFTUs2QkZYR0RRMkNOVlUiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiJRS3hyVTJibk1XYmUifX0.tkO2YtrsXE6euKv061BVXR9O_y9Tyxq4LmT2vM6bYBBgRqSMHz0OS-9r-07YuyBtBb0h--KDI4jk1fnBPnlEkHoOmSxgBiR9qCbps5Fc5hCyVmfiISU3gm5rpzXA7hSJOJP-UTJ1Rm7x3C2g6_8ZjlR-eoI98jIe-Bb7kkKhPEA; T=af=JnRzPTE3MDA0Mjc0OTkmcHM9c3JqZnRqMEZVX292a3VwLmxWT0x2dy0t&d=bnMBeWFob28BZwEyMkxBNlFPM1JZNUVNSzZCRlhHRFEyQ05WVQFhYwFBRExGaXZQVAFhbAFndWlsbDc3YkBnbWFpbC5jb20Bc2MBZGVza3RvcF93ZWIBZnMBQi4uVy5mSmxXbmJyAXp6AXJibldsQkE3RQFhAVFBRQFsYXQBcmJuV2xCAW51ATA-&kt=EAA2kwym38BUL4C68rMWndsiw--~I&ku=FAAVuL1ZJT9mvqyVymBsgOVp6Mu9TNQCRoGc3nyAuem_Czkcg_zqQLlyrvdqZxNlZOUMaKd1_mX55Pc55LtiILB4TQMELcSJQa3F0N7BAoVAnckW1jIZi_nfkCtrKEbSwqMSd.nMfFeco2vP329N6Ev5mLKzZAWHDBmj6thlt_1Xfs-~E; F=d=8IK1kyM9vGVSVBXSsn9r1MHOHF5daxD1xga47a9ZYO.jsFATHHM-; PH=l=fr-FR; Y=v=1&n=360r7k259fedj&l=1acd63p1mop1le4uwhg6clm76evgdsm8t2uxkn22/o&p=n34vvfr00000000&r=1c9&intl=fr",
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
            response = requests.get(f"https://fr.finance.yahoo.com/screener/99b382c3-38c7-4b52-bd34-0c08ec1385af?count=100&offset={page*100}", headers=self.header)
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
        assert len(Mnemo_link)==0, "list is empty"
        assert isinstance(Mnemo_link,list),"Must be a list"
        
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
