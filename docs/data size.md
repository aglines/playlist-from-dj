# Notes about data volume

# Total estimated file storage needed if I capture all data?
- one 20-record file is 28k bytes > multiplied by 132,500 pages of API
- the data alone, IF i get all data per record, wd be 3.5G
- if PostgreSQL, add 20-30% overhead and the db file wd be 4.5G or so

# But I don't seem to need every column in each row. What data isn't relevant to my needs?

- image url and thumbnail url
- URI and ID functionally contain the same data, so only keep ID it's shorter
    - same with show and show URI, only keep the show ID
- TrackID and recordingID, unsure but these might link to some external source
    - recordingID would separate which recording this was in case I am interested later
    - Yes, retrieve these
- airbreak? I don't currently see value in doing analysis of how many seconds the station plays songs as opposed to breaks from songs. Do not store this

# Decision:  the extra data doesn't add so much.  Just retrieve all the data

# Reality:  processing in chunks
- chunk size 5000 yielded 2 files for one year, total size 10.4M
