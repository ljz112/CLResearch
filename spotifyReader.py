import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config


# Your Spotify application credentials
client_id = config.SPOTIFY_CLIENT_ID
client_secret = config.SPOTIFY_CLIENT_SECRET

# Define the scope of permissions your application needs
scope = "user-library-read"

# Create a Spotify object with SpotifyOAuth as the authentication manager
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, 
                    client_secret=client_secret))

# proposed spotify api strategy (may be better than youtube tbh) 
# 1) find N most popular rap songs of a certain genre: rap of certain country
# 2) outta each name, branch out and find the songs of that corpus, branching even more for features (assuming it still aligns with the genre)

# just to keep what I already have
def collectSongs(country, N = 50):
    return collectSongsGenre(country, N)

# get the N songs that first come up with the genre
def collectSongsGenre(country, N):
    results = sp.search(q='genre:"' + config.COUNTRY_SETTINGS[country]['genre'] + '"', type='track', limit=N)

    # Print information about the top 10 tracks
    songNamePlusArtist = []
    for i, track in enumerate(results['tracks']['items']):
        songNamePlusArtist.append(getFeatures(track))
    return songNamePlusArtist

# so I can get all the features of a track that I want
def getFeatures(track):
    return [track['name'], [artist['name'] for artist in track['artists']], track['album']['release_date'], track['popularity']]

# remove dupes from the data, using normal python method of set to list
def mergeResults(data1, data2):
    ARTIST_SEP = "\t"
    ELEMENT_SEP = "\n"

    # convert list from str
    def encode(data):
        newList = []

        for d in data:
            temp = d
            temp[1] = ARTIST_SEP.join(d[1])
            temp[3] = str(temp[3])
            temp = ELEMENT_SEP.join(temp)
            newList.append(temp)

        return newList

    # then from str to list
    def decode(data):
        origList = []

        for d in data:
            temp = d.split(ELEMENT_SEP)
            temp[1] = temp[1].split(ARTIST_SEP)
            temp[3] = int(temp[3])
            origList.append(temp)

        return origList

    return decode(list(set(encode(data1) + encode(data2))))

# get the discography of an artist (spotify API called)
def getDiscography(artist, country, N):
    # search for genre and artist (get right discography and genre)
    results = sp.search(q='genre:"' + config.COUNTRY_SETTINGS[country]['genre'] + '" ' + 'artist:"' + artist + '"', type='track', limit=N)

    discography = []
    for i, track in enumerate(results['tracks']['items']):
        discography.append(getFeatures(track))

    return discography

# find the artists in a group look exclusively for them
def branchOut(country, N, depth, baseData, searchedArtists = []):
    # depth limit reached
    if depth == 0:
        return baseData
    
    # otherwise look at every artist in baseData and for each one (that you haven't done yet) do a spotify API call then a recursive call (merge)
    allData = baseData
    for b in baseData:
        for artist in b[1]:
            # only if we've already searched this artist
            if artist not in searchedArtists:
                # search for genre and artist (get right discography and genre)
                discography = getDiscography(artist, country, N)
                if country == 'uk':
                    discography = mergeResults(discography, getDiscography(artist, 'ukp2', N))

                searchedArtists.append(artist)
                # merge all data together with this discography (and all the extra searching needed)
                allData = mergeResults(allData, branchOut(country, N, depth - 1, discography, searchedArtists))

    return allData

# if you actually wanna get many songs to form a corpus
def collectMostSongs(country, N = 50, depth = 3):

    # step 1: get songs from a genre to form base data
    baseData = collectSongsGenre(country, N)
    # what I should do if there are multiple genres
    if country == 'uk':
        baseData = mergeResults(baseData, collectSongsGenre('ukp2', N))

    # step 2: go thru songs then add new things from them (do this recursively with a given depth)
    allData = branchOut(country, N, depth, baseData)

    return allData

if __name__ == "__main__":
    print("Usually shouldn't have this called itself but ok")
    # should text this: the popular drill things aren't showing (eg doja, welcome to brixton)
    # also idk why but the number of returned things substantially decreases the more you do this 
    mostSongs = collectMostSongs('uk')
    print(mostSongs)
    print(len(mostSongs))