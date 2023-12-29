import pandas as pd
from sklearn.impute import SimpleImputer
import os

def convert_and_multiply(value):
    """
    Converts a string representation of a numerical value with a suffix
    (e.g., 'T' for trillion, 'B' for billion, 'M' for million, 'k' for thousand, or '%' for percentage)
    into its numerical equivalent and multiplies it by the corresponding factor.

    Args:
        value (str): A string representing a numerical value with an optional suffix.

    Returns:
        float or None: The numerical value multiplied by the appropriate factor.
                       Returns None if the input value is None.

    Examples:
        >>> convert_and_multiply('3.5M')
        3500000.0

        >>> convert_and_multiply('2.2B')
        2200000000.0

        >>> convert_and_multiply('500k')
        500000.0

        >>> convert_and_multiply('75%')
        0.75

        >>> convert_and_multiply(None)
        None
    """
    try:
        if value is None:
            # Return None if the input value is None
            return None
        elif 'T' in value:
            # Convert trillion and multiply by 1e12
            return float(value.replace('T', '')) * 1e12
        elif 'B' in value:
            # Convert billion and multiply by 1e9
            return float(value.replace('B', '')) * 1e9
        elif 'M' in value:
            # Convert million and multiply by 1e6
            return float(value.replace('M', '')) * 1e6
        elif 'k' in value:
            # Convert thousand and multiply by 1e3
            return float(value.replace('k', '')) * 1e3
        elif '%' in value:
            # Convert percentage
            return float(value.replace('%', ''))
        else:
            # Convert plain numerical value
            return float(value)
    except:
        print("nothing to modify")
        pass

def Preprocessing(chemin):
    """
    Preprocesses financial data from a CSV file.

    Args:
        chemin (str): The path to the CSV file containing financial data.

    Returns:
        tuple: A tuple containing two DataFrames - the preprocessed financial data and the 'variation' column.

    Examples:
        >>> data_path = "financial_data.csv"
        >>> preprocessed_data, variation_column = pretraitement(data_path)

    """
    assert os.path.exists(chemin), f"Le chemin {chemin} n'existe pas"
    # Read the CSV file into a DataFrame
    df_asset = pd.read_csv(chemin)

    # Drop the 'Unnamed: 0' column if it exists
    if 'Unnamed: 0' in df_asset.columns:
        df_asset = df_asset.drop("Unnamed: 0", axis=1)

    # Define the columns related to financial actions
    colonne_action = ["Cap", "Value", "P/E_N-1", "P/E", "PEG_5", "Stock/Sell", "Stock/Compta",
    "Value/CA", "Value/EBITDA", "Beta_m_5", "Var_52", "Var_S&P", "High", "Low",
    "MA_50", "MA_200", "Vol_Mean_3mo", "Vol_Mean_10d",
    "Pending", "Act_in_circ", "Flottant", "Pct_initiés",
    "Pct_institutions", "Short_14Aug23",
    "Ratio_VAD_14Aug23", "Pct_paiements_14Aug23",
    "Pct_act_circ_VAD_14Aug23", "Short_before_13Jul23",
    "Div_yield_term", "Div_yield_ann_term", "Div_yield_prev", "Div_yield_ann_prev",
    "Div_yield_avg_5yr", "Dist_ratio", "Date_div", "Date_ex_div", "Split_factor",
    "Last_split_date", "Fiscal_year_end", "Last_quarter",
    "Profit_margin", "Operating_margin_TTM", "ROA_TTM", "ROE_TTM",
    "Revenue_TTM", "EPS_TTM", "Qtrly_rev_growth_12mo",
    "Gross_profit_TTM", "EBITDA", "Net_profit_avail_TTM",
    "Diluted_EPS_TTM", "Qtrly_earnings_growth_12mo",
    "Total_cash_last_qtr", "Cash_per_share_last_qtr",
    "Total_debt_last_qtr", "Debt_to_total_assets_last_qtr",
    "Liquidity_ratio_last_qtr", "Book_value_per_share_last_qtr",
    "Operating_cash_flow_TTM", "Leverage_FCF_TTM", "variation"]

    # Rename columns with predefined financial action names
    df_asset.columns = colonne_action
    # Drop unnecessary columns
    columns_to_drop = ["Date_div", "Date_ex_div", "Last_split_date", "Split_factor",
                       "Fiscal_year_end", "Last_quarter"]
    df_asset = df_asset.drop(columns=columns_to_drop, axis=1)

    # Replace 'S.O.' with None
    df_asset = df_asset.replace("S.O.", None)

    # Round and convert 'variation' column to string
    df_asset["variation"] = df_asset["variation"].round(2).astype(str)

    # Replace commas with dots and remove non-breaking spaces
    df_asset = df_asset.replace(",", ".", regex=True)
    df_asset = df_asset.replace("\xa0", "", regex=True)

    # Apply the convert_and_multiply function to the entire DataFrame
    df_asset = df_asset.applymap(convert_and_multiply)

    # Extract the 'variation' column and drop it from the main DataFrame
    variation = df_asset["variation"]
    df_asset = df_asset.drop(["variation"], axis=1)

    # Impute missing values using the most frequent strategy
    imputer = SimpleImputer(strategy='most_frequent')
    action_transformed = imputer.fit_transform(df_asset)

    # Create a new DataFrame with the imputed data
    action_finance = pd.DataFrame(action_transformed)

    # Add back the 'variation' column to the preprocessed DataFrame
    action_finance["variation"] = variation
    
    columns = [x for x in colonne_action if x not in columns_to_drop]
    
    action_finance.columns = columns
    action_finance.dropna(axis=1,inplace=True)
    action_finance.to_csv("src/data/database/bourse.csv")
    # Return the preprocessed data and the 'variation' column
    return action_finance, variation

