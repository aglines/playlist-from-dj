import requests
import json
from config.private_data import API_SOURCE_URL_HOSTS, API_SOURCE_URL_TIMESLOTS

# Goal:  Find the specific DJ ID from the API data
# This code will be only run once, so no need to make it a function
# and minimal error handling is needed

# First, look at the list of hostIDs and names
    
url = API_SOURCE_URL_HOSTS
response = requests.get(url)
response=response.json()

for i in response['results']:
    print(i['name'], i['id'])

# The DJ's name doesn't immediately appear in the list of host names
# We could hunt through a full list of responses
# But we also know the show name and its timeslot
# so maybe the timeslots API has the info we need

url = API_SOURCE_URL_TIMESLOTS
response = requests.get(url)
response=response.json()

for i in response['results']:
    print(i['program_name'], i['host_names'], i['hosts'])

# Got it. The DJ's name is in the timeslots API response
# The hostID for this DJ is 26

