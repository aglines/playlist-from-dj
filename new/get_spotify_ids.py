import requests, os, json, time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
from get_showsongs_fromdb import pick_show_date, process_current_show
import sys

def get_artist_track_spotify(show_artist_song, curr_token, curr_show):
    '''Get the artist and track from Spotify API'''

    endpoint = 'https://api.spotify.com/v1/search'

    # replace spaces with the encoded version
    show_artist_song = [[i.replace(' ', '%20') for i in x]
                        for x in show_artist_song]

    results = []

    # Get track ID and artist ID for each song in the list
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
        # get relevant data
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

        # rate limit just in case
        time.sleep(2)
    print(f"Results: {results}")
    # Save results to a JSON file
    with open(f'{curr_show}.json', 'w') as f:
        json.dump(results, f, indent=4)
    return results

if __name__ == '__main__':
    load_dotenv()
    curr_token = os.getenv('CURR_TOKEN')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')
    scope = 'playlist-modify-public'

    # User supplies a date at the command line in ISO format
    show_date = sys.argv[1]
    # From that date, get the show number
    show_number = pick_show_date(show_date)
    # Get the artist and song for the show, from file get_songs_fromshow.py
    show_artist_song = process_current_show(show_number)

    # For each song in the list, get the artist and track from the Spotify API
    show_spotify_data = get_artist_track_spotify(show_artist_song, curr_token, show_number)

