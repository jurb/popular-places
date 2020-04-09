# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext_format_version: '1.2'
#   kernel_info:
#     name: python3
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
#   nteract:
#     version: 0.11.6
# ---

import pandas as pd
import numpy as np
from titlecase import titlecase
import requests
import datetime
import json
from humps.camel import case


# CSV inlezen
df = pd.read_csv('https://maps.amsterdam.nl/open_geodata/excel.php?KAARTLAAG=FUNCTIEKAART&THEMA=functiekaart', delimiter=';')

# +
# Converteer LAT LNG columns naar een punt als decimal
df['lon'] = pd.to_numeric(df['LNG'].str.replace(',','.'))
df['lat'] = pd.to_numeric(df['LAT'].str.replace(',','.'))

# Categorieën die we gaan uitsluiten (waardes van de FUNCTIE1_OMS kolom)
nietrelevant_FUNCTIE1_OMS = 'Bedrijven|Kantoren|Openbaar vervoer|Parkeren'

# Subcategorien die we gaan uitsluiten (waardes van de FUNCTIE2_OMS kolom)
nietrelevant_FUNCTIE2_OMS = 'Opstappunt rondvaart - waterfiets|Onduidelijk'

# Kolommen die we willen behouden
# 'ADRESSEN_LIJST'
relevante_kolommen = ['FUNCTIE1_OMS', 'FUNCTIE2_OMS', 'ZAAKNAAM', 'lon', 'lat', 'ZAAK_ID']

# Nieuwe dataframe zonder niet relevante data
df_filtered = df[relevante_kolommen]
df_filtered = df_filtered[~df_filtered['FUNCTIE1_OMS'].str.contains(nietrelevant_FUNCTIE1_OMS, na=False)]
df_filtered = df_filtered[~df_filtered['FUNCTIE2_OMS'].str.contains(nietrelevant_FUNCTIE2_OMS, na=False)]
df_filtered = df_filtered.fillna('')

# Hernoem detailhandel naar winkel, horeca naar overige horeca
# We houden cafés en coffeeshops apart van horeca
df_filtered['cat'] = df_filtered['FUNCTIE1_OMS']
df_filtered['cat'] = df_filtered['cat'].replace({'Detailhandel':'Winkels', 'Horeca': 'Horeca - Overig'})
df_filtered.loc[df_filtered['FUNCTIE2_OMS'] == 'Café - Eetcafé', 'cat'] = "Cafés"
df_filtered.loc[df_filtered['FUNCTIE2_OMS'] == 'Coffeeshop', 'cat'] = "Coffeeshops"

# Zelfde voor uitgaan: gokken, bioscopen en bordelen eruit
df_filtered['cat'] = df_filtered['cat'].replace({'Uitgaan en Toerisme': 'Uitgaan en Toerisme - Overig'})
df_filtered.loc[df_filtered['FUNCTIE2_OMS'] == 'Automatenhal - Casino', 'cat'] = "Gokhal"
df_filtered.loc[df_filtered['FUNCTIE2_OMS'] == 'Bioscoop - Filmhuis', 'cat'] = "Bioscoop"
df_filtered.loc[df_filtered['FUNCTIE2_OMS'] == 'Bordeel - Raamprostitutie - Sexclub', 'cat'] = "Prostitutie"

# Zelfde voor zorg: dag- en nachtopvang eruit
df_filtered['cat'] = df_filtered['cat'].replace({'Zorg': 'Zorg - Overig'})
df_filtered.loc[df_filtered['FUNCTIE2_OMS'] == 'Dag- en nachtopvang', 'cat'] = "Dag- en nachtopvang"

# Output filtered vs hele dataset, telling en output waarden eerste keer draaien script
print('Waarde 2018-07-20:')
print('18900 objecten (filtered) vs 28189 (hele dataset)')
print('Waarde ' + str(datetime.datetime.today()).split()[0] + ':')
print(str(len(df_filtered)) + " objecten (filtered) vs " + str(len(df)) + " (hele dataset)")

# Titlecase names with a locally adjusted version of the titlecase 
# module: https://github.com/ppannuto/python-titlecase
from titlecase import titlecase

def title_exceptions(word, **kwargs):
#     print(word)
    if word.upper() in ('BV', 'AKO','AH','PT020', 'IJ', 'VTP', 'ID', 'TV', 'HTML', 'XML', "URL", "HTTP", "VPN"):
        return word.upper()
    if word.upper() in ('VOF'):
        return word.lower()
    if "IJ" in word[:2]:
        return word.lower().replace('ij', 'IJ')

df_filtered['name'] = df_filtered['ZAAKNAAM'].apply((lambda x: titlecase(x, callback=title_exceptions)))

# Only keep what we need, rename columns
df_final = df_filtered[['name', 'cat', 'lon', 'lat', 'ZAAK_ID']].copy()
df_final.columns = ['name', 'cat', 'lon', 'lat', 'zaak_id']

# Write to JSON as records
df_final.to_json('../src/assets/data/functies.json', orient="records")

# Also create category JSON (todo: escape cafés to cafes)
with open('../src/assets/data/functies-categories.json', 'w') as outfile:
    json.dump([ {'category':x, 'camelName': case(x)} for x in df_final['cat'].unique()], outfile)



# + {"inputHidden": false, "outputHidden": false}
[ {'category':x, 'camelName': case(x)} for x in df_final['cat'].unique() ]

# + {"inputHidden": false, "outputHidden": false}

# -

def get_access_token(login_endpoint, username, password):
    r = requests.post(login_endpoint, {"username": username, "password": password})
    return r.json()['access_token']

login_endpoint = 'https://api.stadswerken.amsterdam/login'
endpoint = 'https://api.stadswerken.amsterdam/address_research_data'
token = get_access_token(login_endpoint, 'jurian', 'forest kosher thalamus shipyard hereby')
headers = {"Authorization":"Bearer %s" %token}

def list_records(endpoint, headers):
    r = requests.get(endpoint, headers=headers)
    return r.json()

def post_new_record(endpoint, jsondata, headers):
    requests.post(endpoint, json=jsondata, headers=headers)

# +
# import time
# for row in df_final.to_dict(orient="records"):
#     post_new_record(endpoint, row, headers)
# -

def list_all_records(filter_string):
    skip = 0
    allrecords = []
    recordsfound = True
    while recordsfound:
        records_on_page = list_records(endpoint + "?$skip=" + str(skip) + filter_string, headers)
        if (records_on_page != []):
            allrecords.append(records_on_page)
            skip += len(records_on_page)
        else:
            recordsfound = False
    return [item for sublist in allrecords for item in sublist]

# + {"scrolled": true}
def get_array_of_api_values(column_name, fstring):
    return [d[column_name] for d in list_all_records(filter_string=fstring)]
# -

get_array_of_api_values('name', '')

# + {"inputHidden": false, "outputHidden": false}
len(get_array_of_api_values('id', ''))
# -

def update_record(endpoint_id, jsondata, headers):
    requests.put(endpoint_id, json=jsondata, headers=headers)

# +
# empty = {}

# for id in [d['id'] for d in list_all_records()]:
#     update_record(endpoint + '/' + id, empty, headers)
# -

list_all_records()

len(list_all_records(filter_string="&$filter=id eq 'a6e05e8f-a507-4262-96d4-0315f8b89ab1'"))

# + {"inputHidden": false, "outputHidden": false}


# + {"inputHidden": false, "outputHidden": false}


# + {"inputHidden": false, "outputHidden": false}


# + {"inputHidden": false, "outputHidden": false}
df_final["cat"].unique()

# + {"inputHidden": false, "outputHidden": false}



# + {"inputHidden": false, "outputHidden": false}


# + {"inputHidden": false, "outputHidden": false}
def list_column_value_duplicates(column_value, all_records):
    all_records_var = all_records
    column_value_set = set(d.get(column_value) for d in all_records_var)
    new_dict = {}
    duplicates = []
    for k in column_value_set:
        records_with_column_value = [d for d in all_records_var if d.get(column_value) == k]
        new_dict[k] = records_with_column_value
    for row in new_dict:
        if (len(new_dict[row]) > 1):
            duplicates.append(new_dict[row])
    duplicate_ids = []
    for dupe in duplicates:
        duplicate_ids.append(dupe[1:][0]['id'])
    return duplicate_ids

# + {"inputHidden": false, "outputHidden": false}
bla = list_column_value_duplicates('zaak_id', list_all_records(filter_string=""))
bla

# + {"inputHidden": false, "outputHidden": false}
# empty = {}

# for id in bla:
#     update_record(endpoint + '/' + id, empty, headers)
# -

len(bla)

# + {"inputHidden": false, "outputHidden": false}
len(list_all_records(filter_string="&$filter=cat gt 0"))

# + {"inputHidden": false, "outputHidden": false}
winkels = list_all_records(filter_string="&$filter=cat eq 'Winkels'")
onderwijs = list_all_records(filter_string="&$filter=cat eq 'Onderwijs'")

# + {"inputHidden": false, "outputHidden": false}
len(winkels)

# + {"inputHidden": false, "outputHidden": false}
df_final.groupby(['cat']).size()

# + {"inputHidden": false, "outputHidden": false}
list_all_records(filter_string="")

# + {"inputHidden": false, "outputHidden": false}
list_all_records(filter_string="&$filter=cat eq 'Zorg - Overig'")

# + {"inputHidden": false, "outputHidden": false}
list_all_records(filter_string="&$filter=cat eq ''")
# -



# + {"inputHidden": false, "outputHidden": false}
empty_values = get_array_of_api_values('id', "&$filter=cat eq ''")

# + {"inputHidden": false, "outputHidden": false}
len(empty_values)

# + {"inputHidden": false, "outputHidden": false}
def delete_record(endpoint_id, headers):
    requests.delete(endpoint_id, headers=headers)

# + {"inputHidden": false, "outputHidden": false}
# for v in get_array_of_api_values('id', "&$filter=cat eq ''"):
#     delete_record(endpoint + '/' + v, headers)

# + {"inputHidden": false, "outputHidden": false}
list_all_records(filter_string="")
# -

# [![Screen_Shot_2018-07-31_at_14.54.34.png](https://s8.postimg.cc/zan7875xh/Screen_Shot_2018-07-31_at_14.54.34.png)](https://postimg.cc/image/yl4evu5dt/)


