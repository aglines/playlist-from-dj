import requests, os, json, time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
from get_showsongs_fromdb import pick_show_date, process_current_show
import sys

def get_artist_track_spotify(show_artist_song, curr_token, show_date):

    endpoint = 'https://api.spotify.com/v1/search'

    # API requires URL encoded strings
    show_artist_song = [[i.replace(' ', '%20') for i in x]
        for x in show_artist_song]
    results = []

    # Playlist API requires a track ID, not just artist and track name
    for artist, track in show_artist_song:
        query = f'{endpoint}'
        query += f'?q=track%3A{track}%20artist%3A{artist}&type=track&limit=1'
        response = requests.get(query, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {curr_token}'})
        if response.status_code != 200:
            print(
                f'Error: {response.status_code}, body of error: {response.json()}')
            return None
        data = response.json()
        if not data['tracks']['items']:
            print(
                f'Skipping: Artist "{artist.replace("%20", " ")}" and Track "{track.replace("%20", " ")}" not found.')
            continue
        track_id = data['tracks']['items'][0]['id']
        track_name = data['tracks']['items'][0]['name']
        artist_id = data['tracks']['items'][0]['artists'][0]['id']
        artist_name = data['tracks']['items'][0]['artists'][0]['name']

        results.append({
            'artist_name': artist_name,
            'artist_id': artist_id,
            'track_name': track_name,
            'track_id': track_id
        })

    # Cache results locally with intent to annotate the archive db to avoid future API calls
    data_path = os.getenv('LOCAL_DATA_PATH')
    output_file = os.path.join(f'{data_path}/spotify', f'{show_date}.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    return results
