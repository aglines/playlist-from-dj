import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
import os
import time
# from getdata_show import process_current_show
import json

def get_artist_track_spotify(show_artist_song, curr_token):
    endpoint = 'https://api.spotify.com/v1/search'
    # replace spaces with the encoded version
    show_artist_song = [[i.replace(' ', '%20') for i in x]
                        for x in show_artist_song]
    results = []

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
        duration = data['tracks']['items'][0]['duration_ms']
        explicit = data['tracks']['items'][0]['explicit']
        track_popularity = data['tracks']['items'][0]['popularity']
        available_markets = data['tracks']['items'][0]['available_markets']
        album_id = data['tracks']['items'][0]['album']['id']
        album_name = data['tracks']['items'][0]['album']['name']
        album_release_date = data['tracks']['items'][0]['album']['release_date']
        album_release_date_precision = data['tracks']['items'][0]['album']['release_date_precision']
        album_total_tracks = data['tracks']['items'][0]['album']['total_tracks']


        results.append({
            'artist_name': artist_name,
            'artist_id': artist_id,
            'track_name': track_name,
            'track_id': track_id,
            'duration': duration,
            'explicit': explicit,
            'track_popularity': track_popularity,
            'available_markets': available_markets,
            'album_id': album_id,
            'album_name': album_name,
            'album_release_date': album_release_date,
            'album_release_date_precision': album_release_date_precision,
            'album_total_tracks': album_total_tracks
        })
    return results


def main():
    load_dotenv()
    curr_token = os.getenv('CURR_TOKEN')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')

    # Get a list of artists and songs for the show
    show_artist_song = [('Pixies', 'Dead'), ("The B-52's", 'Devil in My Car'), ('The Animals', 'House of the Rising Sun'), ('The Clash', 'Straight to Hell')]
    print(show_artist_song)

    # For each song in the list, get the artist and track from the Spotify API
    show_spotify_data = get_artist_track_spotify(show_artist_song, curr_token)
    print(show_spotify_data)


if __name__ == '__main__':
    main()
