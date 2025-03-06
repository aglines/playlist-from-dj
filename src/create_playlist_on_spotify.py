import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
import os
import time
from getdata_show import process_current_show
import json

def get_artist_track_spotify(show_artist_song, curr_token, curr_show):
    '''Get the artist and track from Spotify API'''
    # Check if the JSON file for the current show already exists
    if os.path.exists(f'{curr_show}.json'):
        print(f"Data for {curr_show} already exists. Reading from file.")
        with open(f'{curr_show}.json', 'r') as f:
            results = json.load(f)
        return results

    endpoint = 'https://api.spotify.com/v1/search'

    # replace spaces in each element of the list
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
        time.sleep(0.3)

    # Save results to a JSON file
    with open(f'{curr_show}.json', 'w') as f:
        json.dump(results, f, indent=4)

    return results


def make_new_playlist(curr_show, client_id, client_secret, redirect_uri, scope):
    '''Creates a new playlist, whose name is the show number'''
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope))

    playlist_name = curr_show
    user_id = sp.me()['id']

    # Check if the playlist already exists
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            print(f"Playlist {playlist_name} already exists.")
            return playlist['id']

    # If the playlist does not exist, create a new one
    try:
        sp.user_playlist_create(user_id, playlist_name)
    except spotipy.exceptions.SpotifyException as err:
        print(f"Error trying to create playlist: {err}")
        print(f"Response headers: {err.headers}")
        print(f"Response body: {err.msg}")
        return None

    # Add a delay to avoid rate limiting
    time.sleep(1)

    # Get the new playlist ID
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            new_playlist_id = playlist['id']
            break
    return new_playlist_id

def add_songs_to_playlist(show_spotify_data, new_playlist_id, client_id, client_secret, redirect_uri, scope):
    '''Adds songs to a playlist'''
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope))
    
    track_ids = [x['id'] for x in show_spotify_data['tracks']['items']]
    try:
        sp.playlist_add_items(new_playlist_id, track_ids)
    except spotipy.exceptions.SpotifyException as err:
        print(f"Error trying to create playlist: {err}")
        print(f"Response body: {err.msg}")
    return None

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

    # Create a new playlist, get the playlist ID
    new_playlist_id = make_new_playlist(curr_show, client_id, client_secret, redirect_uri, scope)
    # print(f'created playlist {curr_show}')

    # Add song to the new playlist
    # add_songs_to_playlist(show_spotify_data, new_playlist_id, client_id, client_secret, redirect_uri, scope)
    # print('added songs to playlist')


if __name__ == '__main__':
    main()
