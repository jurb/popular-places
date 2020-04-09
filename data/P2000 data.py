# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext_format_version: '1.2'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.6.4
# ---

import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('postgresql://jurian:wonen@oscity.nl:6003/stadswerken')

# +
# df = pd.read_sql_query('SELECT * FROM "p2000"."p2000meldingen" WHERE "datetime_last" > "2016-12-31" AND "description" LIKE "Amsterdam"',con=engine)
date = '2016-12-31'
like = '%%Amsterdam%%'
# df = pd.read_sql_query('SELECT * FROM "p2000"."p2000meldingen" WHERE "datetime_last" > {date} AND "description" LIKE {like}'.format(date=date, like=like), con=engine)

df = pd.read_sql_query('SELECT * FROM "p2000"."p2000meldingen_adam"', con=engine)


# -

df

df.type.unique()

df_politie = df.loc[df['type'] == 'POLITIE']

df_politie

# Create even-odd rule function, see https://en.wikipedia.org/wiki/Even–odd_rule
def is_point_in_path(x, y, poly):
    """
    x, y -- x and y coordinates of point
    poly -- a list of tuples [(x, y), (x, y), ...]
    """
    num = len(poly)
    i = 0
    j = num - 1
    c = False
    for i in range(num):
        if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
                                  (poly[j][1] - poly[i][1])):
            c = not c
        j = i
    return c

import geojson
# Put geojson in variable
with open('GEBIED_BUURTEN.json') as geojson_file:    
     my_geojson = geojson.load(geojson_file)

# Create function that outputs an Array with the names of the nearest worm hotel, or 'Not found'
def lookup_location_in_geojson(my_geojson,lng,lat):
    geos = []
    for i in range(len(my_geojson['features'])):
        geos.append(list(geojson.utils.coords(my_geojson['features'][i])))
    coordinates = []
    for i in range(len(geos)):
        if is_point_in_path(lng,lat,geos[i]):
            return my_geojson['features'][i]
    not_found = { 'properties': {
                'Buurt_code': 'Not found'
                } 
             }
    return not_found

lookup_location_in_geojson(my_geojson, 2.894490, 52.379494) # Near my house
# lookup_location_in_geojson(my_geojson, 4.876480, 52.381994).properties["Buurt_code"]

df_politie['Buurt_code'] = df_politie.apply(lambda x: lookup_location_in_geojson(my_geojson, x.lng, x.lat)['properties']["Buurt_code"], axis=1)

df_politie.iloc[494].Buurt_code['properties']['Buurt_code']

# +
not_found = { 'properties': {
                'Buurt_code': 'Not found'
                } 
             }


not_found['properties']['Buurt_code']

# -

df_politie.dtypes

df_politie

# +
import pandas as pd
import geojson

def data2geojson(df, geojson_file_name):
    features = []
    insert_features = lambda X: features.append(
            geojson.Feature(geometry=geojson.Point((X["lat"],
                                                    X["lng"])),
                            properties=dict(
                                            # datetime_first = X['datetime_first'],
                                            # datetime_last = X['datetime_last'],
                                            id = X['id'],
                                            # timestamp = X['timestamp'],
                                            description = X['description'],
                                            street = X['street'],
                                            type = X['type'],
                                            # lng = X['lng'],
                                            # lat = X['lat']
                                            )))
    df.apply(insert_features, axis=1)
    with open(geojson_file_name, 'w', encoding='utf8') as fp:
        geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)



# -

data2geojson(df_politie, 'politie_test.geojson')

df_politie.to_csv('p2000_politie.csv')

politie_arrays = df_politie[['lat', 'lng']].values

# + {"scrolled": true}
politie_arrays

# +
with open('p2000_politie.js', 'w') as thefile:
    for item in politie_arrays:
        thefile.write("%s\n" % item)

    
# -

politie_arrays.savetxt('test.js')

import numpy as np
np.savetxt('test.js', politie_arrays, delimiter=',', fmt='%1.6f')

df_politie[['lat', 'lng']].to_json('politie.json', orient="records")


