import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
hosts = os.getenv('API_SOURCE_URL_HOSTS')
timeslots = os.getenv('API_SOURCE_URL_TIMESLOTS')
# from config.private_data import API_SOURCE_URL_HOSTS, API_SOURCE_URL_TIMESLOTS

# Goal:  Find the specific DJ ID from the API data
# This code will be only run once, so no need to make it a function
# and minimal error handling is needed

# First, look at the list of hostIDs and names
    
response = requests.get(hosts)
response=response.json()

for i in response['results']:
    print(i['name'], i['id'])

# The DJ's name doesn't immediately appear in the list of host names
# We could hunt through a full list of responses
# But we also know the show name and its timeslot
# so maybe the timeslots API has the info we need

response = requests.get(timeslots)
response=response.json()

for i in response['results']:
    print(i['program_name'], i['host_names'], i['hosts'])

# Got it. The DJ's name is in the timeslots API response
# The hostID for this DJ is 26

