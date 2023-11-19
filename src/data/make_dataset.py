import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

class crawler:
    """
    Permet de scraper les données de yahoo finance  
    """
    def __init__(self,nb_page):
        # header necéssaire à la requête du site
        self.header =  {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "Accept-Encoding":"gzip, deflate, br",
                        "Accept-Language":"fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                        "Cookie":"F=d=9Yw7Xxc9vNbwF.JX.5S0M8f9Jo1mmK20Y9zZ1fskR1NLNQKFi8He0evq1O8toBylqV8-; PH=l=fr-FR; Y=v=1&n=01q31l92lte96&l=avtdodtl8664bpcl9lxo6fb4fhn0l7hlsns5k4ih/o&p=n34vvfr00000000&r=1bt&intl=fr; PRF=t%3DGLE.PA%252BORA.PA%252BBNP.PA%252BSTMPA.PA%252BENGI.PA%252BSGO.PA%252BPUB.PA%252BAMUN.PA%252BFGR.PA%252BHEIA.AS%252B005930.KS%252BMU%252BMC.PA%252BRMS.PA%252BKER.PA%26newChartbetateaser%3D1; thamba=1; ucs=tr=1700504510000; cmp=t=1700418112&j=1&u=1---&v=103; EuConsent=CPs8KYAPs8KYAAOACKFRDfCgAAAAAAAAACiQAAAAAABhoAMAARBQEQAYAAiCgKgAwABEFAA; GUCS=AV7Cvybh; OTH=v=2&s=2&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiU1FMVUI1TldFRFlRWllQWUk1R0paM0VBMzQiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiJZNFFqNU02enJSS0oifX0.Oz3AgzwnFNCl_PFlGFrl7-vnXPw-c7TMgaSynyJpu8Hf7gXN8wE2VLSRonL-KyEtkFmWNDdcokSGXDG8u2wWlYRAEkmYL0GfFQmidKo5pdmazV6i8VjPsoAIaGxUjJWeQF7c0tv4KNA2ZAKDPaYbuHbQHBhqYHSPGpPw5uIDsxw; T=af=JnRzPTE3MDA0MTgyMjYmcHM9b3ZwLjZVM2xHRmRzaUE1Wlpiejd5dy0t&d=bnMBeWFob28BZwFTUUxVQjVOV0VEWVFaWVBZSTVHSlozRUEzNAFhYwFBQURWTzA3NgFhbAFiYXJvaW4uZ3VpbGxhdW1lLnByb0BnbWFpbC5jb20Bc2MBbWJyX2xvZ2luAWZzAUI3OXNGN3BrZnhicQF6egF5S2xXbEJBN0UBYQFRQUUBbGF0AXlLbFdsQgFudQEw&kt=EAAOXJdBh1dkze3t06.OVO22A--~I&ku=FAASQH6decOEFwlJjTprZP10SO77umykbEZsiJjJgf18SQvz4HoprSHNd2Iq4NKqwsozd.wGDtopTdbdbxeUkDixxuc6byOiRbnsi7xSbYDiQOPl1YDNERd5hJ3U05e1bZDr3hdopJGHndr_xOyaaa0fnLkBf9hkCCkipo6c4IE3iY-~E; GUC=AQAACAFlW5ZljkIgxAS5&s=AQAAAHYlc1O7&g=ZVpSwQ; A1=d=AQABBP25OmQCEM1fKs_f0F5IGor0oJd7eQoFEgAACAGWW2WOZeWjJm0AAiAAAAcI-7k6ZKAwxK8ID6aTWTK88apXGucEEhYT5QkBBwoBKQ&S=AQAAAlxmCpqwT1RQ_PN78ljs15M; A3=d=AQABBP25OmQCEM1fKs_f0F5IGor0oJd7eQoFEgAACAGWW2WOZeWjJm0AAiAAAAcI-7k6ZKAwxK8ID6aTWTK88apXGucEEhYT5QkBBwoBKQ&S=AQAAAlxmCpqwT1RQ_PN78ljs15M; A1S=d=AQABBP25OmQCEM1fKs_f0F5IGor0oJd7eQoFEgAACAGWW2WOZeWjJm0AAiAAAAcI-7k6ZKAwxK8ID6aTWTK88apXGucEEhYT5QkBBwoBKQ&S=AQAAAlxmCpqwT1RQ_PN78ljs15M",
                        "Sec-Fetch-User":"?1",
                        "Upgrade-Insecure-Requests":"1",
                        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54"}
        
        # nombre de page à scrapper
        self.nb_page = nb_page

    def scraper_action(self):
        """
        scraping des liens des actions
        """
        #instance d'une liste
        Mnemo_link= []
        #Loop scrap link of stocks yahoo page
        for page in range(self.nb_page+1):
            response = requests.get(f"https://fr.finance.yahoo.com/screener/5eb1d8e8-a115-426f-9ae9-6ffc793a322a?count=100&offset={page*100}",headers = self.header)
            print(response.status_code)
            soup = bs(response.text,"html.parser")
            for Mnemo in soup.find_all("a",attrs={"data-test":"quoteLink"}):
                Mnemo_link.append(Mnemo.text)
        return Mnemo_link
    
    def scraper_asset(self,Mnemo_link):
        """scraping des assets des actions des 5 pages"""
        #instanciation des listes
        list_asset = []
        variation_list = []

        #start a count value
        i= 0

        #loop which took statistics of stocks 
        for element in Mnemo_link:
            response = requests.get(f"https://fr.finance.yahoo.com/quote/{element}/key-statistics?p={element}",headers = self.header)
            print(i)
            i+=1
            soup = bs(response.text,'html.parser')
            for asset in soup.find("div",class_="Mstart(a) Mend(a)").find_all("td",class_="Fw(500) Ta(end) Pstart(10px) Miw(60px)"):
                list_asset.append(asset.text)

            growth = requests.get(f"https://fr.finance.yahoo.com/quote/{element}/history?period1=1661695037&period2=1693231037&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true",headers=self.header)
            growth_soup = bs(growth.text,"html.parser")
            cours_list = []
            for cours in growth_soup.find("tbody").find_all("td","Py(10px) Pstart(10px)"):
                cours_list.append(cours.text)
            df_adj =pd.DataFrame([cours_list[i:i+6] for i in range(0, len(cours_list), 6)])
            df_adj[4]= df_adj[4].str.replace(",",".")
            df_adj[4]= df_adj[4].str.replace("\u202f","").astype(float)
            list = df_adj[4].to_list()
            
            stock_variation = (df_adj[4].iloc[0] - df_adj[4].iloc[-1]) / df_adj[4].iloc[0] * 100

            variation_list.append(stock_variation)

            asset =pd.DataFrame([list_asset[i:i+60] for i in range(0, len(list_asset), 60)])

            asset["variation"]=variation_list
            print(asset)
        asset.to_csv("../database/bourse.csv")
