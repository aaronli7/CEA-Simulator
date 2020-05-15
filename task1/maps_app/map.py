import pandas as pd
import numpy as np
import json
cg_data = pd.read_csv('Final.csv')



cg_data.shape


cg_data.head()
cg_data_clean = cg_data



cg_data_clean = cg_data_clean.rename(columns={'id': 'Location ID',

                                             'latitude':'latitude',

                                             'longitude':'longitude'})



# def clean_description(description):
#     description = description.strip()
#     while((description.startswith(',') or description.endswith(',')) and len(description) > -1):
#        if description.endswith(',') :
#            description = description[0:len(description)-1]
#        if description.startswith(',') :
#            description = description[1:len(description)]
#        description = description.strip()
#     return description

# apply the clean_description function to all rows

# cg_data_clean['description'] = cg_data_clean.description.apply(lambda x: clean_description(x))

collection = {'type':'FeatureCollection', 'features':[]}

# function to create a feature from each row and add it to the collection

def feature_from_row(id, latitude, longitude):

   feature = { 'type': 'Feature',

              'properties': { 'id': ''},

              'geometry': { 'type': 'Point', 'coordinates': []}

              }

   feature['geometry']['coordinates'] = [longitude, latitude]

   feature['properties']['id'] = id

   collection['features'].append(feature)

   return feature
# apply the feature_from_row function to populate the feature collection geojson_series = geojson_df.apply(lambda x: feature_from_row(x['title'],x['latitude'],x['longitude'],x['description']),axis=1)
with open('collection.geojson', 'w') as outfile:
   json.dump(collection, outfile)
