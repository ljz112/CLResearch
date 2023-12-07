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

# mundart for swiss rap (sample), rap francais, deutschrap, uk drill/rap

def collectSongs(country, N = 20):
    results = sp.search(q='genre:"' + config.COUNTRY_SETTINGS[country]['genre'] + '"', type='track', limit=N)
    #print(results)

    # Print information about the top 10 tracks
    songNamePlusArtist = []
    for i, track in enumerate(results['tracks']['items']):
        """
        try: 
            rd = track['album']['release_date']
        except Exception as e:
            rd = ""
        """
        songNamePlusArtist.append([track['name'], [artist['name'] for artist in track['artists']], track['album']['release_date'], track['popularity']])
        #print(f"{i + 1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
    return songNamePlusArtist


if __name__ == "__main__":
    print("Usually shouldn't have this called itself but ok")
    print(collectSongs('uk'))