from lyricsgenius import Genius
import config

genius = Genius(config.GENIUS_TOKEN)
artist = genius.search_artist("Skor", max_songs=1, sort="title")

song = artist.song("Willkomme in Züri")

print(song.lyrics)
