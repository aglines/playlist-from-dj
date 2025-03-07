import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os, time, json, sys
from get_spotify_ids import get_artist_track_spotify
from get_showsongs_fromdb import pick_show_date, process_current_show


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

    playlist_name = make_new_playlist(show_number)
    playlist_id = get_playlist_id(playlist_name)
    print(playlist_id)

    # get tracklist from JSON file
    with open(f'{show_number}.json', 'r') as f:
        tracklist = json.load(f)
    tracklist = [track['track_id'] for track in tracklist]
    print(tracklist)

    add_tracks_to_playlist(playlist_id, tracklist)

