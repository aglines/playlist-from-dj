import json
import requests
import base64
import spotipy
# Include client ID, client secret
from private_data import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

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
    print(f"access token : {token}")
    return token

if __name__ == '__main__':
    req_token()