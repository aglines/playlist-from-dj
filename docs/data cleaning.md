# Notes on cleaning data

## The only fields that will prevent the creation of playlists are artist name and song name.  NULLs in other fields are of no concern.
- No NULLs in either artist or song columns
- However, many records have empty strings for these: 11 artists and 542 songs are blank (and only 1 record is blank for both)

## Records where song name is blank
- Context clues help. There is always an artist, if the song is blank (save 1)
- the booelan "is_live" accounts for 66 of these records
- records not marked is_live which still had the artist OR album name include
"live", "Live", or "LIVE", (32, 13, 9) = 54 songs
- or Album was marked "live" (any combo) = 20 songs
- so of 542 songs, 130 songs seemed to be live performances in the studio
- same goes for the word "interview" in artist or album 
- or "compilation" or "V/A" (various artists)
- Release_ID is not null for many of these, which accounts for more
- there are still 226 songs without the clues as above
- 226 of 254,119 song plays in the database is 0.09 percent of the total. very low
- 542 song plays of 254,119 is 0.2 percent
- Conclusion: skip any record without a value in 'song'

## Misspellings of artist names?
- Undesired because Spotify will not be able to find this artist, resulting in songs missing from some playlists.  How to handle these?
- Like names for people, each individual artist has a standard correct spelling for themselves.
- Unlike a database of names of people, we cannot assume that each individual spelling is valid. "Björk" and "Bjork" are probably the same artist.  So we want to find and correct these misspellings.  

# Logic, assumptions, volume
- This will be a one-time process to correct archived data
- Find a method that can automatically handle a large amount of the work, then plan to manually process a smaller amount.
- 13,370 unique artist names
- Of these, 5098 appear one time, 1672 appear two times

# Method
- Assume each artist name that appears once is a misspelling
- For each 1-count artist, use fuzzy matching to see if there is a close match whose count is higher than the 1-count.  List all these and make a judgment about how to proceed.


