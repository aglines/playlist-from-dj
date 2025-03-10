import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os, time, json, sys
from datetime import datetime
from get_spotify_ids import get_artist_track_spotify
from get_showsongs_fromdb import pick_show_date, process_current_show

def get_spotify_client():
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')
    scope = 'playlist-modify-public'
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

def make_new_playlist(sp, curr_show):
    playlist_name = curr_show
    user_id = sp.me()['id']
    try:
        sp.user_playlist_create(user_id, playlist_name)
    except RuntimeError as err:
        print(f"error trying to create playlist: {err}")
    return playlist_name

def get_playlist_id(sp, playlist_name):
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            return playlist['id']
    return None

def add_tracks_to_playlist(sp, playlist_id, track_ids):
    try:
        sp.playlist_add_items(playlist_id, track_ids)
    except RuntimeError as err:
        print(f"error trying to add tracks to playlist: {err}")

if __name__ == '__main__':
    load_dotenv()
    sp = get_spotify_client()
    curr_token = os.getenv('CURR_TOKEN')
        
    # User supplies a date for a single show at the command line in ISO format
    show_date = sys.argv[1]
    try:
        datetime.fromisoformat(show_date)
    except ValueError:
        print("Error: Date is not in ISO format (YYYY-MM-DD)")
        sys.exit(1)

    # Given a valid date, find a show number for that date, which we need to get artists / songs
    show_number = pick_show_date(show_date)
    if show_number is None:
        print("Error: No show found for the given date")
        sys.exit(1)
    
    # Get the artist and song for the show, from file get_songs_fromshow.py
    show_artist_song = process_current_show(show_number)

    # Playlist API requires a track ID, not just artist and track name
    show_spotify_data = get_artist_track_spotify(show_artist_song, curr_token, show_number)

    # TODO: handle the stringification of the show number earlier in the process

    playlist_name = make_new_playlist(sp, f'{show_number}')
    if playlist_name:
        playlist_id = get_playlist_id(sp, playlist_name)

        # used cached JSON to avoid API calls
        with open(f'{show_number}.json', 'r') as f:
            tracklist = json.load(f)
        tracklist = [track['track_id'] for track in tracklist]

        add_tracks_to_playlist(sp, playlist_id, tracklist)
    else:
        print("Failed to create playlist. Exiting.")
        sys.exit(1)

    print(f"Playlist {playlist_name} created successfully.") 


