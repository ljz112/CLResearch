######### IN USE FOR PROJECT: open the borrowed words, get list of artists ids, and get list of all songs (so you don't have to rewrite it constantly)



import json
import csv
from lingua import Language, LanguageDetectorBuilder

# open the json
languages = [Language.SWAHILI, Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.ITALIAN, Language.SPANISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

# for opening collected corpus
def getDataOfInterest():
    # collect the data
    with open('../dataEntries/frenchDataNew.json', 'r') as file:
        data = json.load(file)
        artistLen = len(data['allArtists'])
        data = data['allSongs']

    with open('../dataEntries/frenchDataOldSongs.json', 'r') as file:
        data2 = json.load(file)['allSongs']
        for d2 in data2:
            # to properly reference all artists
            d2['artists'] = [d + artistLen for d in d2['artists']]
    
    data += data2
    # filter to french speaking ones only (8222 songs)
    startData = [d for d in data if ((d['lyrics'].replace('\n', '').strip() != "") and (detector.compute_language_confidence_values(d['lyrics'])[0].language.name == "FRENCH"))]

    # remove duplicates
    seen = {}
    dataOfInterest = []
    for item in startData:
        if item['lyrics'] not in seen:
            seen[item['lyrics']] = True
            dataOfInterest.append(item)
    return dataOfInterest

# for openining borrowed words
def getWords(getRaw = False):
    # generate the words in a csv file
    csv_file_path = 'collectedData/borrowedWords.csv'
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
        wordData = list(csv.reader(file))

    # just for visualizations
    if getRaw:
        return wordData

    # could add condition if " " not in wd[0]
    words = [wd[0].strip().lower() for wd in wordData[1:]]
    return words

def getArtists():
    # collect the data 
    with open('../dataEntries/frenchDataNew.json', 'r') as file:
        data = json.load(file)['allArtists']

    with open('../dataEntries/frenchDataOldSongs.json', 'r') as file:
        data2 = json.load(file)['allArtists']
    
    data += data2

    # add a mapper for duplicate entries?
    seen = {}
    dupeMapper = [-1] * len(data)
    i = 0
    for item in data:
        if item['name'] not in seen:
            seen[item['name']] = i
            dupeMapper[i] = i
        else:
            dupeMapper[i] = seen[item['name']]
        i += 1
    return data, dupeMapper
