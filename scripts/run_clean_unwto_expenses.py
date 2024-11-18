"""
Purpose: Clean the UNWTO tourism expenditure data.
"""

# Dependencies 
import os
import numpy as np
import pandas as pd
import pycountry
    # NOTE: You will need to install pycountry in miniforge 
    # conda activate teem_devstack
    # conda install pycountry

# Label country codes
def get_iso3_code(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        if country:
            return country.alpha_3
        else:
            return None
    except KeyError:
        return None
    
# Function: Clean data set
def fun_clean_expenses(df):
    # Add Variable: ISO-3 Alpha country codes
    df['iso_code'] = get_iso3_code(df['country'])
    # Reshape (pivot table)
    df = pd.melt(df, 
                id_vars = ["c", "c_s", "country", "iso_code"], 
                value_vars = [str(year) for year in range(1995, 2023)],  # Years 1995 to 2022
                var_name = "year", 
                value_name = "expense")
    # Replace exact zero with missing
    df["expense"].replace(0, np.nan, inplace=True)
    # Rescale for million dollar units
    df["expense"] = df["expense"] * 1e6


# Bring in data 
df_unwto_expenses = pd.read_excel("../data/unwto-inbound-tourism-expenditure.xlsx")
    # TODO:  I can't figure out why the directory path is failing here...

# Clean data 
df_unwto_expenses = fun_clean_expenses(df_unwto_expenses)

# Export cleaned data
df_unwto_expenses.to_csv("../data/unwto-expenses-cleaned.csv", index=False)