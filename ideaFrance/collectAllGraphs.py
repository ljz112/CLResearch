############ IN USE FOR PROJECT



import json
from lingua import Language, LanguageDetectorBuilder
from slangTimeDistrib import getWordUsePlot
from embeddingsPlayground import getWords

# open the json
languages = [Language.SWAHILI, Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.ITALIAN, Language.SPANISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()
print("Opening collected songs")

# collect the data
with open('../dataEntries/frenchDataNew.json', 'r') as file:
    data = json.load(file)['allSongs']

with open('../dataEntries/frenchDataOldSongs.json', 'r') as file:
    data2 = json.load(file)['allSongs']

data += data2
# filter to french speaking ones only (7262/9497 songs)
startData = [d for d in data if ((d['lyrics'].replace('\n', '').strip() != "") and (detector.compute_language_confidence_values(d['lyrics'])[0].language.name == "FRENCH"))]

# remove duplicates
seen = {}
dataOfInterest = []
for item in startData:
    if item['lyrics'] not in seen:
        seen[item['lyrics']] = True
        dataOfInterest.append(item)

# open the slang words
print("Collecting words")
words = getWords()


mode = "freq"
dateModes = ["year", "month"]
allGraphs = {}

for dateMode in dateModes:
    allGraphs[dateMode] = {}

for w in words:
    print(w)
    for dateMode in dateModes:
        allGraphs[dateMode][w] = getWordUsePlot(w, mode, dataOfInterest, dateMode)
print("All graphs collected")

json_data = json.dumps(allGraphs) 
json_file_path = "collectedData/allGraphsNew.json"
with open(json_file_path, "w") as json_file:
    json_file.write(json_data)
print("All graphs uploaded to json file")