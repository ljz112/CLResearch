############ IN USE FOR PROJECT: collect the frequency over time graph for each collected borrowing (month and year granularity)

import json

from slangTimeDistrib import getWordUsePlot
from embeddingsPlayground import getWords
from open_files import getDataOfInterest, getArtists


if __name__ == "__main__":
    print("Opening collected songs")
    dataOfInterest = getDataOfInterest()
    artistData = getArtists()

    # open the slang words
    print("Collecting words")
    words = getWords()


    mode = "artist_num" # "song_num" # "freq" # what specifically you want the output of the graphs to be
    dateModes = ['year'] # ["year", "month"]
    allGraphs = {}

    for dateMode in dateModes:
        allGraphs[dateMode] = {}

    for w in words:
        print(w)
        for dateMode in dateModes:
            allGraphs[dateMode][w] = getWordUsePlot(w, mode=mode, dataOfInterest=dataOfInterest, dateMode=dateMode, artistData=artistData)
    print("All graphs collected")

    json_data = json.dumps(allGraphs) 
    json_file_path = "collectedData/allGraphsArtistCount.json"
    with open(json_file_path, "w") as json_file:
        json_file.write(json_data)
    print("All graphs uploaded to json file")