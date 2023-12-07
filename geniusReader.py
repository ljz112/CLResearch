from lyricsgenius import Genius
import config

genius = Genius(config.GENIUS_TOKEN)


# use genius API to get song lyrics
def getLyric(songName, artist):
    artist = genius.search_artist(artist, max_songs=1, sort="title")
    song = artist.song(songName)
    # need to parse these lyrics so you know
    return song.lyrics
