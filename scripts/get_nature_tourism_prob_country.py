import geopandas as gpd
import pandas as pd
import os

# Paths to input data
accessible_tourism_shp = r"D:\Users\lifengren\Dropbox\400_research\440_UMN\gep\gep_recreation\data\spatial\wdpa_tourism\WDPA_tourism_merged.shp"
countries_gpkg = r"C:\Users\lifengren\Files\base_data\cartographic\ee\ee_r264_ee_correspondence.gpkg"

# Output paths
output_gpkg = r"D:\Users\lifengren\Dropbox\400_research\440_UMN\gep\gep_recreation\data\spatial\wdpa_tourism\ee_r264_prob_nature_tourism.gpkg"
output_csv = r"D:\Users\lifengren\Dropbox\400_research\440_UMN\gep\gep_recreation\data\spatial\wdpa_tourism\ee_r264_prob_nature_tourism.csv"

# Read the accessible tourism areas shapefile
tourism_gdf = gpd.read_file(accessible_tourism_shp)

# Read the countries geopackage
countries_gdf = gpd.read_file(countries_gpkg, layer="ee_r264_ee_correspondence")

# Ensure both datasets use the same CRS suitable for area calculation
equal_area_crs = "EPSG:6933"  # Equal Earth projection for accurate area calculations

# Reproject to equal-area CRS
tourism_gdf = tourism_gdf.to_crs(equal_area_crs)
countries_gdf = countries_gdf.to_crs(equal_area_crs)

# Convert 'id' columns to strings in countries_gdf
countries_gdf['id'] = countries_gdf['id'].astype(str)

# Calculate the area of each country in km^2
countries_gdf['country_area_km2'] = countries_gdf['geometry'].area / 10**6  # m^2 to km^2

# Drop 'tourism_area_km2' and 'intersection_area_km2' if they exist
for col in ['tourism_area_km2', 'intersection_area_km2']:
    if col in countries_gdf.columns:
        countries_gdf.drop(columns=[col], inplace=True)

# Overlay the tourism areas onto the countries
print("Computing intersections between countries and accessible tourism areas...")
intersection_gdf = gpd.overlay(
    countries_gdf, tourism_gdf, how='intersection', keep_geom_type=False
)

# Calculate the area of the intersected geometries in km^2
intersection_gdf['intersection_area_km2'] = (
    intersection_gdf['geometry'].area / 10**6
)  # m^2 to km^2

# The 'id' column in intersection_gdf comes from countries_gdf
# Ensure 'id' is a string
intersection_gdf['id'] = intersection_gdf['id'].astype(str)

# Sum the intersection areas for each country
tourism_area_by_country = (
    intersection_gdf.groupby('id')['intersection_area_km2'].sum().reset_index()
)

print(f"Number of records in countries_gdf: {len(countries_gdf)}")
print(f"Number of records in intersection_gdf: {len(intersection_gdf)}")
print(f"Number of records in tourism_area_by_country: {len(tourism_area_by_country)}")

# Merge the tourism area data back to the countries_gdf with suffixes
countries_gdf = countries_gdf.merge(
    tourism_area_by_country, on='id', how='left', suffixes=('', '_new')
)

# Replace NaN values with 0 for countries with no accessible tourism areas
countries_gdf['intersection_area_km2'] = countries_gdf[
    'intersection_area_km2'
].fillna(0)

# Rename the intersection column to 'tourism_area_km2'
countries_gdf.rename(
    columns={'intersection_area_km2': 'tourism_area_km2'}, inplace=True
)

# Ensure area columns are numeric
countries_gdf['country_area_km2'] = pd.to_numeric(
    countries_gdf['country_area_km2'], errors='coerce'
).fillna(0)
countries_gdf['tourism_area_km2'] = pd.to_numeric(
    countries_gdf['tourism_area_km2'], errors='coerce'
).fillna(0)

# Recalculate percentage
countries_gdf['percentage_tourism_area'] = countries_gdf.apply(
    lambda row: (row['tourism_area_km2'] / row['country_area_km2'] * 100)
    if row['country_area_km2'] > 0 else 0,
    axis=1
)

# Save the updated countries_gdf to a new geopackage file
countries_gdf.to_file(output_gpkg, driver='GPKG')

# Create a simple CSV file with selected columns (removed 'fid')
csv_columns = [
    'id',
    'ee_r264_label',
    'ee_r264_name',
    'country_area_km2',
    'tourism_area_km2',
    'percentage_tourism_area',
]
countries_gdf[csv_columns].to_csv(output_csv, index=False)

print(f"Analysis complete. Outputs saved to {output_gpkg} and {output_csv}")
