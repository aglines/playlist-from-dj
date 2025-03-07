# playlist-from-dj
This code gets song play data from a particular radio station DJ, then creates a playlist in Spotify based on the songs they played

## To run
### Create the archive of song play data
- Run utils/create_archive_gethost.py one time, to get the host ID from the radio station API, given the known time slots when the DJ hosts a show. 

- Run create_archive_getsongs.py. This Beam pipeline grabs historical song data via the radio station API, from the current date back to an arbitrarily set date (2000-01-01, since the station archive only goes back 25 years.)  Because the oldest dates drop off, I chose to save the raw API response ASAP. This data gets cached locally as json.

- Run create_archive_writejson_todb.py.  This code reads the cached json and writes it to a Postgres db.

### Create a playlist in Spotify based on a given date

- Run utils/request_spot_token.py to refresh the auth token

- Run get_spotify_ids.py with an ISO formatted date (2024-12-20) to get the list of songs and artists for a particular day's show.  This will cache Spotify IDs to json. This potentially sidesteps rate limit difficulties in using Spotify's API.  (The future intent is to annotate the archive db to avoid repeat lookups.)

- Run create_playlist.py











# to do / planned structure

## Roadblock: API rate limits 
- Running into rate limiting upon searching or creating playlist w artist/track info
- unable to find clear info about the limits, only anecdata. How to get around this?

### Solution: don't repeat the same request
- One way could be to not repeat anything for the same artist / track
- Spotify Web API offers: Get Artist's Albums, and Get Album Tracks
- Use this DJ's favorite artists to cache data ahead of time
- so that creating the playlists uses fewer network calls

# -------------------------------------------------

## Create playlists from a subset of the data
- write spotify track and artist data to db
- For all the songs in one show, create one playlist

## Analysis
- start research questions, t.ex. most played band by this DJ? do they favor songs from any years, genres? live versions or studio recordings? etc

# done
- check for NULLS, missing data, etc
- missing data mostly explained by context (see data cleaning.md)
- Spotify handles malformed queries pretty well, for the purposes of this project
- Decision: apart from missing data, it is not worth it to do much more cleaning, since the stakes are low here
- use song title and artist to find the song on Spotify
- refactor to include .env file
- select data subset for one value of show from db
- write local JSON to a db for later analysis
    - incl all fields for now
- desired dataset completely retrieved, stored locally in json
- add a delay between requests to not overtax the resource
- get song play data, given hostID
- retrieve data in JSON for now & just store locally in chunks
- find the host_id for a given DJ. I know the DJ name and timeslot, but not their ID in the API
- write config details to private_data.py, add to git ignore
- create playlist app in Spotify, get config details

# wish list
- estimate db final size prior to starting retrieval


