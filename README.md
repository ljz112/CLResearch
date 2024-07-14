# About

  

This repository contains code and data for the 2024 ACL-SRW paper "A Computational Analysis and Exploration of Linguistic Borrowings in French Rap Lyrics" by Lucas Zurbuchen and Rob Voigt.

  

## Configuration

  

In order to access the [Spotify](https://developer.spotify.com/documentation/web-api) and [Genius](https://docs.genius.com/#/getting-started-h1) APIs, obtain the necessary information and put into the `GENIUS_TOKEN`, `SPOTIFY_CLIENT_ID`,  and `SPOTIFY_CLIENT_SECRET`  fields in `config.py` while also installing `lyricsgenius` and `spotipy` on pip. 

The [MusicBrainz](https://musicbrainz.org/doc/MusicBrainz_API) API offers useful information on the birthplaces and birth dates of artists -- enter the necessary information into the `EMAIL` field in `config.py` while also installing `musicbrainzngs` on pip in order to use.
  

## Corpus and Wordlists

  

For open-source use, access 		`frenchDataNew.json` and `frenchDataOldSongs.json` in `dataEntries` to view songs after and before 2015. `ideaFrance` offers `getDataOfInterest()` and `getArtists()` in `open_files.py` to merge the list of songs and artists.

In `ideaFrance`, view `collectedData` for `borrowedWords.csv` and `borrowedWordsLangKey.csv` for information on the borrowed words examined. 
  

## How to Run

  
To gather information on French rap songs like in `dataEntries`, run `python  lyricCollection/mainDataCollector.py`. 

To obtain information about the usage of all collected borrowed words, run `python  ideaFrance/collectAllGraphs.py`. 

Lastly, `quickPlot.py` will output a matplotlib plot of any word's usage over time in the corpus. 
  

## Contact

  

If you have any questions, feel free to reach out at lucaszurbuchen2024@u.northwestern.edu.