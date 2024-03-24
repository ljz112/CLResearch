import json
from lingua import Language, LanguageDetectorBuilder

def find_duplicates(arr):
    seen = {}
    unique = []

    for item in arr:
        if item['lyrics'] not in seen:
            seen[item['lyrics']] = True
            unique.append(item)

    # 7262 entries
    return unique

# open the json
languages = [Language.SWAHILI, Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.ITALIAN, Language.SPANISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

with open('../dataEntries/frenchDataNew.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)
# filter to french speaking ones only (7371/9497 songs)
dataOfInterest = [d for d in data['allSongs'] if ((d['lyrics'].replace('\n', '').strip() != "") and (detector.compute_language_confidence_values(d['lyrics'])[0].language.name == "FRENCH"))]
result = find_duplicates(dataOfInterest)

print(len(result))