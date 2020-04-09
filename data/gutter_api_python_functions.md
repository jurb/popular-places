```python
import pandas as pd
import requests

def api_get_access_token(login_endpoint, username, password):
    r = requests.post(login_endpoint, {"username": username, "password": password})
    return r.json()['access_token']

login_endpoint = 'https://api.stadswerken.amsterdam/login'
endpoint = 'https://api.stadswerken.amsterdam/address_research_data'
token = api_get_access_token(login_endpoint, 'USER', 'PASS')
headers = {"Authorization":"Bearer %s" %token}

def api_list_records(endpoint, headers):
    r = requests.get(endpoint, headers=headers)
    return r.json()

def api_post_new_record(endpoint, jsondata, headers):
    requests.post(endpoint, json=jsondata, headers=headers)

# Example of posting all rows from a dataframe:
# for row in df_final.to_dict(orient="records"):
#     api_post_new_record(endpoint, row, headers)

def api_list_all_records(filter_string):
    skip = 0
    allrecords = []
    recordsfound = True
    while recordsfound:
        records_on_page = api_list_records(endpoint + "?$skip=" + str(skip) + filter_string, headers)
        if (records_on_page != []):
            allrecords.append(records_on_page)
            skip = skip + 500
        else:
            recordsfound = False
    return [item for sublist in allrecords for item in sublist]

def api_update_record(endpoint_id, jsondata, headers):
    requests.put(endpoint_id, json=jsondata, headers=headers)

def api_get_array_of_values_in_column(column_name, fstring):
    return [d[column_name] for d in api_list_all_records(filter_string=fstring)]

def api_delete_record(endpoint_id, headers):
    requests.delete(endpoint_id, headers=headers)
```