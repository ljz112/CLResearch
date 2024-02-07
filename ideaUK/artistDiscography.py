# code taken from (and adapted to) https://github.com/spotipy-dev/spotipy/blob/master/examples/artist_discography.py

# however this only applies to albums. maybe later deal with features and/or singles

# Shows the list of all songs sung by the artist or the band
import argparse
import sys

# setting path
sys.path.append('..')
import config

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy


# for now
allTracks = []

# Your Spotify application credentials
client_id = config.SPOTIFY_CLIENT_ID
client_secret = config.SPOTIFY_CLIENT_SECRET

# Create a Spotify object with SpotifyOAuth as the authentication manager
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, 
                    client_secret=client_secret))

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def show_album_tracks(album):
    tracks = []
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    releaseDate = album['release_date']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for i, track in enumerate(tracks):
        allTracks.append({"name": track['name'], "date": releaseDate})


def show_artist_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    unique = set()  # skip duplicate albums
    for album in albums:
        name = album['name'].lower()
        if name not in unique:
            unique.add(name)
            show_album_tracks(album)


def getAllTrackNames(artist):
    artist = get_artist(artist)
    show_artist_albums(artist)
    return allTracks


if __name__ == '__main__':

    # have artist name here
    artist = "Skepta"

    print(getAllTrackNames(artist))