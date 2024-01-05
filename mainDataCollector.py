import config
import spotifyReader
import musicBrainzReader
import processOrigin
import geniusReader
import json

# defaults for every thing
songTable = []
artistTable = []
artistIdMap = {}
countries = list(config.COUNTRY_SETTINGS.keys())
searchSize = 25       # max 50
searchDepth = 3

# use NLP strategies
def parseBackground(query, language):
    # for now -- want to make this diff prolly
    return []
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
    # toAdd['background'] = parseBackground(artist, lang)
    # then add to the table
    artistTable.append(toAdd)


def getArtistList(artists, country):
    return [artistIdMap[country][a] for a in artists]

# get lyrics through Genius API
def getLyrics(songName, artists):
    # should make conjoined artist title

    # artistQuery = artists[0] + " feat. " + ", ".join(artists[1:])

    try: 
        lyrics = geniusReader.getLyric(songName, artists[0])
    except Exception as e:
        print(e)
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
    print("SONG NUMBER " + str(songId + 1))
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
    # should prolly do only one country at a time though then combine at the end (TODO uk)
    for country in countries:
        country = 'uk'
        if country == 'ukp2':
            continue
        # some data things 
        artistIdMap[country] = {}
        # first get the songs from the spotify playlist
        print(f"STATS BEFORE: {country}, {searchSize}, {searchDepth}")
        songArtistPairs = spotifyReader.collectMostSongs(country, searchSize, searchDepth)
        print(f"ALL COLLECTED SONGS: {len(songArtistPairs)}")
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
        break

    # convert all collected data to a json and create that json file
    json_data = json.dumps({'allSongs': songTable, 'allArtists': artistTable}) 
    json_file_path = "dataEntries/output.json"
    with open(json_file_path, "w") as json_file:
        json_file.write(json_data)

    print("JSON data written, data collection finished")
