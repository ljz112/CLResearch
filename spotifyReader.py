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
        return [baseData, searchedArtists]
    
    # otherwise look at every artist in baseData and for each one (that you haven't done yet) do a spotify API call then a recursive call (merge)
    allData = baseData
    # add the searched artists and remove dupes after (NO NOT REALLY)

    # steps for searched artists
    # 1) find all the artists in the baseData
    # 2) search through them if they're not in searchedArtists already
    # 3) update searchedArtists based on what the recursive calls have searched
    
    # find all the artists in the baseData
    artistsInData = []
    for b in baseData:
        for artist in b[1]:
            artistsInData.append(artist)
    artistsInData = list(set(artistsInData))

    # now go through searched artists to get the discographies
    for artist in artistsInData:
        if artist not in searchedArtists:
            # search for genre and artist (get right discography and genre)
            discography = getDiscography(artist, country, N)
            if country == 'uk':
                discography = mergeResults(discography, getDiscography(artist, 'ukp2', N))

            searchedArtists.append(artist)
            # get branched out data plus new list of searched artists
            branchedData, searchedArtists = branchOut(country, N, depth - 1, discography, searchedArtists)
            # merge all data together with this discography
            allData = mergeResults(allData, branchedData)
            searchedArtists = list(set(searchedArtists))

    return [allData, searchedArtists]

# if you actually wanna get many songs to form a corpus
def collectMostSongs(country, N = 50, depth = 3):

    # step 1: get songs from a genre to form base data
    baseData = collectSongsGenre(country, N)
    # what I should do if there are multiple genres
    if country == 'uk':
        baseData = mergeResults(baseData, collectSongsGenre('ukp2', N))

    # step 2: go thru songs then add new things from them (do this recursively with a given depth)
    allData, otherVar = branchOut(country, N, depth, baseData)

    return allData

# removes multiple releases of the same song 
def removeMultipleReleases(data):
    # to keep the duplicate winners in this list
    revised_elements = []
    ind = 0
    while ind < len(data):
        song = data[ind]
        # find all indexes where 1st and 2nd element is the same
        indexes = [i for i in range(len(data)) if (data[i][0] == song[0] and data[i][1] == song[1])]
        if len(indexes) == 1:
            ind += 1
            continue
        # get these elements
        dupeElements = [data[i] for i in indexes]
        # add the most popular thing to the revised elements (deciding to do this since spotify's popularity metric is 1-100)
        maxDupe = max(dupeElements, key=lambda x: x[3])
        revised_elements.append(maxDupe)
        # and remove all the dupe values from the main data
        indexes = sorted(indexes, reverse = True)
        for i in indexes:
            data.pop(i)

    data += revised_elements
    return data
        

if __name__ == "__main__":
    print("Usually shouldn't have this called itself but ok")
    # problem 0: have to get all of these results at the end of mainData into a json where everything can be stored (might have to take less popular away if too much storage)
    # problem 1: not doing spotify queries correctly with genre (need array and no ukp2?, but I'm close enough) and artists (need id) (data management problem)
    mostSongs = collectMostSongs('fr', 50, 3)
    mostSongs = removeMultipleReleases(mostSongs)
    print(mostSongs)
    print(len(mostSongs))
    # print(getDiscography("Skepta", "ukp3", 50))