import config
import spotifyReader
import musicBrainzReader
import processOrigin
import geniusReader

# defaults for every thing
songTable = []
artistTable = []
artistIdMap = {}
countries = list(config.COUNTRY_SETTINGS.keys())
N = 20

# use NLP strategies
def parseBackground(query, language):
    try: 
        queryOrigin = processOrigin.getAllRoots(query, language)
        return queryOrigin
    except Exception as e:
        print(f"Wasn't able to get ethnic background: {e}")
        return []

# get the birth date + place of origin of artist
def getBasicDetails(artist):
    try: 
        details = musicBrainzReader.getOriginDetails(artist)
        return details
    except Exception as e:
        print(f"Couldn't get origin details: {e}")
        return ['','']


# add a new artist + all fields to 
def addArtist(artist, country):
    # first need to check if artist alr exists in the table
    alrHere = any((d['name'] == artist and d['country'] == country) for d in artistTable)
    if alrHere:
        # artist info has alr been recorded
        return
    toAdd = {}
    # basic fields
    artistId = len(artistTable)
    artistIdMap[country][artist] = artistId
    toAdd['id'] = artistId
    toAdd['name'] = artist
    toAdd['country'] = country
    # fields from musicBrainz
    bDate, bArea = getBasicDetails(artist)
    toAdd['birthDate'] = bDate
    toAdd['birthArea'] = bArea
    # fields from wiki
    lang = config.COUNTRY_SETTINGS[country]['lang']
    toAdd['background'] = parseBackground(artist, lang)
    # then add to the table
    artistTable.append(toAdd)


def getArtistList(artists, country):
    return [artistIdMap[country][a] for a in artists]

# get lyrics through Genius API
def getLyrics(songName, artists):
    # assuming only 1 artist works
    for artist in artists:
        try: 
            lyrics = geniusReader.getLyric(songName, artist)
        except Exception as e:
            lyrics = ''
          
        if lyrics != '':
            return lyrics

    print("Couldn't get lyrics for song " + songName)
    return ''



# now time to add songs to the table
def addSong(songName, artists, country, releaseDate, popularity):
    # first need to get the artists into an id list
    artistList = getArtistList(artists, country)
    # also need a function to determine if all the elements are in the same list 
    alrHere = any((d['name'] == songName and set(d['artists']) == set(artistList) and d['country'] == country) for d in songTable)
    if alrHere:
        # song info has been here once
        return
    toAdd = {}
    # basic fields 
    songId = len(songTable)
    toAdd['id'] = songId
    toAdd['name'] = songName
    toAdd['artists'] = artistList
    toAdd['country'] = country
    toAdd['releaseDate'] = releaseDate
    toAdd['popularity'] = popularity
    # lyrics
    toAdd['lyrics'] = getLyrics(songName, artists)
    songTable.append(toAdd)

# main code that runs to get songTable and artistTable filled up
if __name__ == "__main__":
    # this example is only with switzerland (and only looking at a set of songs assuming I want to branch out recursively)
    countries = list(config.COUNTRY_SETTINGS.keys())
    for country in countries:
        # some data things 
        artistIdMap[country] = {}
        # first get the songs from the spotify playlist
        songArtistPairs = spotifyReader.collectSongs(country, N)
        print(songArtistPairs)
        for sap in songArtistPairs:
            songName = sap[0]
            artists = sap[1]
            releaseDate = sap[2]
            popularity = sap[3]
            # first look at artists: check for membership then get all fields
            for a in artists:
                addArtist(a, country)
            # the look at/get info about songs
            addSong(songName, artists, country, releaseDate, popularity)

    print("SONG TABLE:")
    print(songTable)
    print("ARTIST TABLE:")
    print(artistTable)
