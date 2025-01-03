import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
from getdata_show import process_current_show

def search_artist_track_spotify(show_artist_song):

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
    return data

def get_artist_track_spotify(show_artist_song, curr_token):

    endpoint = 'https://api.spotify.com/v1/search'

    # replace spaces in each element of the list
    show_artist_song = [[i.replace(' ', '%20') for i in x] for x in show_artist_song]

    # Get track ID and artist ID for each song in the list
    for artist, track in show_artist_song:
        query = f'{endpoint}'
        query += f'?q=track%3A{track}%20artist%3A{artist}&type=track&limit=1'
        response = requests.get(query, headers={
            'Content-Type': 'application/json',
            'Authorization':f'Bearer {curr_token}'})
        if response.status_code != 200:
            print(f'Error: {response.status_code}, body of error: {response.json()}')
            return None
        data = response.json()
        if not data['tracks']['items']:
            print(f'Skipping: Artist "{artist.replace("%20", " ")}" and Track "{track.replace("%20", " ")}" not found.')
            continue
        # get relevant data 
        track_id = data['tracks']['items'][0]['id']
        track_name = data['tracks']['items'][0]['name']
        artist_id = data['tracks']['items'][0]['artists'][0]['id']
        artist_name = data['tracks']['items'][0]['artists'][0]['name']
        print(f'Artist: {artist_name}, Track: {track_name}')


def main():
    load_dotenv()
    curr_token = os.getenv('CURR_TOKEN')

    # for one entire show, get list of artist name and song name from db
    # Pick one show at random
    curr_show = 37547

    # Get a list of artists and songs for the show
    show_artist_song = process_current_show(curr_show)
    # print(show_artist_song)

    # For each song in the list, get the artist and track from the Spotify API
    get_artist_track_spotify(show_artist_song, curr_token)


if __name__ == '__main__':
    main()


