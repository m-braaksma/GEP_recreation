"""
Purpose: 
"""

# Dependencies 
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt


# Define Data Paths
unwto_path = 'intermediate/unwto-expenses-cleaned.csv'
prob_nature_path = 'intermediate/ee_r264_prob_nature_tourism.csv'
wb_gdp_path = 'intermediate/gep_tourism.csv'

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


# PLOTS
# Expenditure
# Create a line plot using seaborn
plt.figure(figsize=(12, 6))
sns.lineplot(data=nature_tourism, x='year', y='gep_from_exp', hue='country', alpha=0.5, linewidth=1, legend=None)

# Get the ending points for each country
end_points = nature_tourism.groupby('country').last()[['gep_from_exp']]

# Sort the countries by the ending point and select the top 5
top_5_countries = end_points.nlargest(5, 'gep_from_exp').index

# Loop through the top 5 countries and add labels
for country in top_5_countries:
    country_data = nature_tourism[nature_tourism['country'] == country]
    last_year = country_data['year'].iloc[-1]
    last_value = country_data['gep_from_exp'].iloc[-1]
    plt.text(last_year, last_value, country, ha='left', va='bottom', fontsize=9)

# Add labels and title
plt.title('Nature Based Tourism from Expenditure')
plt.xlabel('Year')
plt.ylabel('NBT Expenditure')
plt.grid(True)
plt.tight_layout()
plt.savefig('figures/gep_from_exp_line.png', format="png")
plt.close()


# GDP
# Create a line plot using seaborn
# Subset the data for years 2008 to 2019
subset_data = nature_tourism[(nature_tourism['year'] >= 2008) & (nature_tourism['year'] <= 2019)]

plt.figure(figsize=(12, 6))

# Plot the subsetted data
sns.lineplot(data=subset_data, x='year', y='gep_from_gdp', hue='country', alpha=0.5, linewidth=1, legend=None)

# Get the ending points for each country
end_points = subset_data.groupby('country').last()[['gep_from_gdp']]

# Sort the countries by the ending point and select the top 5
top_5_countries = end_points.nlargest(5, 'gep_from_gdp').index

# Loop through the top 5 countries and add labels
for country in top_5_countries:
    country_data = subset_data[subset_data['country'] == country]
    last_year = country_data['year'].iloc[-1]
    last_value = country_data['gep_from_gdp'].iloc[-1]
    plt.text(last_year, last_value, country, ha='left', va='bottom', fontsize=9)

# Add labels and title
plt.title('Nature Based Tourism from GDP (2008–2019)')
plt.xlabel('Year')
plt.ylabel('NBT GDP')
plt.ylim(subset_data['gep_from_gdp'].min() * 0.9, subset_data['gep_from_gdp'].max() * 1.1)
plt.grid(True)
plt.tight_layout()
plt.savefig('figures/gep_from_gdp_line.png', format="png")
# plt.show()
plt.close()


# MAPS
user_dir = os.path.expanduser('~')
gadm_path = os.path.join(user_dir, 'Files', 'base_data', 'cartographic', 'gadm', 'gadm_410-levels.gpkg')

# Calculate percentage change for 'gep_from_exp'
percent_change = (
    nature_tourism.groupby('iso3')
    .agg(
        start_exp=('gep_from_exp', 'first'),
        end_exp=('gep_from_exp', 'last'),
        percentage_tourism_area=('percentage_tourism_area', 'first')  # Assuming this is constant
    )
)
percent_change['percent_change_exp'] = ((percent_change['end_exp'] - percent_change['start_exp']) / percent_change['start_exp']) * 100
collapsed_data = percent_change[['percentage_tourism_area', 'percent_change_exp']].reset_index()

# Merge
boundaries = gpd.read_file(gadm_path, layer='ADM_0', engine='pyogrio')
mapping_gdf = boundaries.merge(
    collapsed_data, 
    left_on='GID_0',
    right_on='iso3',
    how='left',
    validate='one_to_one')

# Plot the map with the percentage of protected areas
ax = mapping_gdf.plot(
    column='percentage_tourism_area',  # Assuming this column represents % of protected areas
    legend=True,
    legend_kwds={
        "label": "Percentage of Protected Areas",  # Update the label for clarity
        "orientation": "horizontal",
        'shrink': 0.6,
    }
)
ax.set_axis_off()
ax.set_title('Percentage of Tourism Expenditure Attributed to Nature\nBased on Area of Protected Areas', fontsize=12)
plt.savefig('figures/percentage_tourism_map.png', format="png", bbox_inches="tight")  # Save as PNG
# plt.show()  # Display the plot
plt.close()  # Close the plot