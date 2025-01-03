import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()
curr_token = os.getenv('CURR_TOKEN')

# test the connection to the Spotify API

def search_artist_track(artist, track):
    endpoint = 'https://api.spotify.com/v1/search'
    
    artist = artist.replace(' ', '+')
    track = track.replace(' ', '+')

    query = f'{endpoint}'
    query += f'?q=track%3A{track}%20artist%3A{artist}&type=track&limit=1'
    response = requests.get(query, headers={
        'Content-Type': 'application/json',
        'Authorization':f'Bearer {curr_token}'})
    if response.status_code != 200:
        print(f'Error: {response.status_code}')
        return None
    data = response.json()

    # get relevant data 
    track_id = data['tracks']['items'][0]['id']
    track_name = data['tracks']['items'][0]['name']
    artist_id = data['tracks']['items'][0]['artists'][0]['id']
    artist_name = data['tracks']['items'][0]['artists'][0]['name']

    print(track_id, track_name, artist_id, artist_name)

    return data

def main():

    # later, get show data from the db and search for the artist and track
    # for now just use a test case
    search_artist_track('The Beatles', 'Hey Jude')



if __name__ == '__main__':
    main()


