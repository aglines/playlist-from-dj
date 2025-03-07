import requests
import json
import os
from dotenv import load_dotenv, set_key

load_dotenv()
ENV_PATH = os.getenv("ENV_PATH")

hosts = 'https://api.kexp.org/v2/hosts/'
timeslots = 'https://api.kexp.org/v2/timeslots/'

# Goal:  Find the specific DJ ID from the API data
# This code will be only run once, so no need to make it a function
# and minimal error handling is needed

# First, look at the list of hostIDs and names
    
response = requests.get(hosts)
response = response.json()

for i in response['results']:
    print(i['name'], i['id'])

# The DJ's name doesn't immediately appear in the list of host names
# We could hunt through a full list of responses
# But we also know the show name and its timeslot
# so maybe the timeslots API has the info we need

response = requests.get(timeslots)
response = response.json()

for i in response['results']:
    print(i['program_name'], i['host_names'], i['hosts'])

# Got it. The DJ's name is in the timeslots API response
# The hostID for this DJ is 26

set_key(ENV_PATH, "DJ_ID", "26")
