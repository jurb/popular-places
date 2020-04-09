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

# +
import pandas as pd
import numpy as np
import folium
import datetime
import json

# Meer regels laten zien in jupyter
pd.set_option('display.max_rows', 100)
# -

# De [Functiekaart](https://maps.amsterdam.nl/functiekaart/?LANG=nl) op maps.amsterdam.nl toont de functie van gebouwen die geen woningen zijn. Voor het prototype matching willen wij verschillende categoriën hieruit filteren, en de data in een werkbaar bestand omzetten.

# CSV inlezen
df = pd.read_csv('https://maps.amsterdam.nl/open_geodata/excel.php?KAARTLAAG=FUNCTIEKAART&THEMA=functiekaart', delimiter=';')

# ## Data bekijken

# Even kijken
df.head()



# Group en sum de soorten gebouwen in hoofdfuncties en subfuncties
df.groupby(['FUNCTIE1_OMS','FUNCTIE2_OMS']).size()

# Alleen count van hoofdfuncties
df.groupby(['FUNCTIE1_OMS']).size()

# ## Data selecteren, platslaan naar 1 categorie, titles correct capitalizen

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
df_final.to_json('../src/assets/functies.json', orient="records")
# -

df_final

# ## Op een kaart plotten

# +
amsterdam_centraal = [52.3702, 4.8952]
huidige_locatie = [52.38200068197066, 4.87652430311739]
slijterijen_zaaknaam = 'SLIJTER|GALL & GALL'

m = folium.Map(
    location = amsterdam_centraal,
    zoom_start = 13,
#     tiles='Stamen Terrain'
)


for index, row in df_filtered[df['ZAAKNAAM'].str.contains(slijterijen_zaaknaam, na=False) | df_filtered['FUNCTIE2_OMS'].str.contains('Supermarkt groot', na=False)].iterrows():
    folium.Marker(
    location=[float(row['lat']), float(row['lon'])],
    popup=row['ZAAKNAAM'],
    icon=folium.Icon(color='green')).add_to(m)

folium.Marker(
    location=[float(huidige_locatie[0]), float(huidige_locatie[1])],
    popup='Huidige locatie',
    icon=folium.Icon(icon='cloud', color='red')).add_to(m)
    
    
m
# -



import seaborn as sns


# + {"scrolled": false}
sns.distplot(df['FUNCTIE1_OMS'].T.value_counts())
# -

df_filtered

df_filtered.to_json('flat.json', orient="records")

df_filtered
