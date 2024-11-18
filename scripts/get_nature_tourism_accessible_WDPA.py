import geopandas as gpd
import pandas as pd  # Import pandas
import os

def is_tourism_accessible(desig):
    desig_lower = desig.lower() if desig else ''
    
    exclude_keywords = [
        'strict', 'private', 'buffer zone', 'core zone', 'proposed',
        'not reported', 'not assigned', 'undesignated', 'closed',
        'experimental', 'scientific', 'research', 'hunting', 'no entry',
        'restricted', 'exclusion', 'military', 'non-suitable', 'easement',
        'others', 'other', 'habitat protection area', 'no recommendation',
        'closed forest reserve', 'buffer'
    ]
    
    include_keywords = [
        'park', 'national park', 'marine park', 'monument', 'garden',
        'heritage', 'recreation', 'scenic', 'protected landscape',
        'historic site', 'nature reserve', 'natural monument',
        'botanical garden', 'world heritage site', 'state park',
        'provincial park', 'natural park', 'conservation area', 'refuge',
        'wildlife refuge', 'eco-park', 'eco park', 'ramsar', 'tourism',
        'tourist', 'protected area', 'natural features reserve',
        'marine reserve', 'biodiversity reserve', 'protected landscape',
        'wetland reserve', 'wilderness area', 'marine sanctuary',
        'national monument', 'nature park', 'community forest',
        'nature sanctuary', 'wildlife sanctuary', 'biosphere reserve',
        'archaeological reserve', 'forest park', 'national scenic area',
        'world heritage site', 'unesc', 'scenic reserve', 'wilderness park'
    ]
    
    for keyword in exclude_keywords:
        if keyword in desig_lower:
            return False
    
    for keyword in include_keywords:
        if keyword in desig_lower:
            return True
    
    return False

# Paths to the three WDPA shapefiles
shp_paths = [
    r"D:\Users\lifengren\Dropbox\400_research\440_UMN\gep\gep_recreation\data\spatial\WDPA_Jul2024_Public_shp\WDPA_Jul2024_Public_shp_0\WDPA_Jul2024_Public_shp-polygons.shp",
    r"D:\Users\lifengren\Dropbox\400_research\440_UMN\gep\gep_recreation\data\spatial\WDPA_Jul2024_Public_shp\WDPA_Jul2024_Public_shp_1\WDPA_Jul2024_Public_shp-polygons.shp",
    r"D:\Users\lifengren\Dropbox\400_research\440_UMN\gep\gep_recreation\data\spatial\WDPA_Jul2024_Public_shp\WDPA_Jul2024_Public_shp_2\WDPA_Jul2024_Public_shp-polygons.shp"
]

# Output directory for filtered shapefiles
output_dir = r"D:\Users\lifengren\Dropbox\400_research\440_UMN\gep\gep_recreation\data\spatial\wdpa_tourism"
os.makedirs(output_dir, exist_ok=True)

# List to hold filtered GeoDataFrames
filtered_gdfs = []

# Process each shapefile
for i, shp_path in enumerate(shp_paths):
    gdf = gpd.read_file(shp_path)
    gdf_filtered = gdf[gdf['DESIG_ENG'].apply(is_tourism_accessible)]
    filtered_gdfs.append(gdf_filtered)
    print(f"Processed {shp_path} with {len(gdf_filtered)} records.")

# Merge all filtered GeoDataFrames and ensure CRS consistency
merged_gdf = gpd.GeoDataFrame(pd.concat(filtered_gdfs, ignore_index=True), crs=filtered_gdfs[0].crs)

# Save the merged GeoDataFrame
merged_output_path = os.path.join(output_dir, "WDPA_tourism_merged.shp")
merged_gdf.to_file(merged_output_path)

print(f"Merged shapefile saved to {merged_output_path}")
