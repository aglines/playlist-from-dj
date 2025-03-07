import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os, time, json

def make_new_playlist(curr_show):
    load_dotenv()
    curr_token = os.getenv('CURR_TOKEN')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    playlist_name = curr_show
    user_id = sp.me()['id']

    try:
        sp.user_playlist_create(user_id, playlist_name)
    except RuntimeError as err:
        print(f"error trying to create playlist: {err}")
    return playlist_name

def get_playlist_id(playlist_name):
    load_dotenv()
    curr_token = os.getenv('CURR_TOKEN')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
    return playlist_id

def add_tracks_to_playlist(playlist_id, track_ids):
    load_dotenv()
    curr_token = os.getenv('CURR_TOKEN')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    try:
        sp.playlist_add_items(playlist_id, track_ids)
    except RuntimeError as err:
        print(f"error trying to add tracks to playlist: {err}")
    

def main():

    test_playlist_name = '62141'
    playlist_name = make_new_playlist(test_playlist_name)
    playlist_id = get_playlist_id(playlist_name)
    print(playlist_id)

    # get tracklist from JSON file
    with open(f'{test_playlist_name}.json', 'r') as f:
        tracklist = json.load(f)
    tracklist = [track['track_id'] for track in tracklist]
    print(tracklist)

    add_tracks_to_playlist(playlist_id, tracklist)



if __name__ == '__main__':
    main()

