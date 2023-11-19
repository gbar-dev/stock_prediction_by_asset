import pandas as pd
from sklearn.impute import SimpleImputer

def convert_and_multiply(value):
    if value is None:
        return None
    elif 'T' in value:
        return float(value.replace('T', '')) * 1e12
    elif 'B' in value:
        return float(value.replace('B', '')) * 1e9
    elif 'M' in value:
        return float(value.replace('M', '')) * 1e6
    elif "k" in value:
        return float(value.replace('k', '')) * 1e3
    elif "%" in value:
        return float(value.replace('%', '')) 
    
    else:
        return float(value)
def pretraitement(chemin):
    df_asset = pd.read_csv(chemin)
    df_asset =df_asset.drop("Unnamed: 0", axis = 1)
    colonne_action = ["Cap. boursière (intrajournalière)","Valeur de entreprise","P/E précédent","P/E à terme","Rapport PEG (prévu sur 5 ans)","Cours/Ventes (ttm)","Cours/Registre comptable (dern. trim.)","Valeur entreprise/CA","Valeur de entreprise/EBITDA","Bêta (mensuel sur 5 ans)",
                    "Variation sur 52 semaines 3","Variation S&P500 sur 52 semaines 3","Plus haut annuel 3","Plus bas annuel 3","Moyenne mobile sur 50 jours 3","Moyenne mobile sur 200 jours","Vol. moy. (3 mois) 3","Vol. moy. (10 jours)","Actions en attente","Actions implicites en circulation","Flottant","pct détenu par des initiés","pct détenu par des institutions",
                    "Actions vendues à découvert au (14 août 2023)","Ratio VAD au (14 août 2023)","pct des paiements en cours encaissement au (14 août 2023)","pct actions en circulation VAD au (14 août 2023)","Actions vendues à découvert (avant le 13 juil. 2023)","Taux de dividende annuel à terme","Rendement en dividende annuel à terme","Taux de dividende annuel précédent","Rendement du dividende annuel précédent",
                    "Rendement en dividendes moyen sur 5 ans","Rapport de distribution","Date du dividende ","Date ex-dividende","Dernier facteur de fractionnement","Dernière date de division","Fin exercice financier","Dernier trimestre (dern. trim.)","Marge bénéficiaire","Marge exploitation (ttm)",
                    "Rendement des actifs (ttm)","Rendement des capitaux propres (ttm)","Recettes (ttm)","Revenu par action (ttm)	","Croissance trimestrielle du CA (Sur 12 mois)	","Bénéfice brut (ttm)","EBITDA	","Bénéfice net disponible distribuable (ttm)","BPA dilué (ttm)","Croissance trimestrielle des bénéfices (Sur 12 mois)","Trésorerie totale (dern. trim.)","Total espèces par action (dern. trim.)","Dette totale (dern. trim.)","Dette/Actif total (dern. trim.)","Coefficient de liquidité (dern. trim.)",
                    "Valeur comptable par action (dern. trim.)","Flux de trésorerie exploitation (ttm)","Effet de levier de flux de trésorerie libre (ttm)","variation"]

    df_asset.columns = colonne_action
    df_asset= df_asset.drop(["Date du dividende ","Date ex-dividende","Dernière date de division","Dernier facteur de fractionnement","Fin exercice financier","Dernier trimestre (dern. trim.)"],axis=1)
    df_asset = df_asset.replace("S.O.",None)
    df_asset["variation"] =df_asset["variation"].round(2).astype(str)
    df_asset = df_asset.replace(",",".",regex=True)
    df_asset = df_asset.replace("\xa0","",regex=True)
    df_asset = df_asset.applymap(convert_and_multiply)

    variation = df_asset["variation"]
    df_asset = df_asset.drop(["variation"],axis = 1)

    imputer = SimpleImputer(strategy='most_frequent')
    action_transformed = imputer.fit_transform(df_asset)
    action_finance = pd.DataFrame(action_transformed)
    action_finance["variation"] = variation
    return action_finance,variation


