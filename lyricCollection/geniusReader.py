######### IN USE FOR PROJECT: get the lyrics of a song and parse them accordingly


from lyricsgenius import Genius
import config
import re
from lingua import Language, LanguageDetectorBuilder

genius = Genius(config.GENIUS_TOKEN)

languages = [Language.SWAHILI, Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH] # Language.ARABIC (swahili used as replacement)
detector = LanguageDetectorBuilder.from_languages(*languages).build()

# use genius API to get song lyrics
def getLyric(songName, artist, inFrench = False):
    song = genius.search_song(songName, artist)
    # find the song lyrics and parse them
    lyrics = parse(song, songName, artist, inFrench)
    return lyrics

# to parse the lyrics since they can be quite noisy
def parse(song, songName, artist, inFrench):
    # none checking
    if song is None:
        return ""
    # check that it is the right song
    if (songName.lower() not in song.title.lower()) and (artist.lower() not in song.artist.lower()):
        return ""
    # if yes, start doing parsing on the lyrics
    lyrics = song.lyrics
    # genius messages that get in lyrics (might have to finetune)
    unwantedMessages = ["You might also like"]
    for um in unwantedMessages:
        lyrics = lyrics.replace(um, "")
    # all square brackets
    lyrics = remove_square_brackets(lyrics)
    # remove "Embed" 
    lyrics = remove_last_occurrence(lyrics, "Embed")
    # then all the numbers coming before it
    while lyrics[-1].isdigit():
        lyrics = lyrics[:-1]
    # find the first "Lyrics" string and remove that plus everything before it
    lyricsSep = "Lyrics"
    lyrics = lyricsSep.join(lyrics.split(lyricsSep)[1:])

    # only for french
    if inFrench and detector.compute_language_confidence_values(lyrics)[0].language.name != "FRENCH":
        return ""

    return lyrics

# to remove all [] bracekts in the lyrics (from gpt)
def remove_square_brackets(input_string):
    pattern = r"\[.*?\]"  # Matches anything within square brackets
    result_string = re.sub(pattern, "", input_string)
    # also so the ticket message is gone
    pattern = r'See ([^\n]*) LiveGet tickets as low as \$\d+'
    result_string = re.sub(pattern, "", input_string)
    return result_string

# same here, used for the "Embed" occuring at the very end
def remove_last_occurrence(main_string, sub_string):
    last_occurrence_index = main_string.rfind(sub_string)

    if last_occurrence_index != -1:
        # If the substring is found, remove it
        modified_string = main_string[:last_occurrence_index] + main_string[last_occurrence_index + len(sub_string):]
        return modified_string
    else:
        # If the substring is not found, return the original string
        return main_string

if __name__ == "__main__":
    print(getLyric('A lot', '21 savage'))