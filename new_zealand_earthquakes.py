import pandas as pd
import geopandas as gpd
import os, glob

## Merge all csv files together

# filenames
path = 'path to data'

# Specify the path for each csv file in the folder
extension = 'csv'
all_filenames = [i for i in glob.glob(os.path.join(path, '*.{}'.format(extension)))]

# Combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

# Export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

# Read in data
data_path = 'path to data'
data = pd.read_csv(data_path)

# Remove white spaces from column headers
data.columns = data.columns.str.strip()

# Subset data
earthquake_data = data[['origintime', 'longitude', 'latitude', 'magnitude', 'depth']]

# Check for null values
earthquake_data.isna().sum()

## Creating year, month and day column

# Convert date column into datetime objects
earthquake_data['origintime'] = pd.to_datetime(earthquake_data['origintime'])

# Subset each date value into year, month and day columns
earthquake_data['Year'] = pd.DatetimeIndex(earthquake_data['origintime']).year  
earthquake_data['Month'] = pd.DatetimeIndex(earthquake_data['origintime']).month 
earthquake_data['Day'] = pd.DatetimeIndex(earthquake_data['origintime']).day

# View first 5 rows of data
earthquake_data.head()

earthquake_data.to_csv('nz_earthquakes.csv')

# Filter data 
mask = (earthquake_data['magnitude'] >= 3.0)
earthquake_data = earthquake_data.loc[mask]

# Write to csv file
earthquake_data.to_csv('nz_earthquakes_subset.csv')
