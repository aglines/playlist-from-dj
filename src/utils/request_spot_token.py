import json
import requests
import base64
import spotipy
from dotenv import load_dotenv, set_key
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
ENV_PATH = os.getenv("ENV_PATH")


def req_token():
    """gets a spotify web API token"""
    endpoint = 'https://accounts.spotify.com/api/token'
    # Encode creds in b64
    creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    creds_b64 = base64.b64encode(creds.encode())
    header = {"Authorization" : f"Basic {creds_b64.decode()}"}
    payload = {"grant_type" : 'client_credentials'}
    r = requests.post(endpoint, headers=header, data=payload)
    if r.status_code not in range(200,299):
        raise Exception("could not authenticate client. Status code was : ", r.status_code)
    token = r.json()["access_token"]
    set_key(ENV_PATH, "CURR_TOKEN", token)
    print("New token updated and saved to .env")

    return token

if __name__ == '__main__':
    req_token()

