"""
Purpose: Clean the UNWTO tourism expenditure data.
"""

# Dependencies 
import numpy as np
import pandas as pd
import country_converter as cc
    # NOTE: You will need to install country_converter in miniforge 
    # conda activate teem_devstack
    # conda install pycountry
    
# Function: Clean data set
def fun_clean_expenses(df):

    # Add Variable: ISO-3 Alpha country codes
    df['iso3'] = cc.convert(df['country'],to='ISO3') 

    # Ensure that columns representing years are integers
    year_cols = [col for col in df.columns if isinstance(col, int) and 1995 <= col <= 2022]
    
    # Reshape (pivot table)
    df_long = pd.melt(
        df,
        id_vars=["c", "c_s", "country", "iso3"],
        value_vars=year_cols,
        var_name="year",
        value_name="expense"
    )
    
    # Replace exact zeros with missing values
    df_long["expense"].replace(0, np.nan, inplace=True)
    
    # Rescale for million dollar units
    df_long["expense"] = df_long["expense"].astype(float) * 1e6
    
    return df_long

# Bring in data 
df_unwto_expenses = pd.read_excel("../data/unwto-inbound-tourism-expenditure.xlsx")

# Clean data 
df_unwto_expenses = fun_clean_expenses(df_unwto_expenses)

# Export cleaned data
df_unwto_expenses.to_csv("../data/unwto-expenses-cleaned.csv", index=False)