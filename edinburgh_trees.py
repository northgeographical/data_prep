import os
import pandas as pd
import geopandas as gpd
from pyproj import Proj, transform

## Concatenate all spreadsheets together

# filenames
excel_path = 'path to data'

excel_names = []
for f in os.listdir(excel_path):
    fp = os.path.join(excel_path, f)
    excel_names.append(fp)

# read each file
excels = [pd.ExcelFile(name) for name in excel_names]

# turn them into dataframes
frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]

# concatenate all the dataframes
combined = pd.concat(frames)

# write combined files to new file
combined.to_excel("tree_data.xlsx", header=False, index=False)

## Read in data
tree_data = r'path to data'
names = ['type_latin', 'Type', 'code1', 'code2', 'Location1', 'Location2', 'name', 'Coordinates', 'Height', 'age', 'age2', 'Height2']
data = pd.read_excel(tree_data, header=None, names=names)[['Type', 'Coordinates', 'Height']]
data.head()

# filter data
data = data[data['Coordinates'] != 'Tree not fixed']
data = data[data['Coordinates'] != ' 000000,000000']

# separate coordinates into eastings and northings
eastings = []
northings = []

coords = data['Coordinates'].values.tolist()
for c in coords:
    eastings.append(c[1:7])
    northings.append(c[8:])
    
# convert each to integer
eastings = [int(num) for num in eastings]
northings = [int(num) for num in northings]

# convert eastings and northings into latitude and longitude
inProj = Proj(init='epsg:27700')
outProj = Proj(init='epsg:4326')
x1, y1 = eastings, northings
x2, y2 = transform(inProj, outProj, x1, y1)

data = data.drop(columns='Coordinates')

# print all height ranges
print(data['Height'].unique())

# replace all height ranges with maximum value integer
data['Max Height'] = data['Height'].replace('Up to 5 meters', 5)
data['Max Height'] = data['Max Height'].replace('5 to 10 meters', 10)
data['Max Height'] = data['Max Height'].replace('10 to 15 meters', 15)
data['Max Height'] = data['Max Height'].replace('15 to 20 meters', 20)
data['Max Height'] = data['Max Height'].replace('20 to 25 meters', 25)
data['Max Height'] = data['Max Height'].replace('30 meters +', 30)

# write tree height dataset to csv file
tree_height_data = data[['Type', 'Max Height', 'Latitude', 'Longitude']]
tree_height_data.to_csv('tree_heights.csv')

# write tree types dataset to csv file
tree_loc = data[['Type', 'Height', 'Latitude', 'Longitude']]
data.to_csv('edi_tree_locations.csv')
