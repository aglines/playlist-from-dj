import requests
import json
from config.private_data import API_SOURCE_URL_HOSTS

url = API_SOURCE_URL_HOSTS
names_ids = {}

# get the list of hostIDs to identify the specific DJ
def get_host_ids():
    response = requests.get(url)
    if response.status_code not in range(200,201):
        print(f"Error in API request response: {response.status_code}")
    response=response.json()
    data=response['results']
    for i in data:
        names_ids[i['name']] = i['id']
    
    print(names_ids)

get_host_ids()


