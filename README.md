# playlist-from-dj
creates playlists in Spotify, based on music data from a radio station dj

## To run
- First, run create_archive_gethost.py one time, to get the host ID from the radio station API, given the known time slots when the DJ hosts a show. TODO: explain required env vars

- Run create_archive_getsongs.py given the known host_id. Hardcoded host_id and airdate_after and airdate_before datetimes, in order to retrieve all historical song data and cache locally as json.  Retrieved in chunks based on airdate.  Historical data is limited, so the oldest dates drop off, therefore I wanted to save the raw API response ASAP and process it later.

- To do further processing, write the cached json to a local db by running create_archive_writejson_todb.py.  This stores the raw API response in postgres.

- TODO: modify getshow_from_dj.py, so that user can enter a date at cl, and a playlist will be created from that date. 
    - Build a lookup table to make this quicker: show_date (done)
    




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


