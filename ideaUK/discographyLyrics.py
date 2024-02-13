# so for this idea you need to 
# 1) get the discography of the artist (DONE)
# 2) get the lyrics of the songs of interest
# 3) get the lexical borrowing code on python (STUCK)

import artistDiscography
import json
import sys

# setting path
sys.path.append('../lyricCollection')
from geniusReader import getLyric
from youtubeReader import getYoutubePopularity

artist = "Yuno Miles"

songNames = artistDiscography.getAllTrackNames(artist)

# what data do you need? you need the date, name
allTrackInfo = []

for songName in songNames:
    songInfo = {}
    songInfo['date'] = songName['date']
    songInfo['name'] = songName['name']
    # be careful, you have a quota for using the youtube api
    songInfo['popularity'] = getYoutubePopularity(songName['name'], artist)
    songInfo['lyrics'] = getLyric(songName['name'], artist)
    allTrackInfo.append(songInfo)
    
allInfo = {}
allInfo['artist'] = artist
allInfo['discography'] = allTrackInfo


json_data = json.dumps(allInfo) 
json_file_path = "discographyData/output.json"
with open(json_file_path, "w") as json_file:
    json_file.write(json_data)