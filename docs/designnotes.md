## Potential roadblock: API rate limits 
- Running into rate limiting upon searching or creating playlist w artist/track info
- unable to find clear info about the limits, only anecdata. How to get around this?

### Solution: don't repeat the same request
- One way could be to not repeat anything for the same artist / track
- Spotify Web API offers: Get Artist's Albums, and Get Album Tracks
- Use this DJ's favorite artists to cache data ahead of time
- so that creating the playlists uses fewer network calls

