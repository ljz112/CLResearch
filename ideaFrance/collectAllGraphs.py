import json
from lingua import Language, LanguageDetectorBuilder
from slangTimeDistrib import getWordUsePlot
from embeddingsPlayground import getWords

# open the json
languages = [Language.SWAHILI, Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.ITALIAN, Language.SPANISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()
print("Opening collected songs")

with open('../dataEntries/frenchDataNew.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)
# filter to french speaking ones only (7371/9497 songs)
dataOfInterest = [d for d in data['allSongs'] if ((d['lyrics'].replace('\n', '').strip() != "") and (detector.compute_language_confidence_values(d['lyrics'])[0].language.name == "FRENCH"))]
print("Filtered collected songs")

# open the slang words
words = getWords()
print("Collected words")

allGraphs = {}
for w in words:
    print(w)
    allGraphs[w] = getWordUsePlot(w, "freq", dataOfInterest)
print("All graphs collected")

json_data = json.dumps(allGraphs) 
json_file_path = "collectedData/allGraphs.json"
with open(json_file_path, "w") as json_file:
    json_file.write(json_data)
print("All graphs uploaded to json file")