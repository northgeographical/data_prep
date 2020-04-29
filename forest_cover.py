'''

This Script is used to prepare the World Forest Cover dataset for the Choropleth Map visualization example.

'''



# Import Modules
import pandas as pd
import geopandas as gpd

# Forest Land Cover data
file = r'path to file'

# Rename column names
col_names = ['Entity', 'Code', 'Year', 'Forest area as a proportion of total land area (%)']
forest_cover = pd.read_csv(file, names=col_names, skiprows=1)
forest_cover = forest_cover.fillna('NaN')

# Filter to year 2015 and show first 5 rows
forest_cover = forest_cover[forest_cover['Year'] == 2015]
forest_cover.head()

# Check data for null values
forest_cover.isna().sum()

# Rename country codes in forest cover dataset to match country shapefile
forest_cover.Code[forest_cover.Code=="ESH"] = 'SAH'
forest_cover.Code[forest_cover.Code=="PSE"] = 'PSX'
forest_cover.Code[forest_cover.Code=="CYN"] = 'CYP'
forest_cover.Code[forest_cover.Code=="SSD"] = 'SDS'

# Import World Country Boundary Data
file = r'C:\Users\Jakeh\Desktop\python_prog\mastering_geospatial\geospatial_data/ne_110m_admin_0_countries.shp'
countries = gpd.read_file(file)[['ADMIN', 'ADM0_A3', 'geometry']]
countries.columns = ['Country_Name', 'Country_Code', 'geometry']

# Remove Antarctica and merge forest cover data to boundary data
world = countries[(countries['Country_Name']!='Antarctica')]
world_forest_cover = world.merge(forest_cover, left_on='Country_Code', right_on='Code', how='left')

# Subset columns and view data 
world_forest_cover = world_forest_cover[['Country_Name', 'Country_Code', 'Code', 'Year', 'Forest area as a proportion of total land area (%)', 'geometry']]
world_forest_cover.head()

# Check using matplotlib
import matplotlib.colors as colors

# Plot basemap
ax = world.plot(
    color = "lightslategray", 
    edgecolor = "slategray", 
    linewidth = 0.5, figsize=(18, 6));
ax.set_facecolor("slategray")
ax.set_clip_on(False)
#ax.axis('off')

# Plot World Forest Cover Data
world_forest_cover.plot(
    ax=ax, 
    column="Forest area as a proportion of total land area (%)",
    legend=True,
    legend_kwds={'label': "Forest area as a proportion of total land area (%)"},
    cmap='Greens')
    
# Export to GeoJSON file

# Import Module
from geopandas import GeoDataFrame

# Set CRS and convert to GeoDataFrame
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(world_forest_cover, crs=crs, geometry='geometry')

# Write to GeoJSON file
world_forest_cover.to_file('world_forest_cover.geojson', driver='GeoJSON', encoding="utf-8")
