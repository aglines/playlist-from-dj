# playlist-from-dj
creates playlists in Spotify, based on music data from a radio station dj

# to do / planned structure

## Create playlists from a subset of the data
- Use song title and artist to find the song on Spotify
- For all the songs in one show, create one playlist

## Analysis
- come up with some research questions, t.ex. what's the most played band by this DJ? do they favor songs from any certain year? live versions or studio recordings? etc

# done
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
