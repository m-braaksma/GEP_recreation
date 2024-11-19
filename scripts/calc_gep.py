"""
Purpose: 
"""

# Dependencies 
import numpy as np
import pandas as pd

# Define Data Paths
unwto_path = '../intermediate/unwto-expenses-cleaned.csv'
prob_nature_path = '../intermediate/ee_r264_prob_nature_tourism.csv'
wb_gdp_path = '../intermediate/gep_tourism.csv'

# Import Data
unwto_exp = pd.read_csv(unwto_path)
unwto_exp.drop(columns='country', inplace=True)
prob_nature = pd.read_csv(prob_nature_path)
prob_nature.rename(columns={'ee_r264_label': 'iso3'}, inplace=True)
wb_gdp = pd.read_csv(wb_gdp_path)

# Merge Data
nature_tourism_initial = pd.merge(
    unwto_exp, 
    prob_nature,
    how='left',
    on='iso3',
    validate='many_to_one')

nature_tourism = pd.merge(
    nature_tourism_initial, 
    wb_gdp,
    how='left',
    on=['iso3','year'],
    validate='one_to_one')

# Ensure data is unique for country-year
assert nature_tourism[['iso3', 'year']].apply(tuple, axis=1).is_unique == True

# Calculate GEP from expenses, gdp
nature_contribution_factor = 0.75
nature_tourism['gep_from_exp'] = nature_tourism['expense'] * nature_tourism['percentage_tourism_area'] * nature_contribution_factor
nature_tourism['gep_from_gdp'] = nature_tourism['gdp_tourism_usd'] * nature_tourism['percentage_tourism_area'] * nature_contribution_factor


# Options for plotting
import seaborn as sns
import matplotlib.pyplot as plt

# Create a line plot using seaborn
plt.figure(figsize=(12, 6))
sns.lineplot(data=nature_tourism, x='year', y='gep_from_exp', hue='country', alpha=0.5, linewidth=1)

# Add labels and title
plt.title('Nature Based Tourism from Expenditure')
plt.xlabel('Year')
plt.ylabel('NBT Expenditure')
# plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
plt.close()


# Create a line plot using seaborn
plt.figure(figsize=(12, 6))
sns.lineplot(data=nature_tourism, x='year', y='gep_from_gdp', hue='country', alpha=0.5, linewidth=1)

# Add labels and title
plt.title('Nature Based Tourism from GDP')
plt.xlabel('Year')
plt.ylabel('NBT from GDP')
# plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
plt.close()




import plotly.express as px

# Create an interactive line plot using Plotly
fig = px.line(nature_tourism, x='year', y='gep_exp', color='country', 
              labels={'gep_exp': 'Government Expenditure', 'year': 'Year'},
              title='Government Expenditure Over Time by Country')
fig.update_layout(legend_title_text='Country', hovermode='x unified')
fig.show()