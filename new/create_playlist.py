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


def main():

    # Create playlist with random name
    test_playlist_name = '11111'
    playlist_name = make_new_playlist(test_playlist_name)
    playlist_id = get_playlist_id(playlist_name)
    print(playlist_id)



if __name__ == '__main__':
    main()

