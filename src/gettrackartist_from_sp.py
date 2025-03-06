import requests, os, json, time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
from getdata_show import process_current_show

def get_artist_track_spotify(show_artist_song, curr_token, curr_show):
    '''Get the artist and track from Spotify API'''

    # Check the database to see if the data for this show already exists

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
    return results



def main():
    load_dotenv()
    curr_token = os.getenv('CURR_TOKEN')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')
    scope = 'playlist-modify-public'

    # for one entire show, get list of artist name and song name from db
    curr_show = 37547

    # Get a list of artists and songs for the show
    show_artist_song = process_current_show(curr_show)
    print('got show data from db')

    # For each song in the list, get the artist and track from the Spotify API
    show_spotify_data = get_artist_track_spotify(show_artist_song, curr_token, curr_show)
    print('got Spotify data for all artists and tracks in show list')


if __name__ == '__main__':
    main()
