import langdetect
import json
import nltk
import re

nltk.download('punkt')
MAINLANG = "de"

def getDetectedLang(distrib):
    return str(distrib[0]).split(':')[0]

def onlyPunctuation(input_string):
    punctuation_pattern = re.compile(r'^[^\w\s\d]$')
    match = punctuation_pattern.search(input_string)
    return bool(match)


def langDetectStats(text):
    # get overall stats
    distrib = langdetect.detect_langs(text)
    print("OVERALL DISTRIB")
    print(distrib)
    # sep by \n
    lines = text.split('\n')
    print("LINES NOW")
    for l in lines:
        if l != "":
            distrib = langdetect.detect_langs(l)
            if getDetectedLang(distrib) != "fr" or len(distrib) != 1:
                print(l)
                print(distrib)
                # go word level here
                tokens = nltk.word_tokenize(l)
                print("KEY WORDS")
                for t in tokens:
                    if not (onlyPunctuation(t) or t.isdigit()):
                        distrib = langdetect.detect_langs(t)
                        if getDetectedLang(distrib) != "fr" or len(distrib) != 1:
                            print(t)
                            print(distrib)


                
            



with open('../dataEntries/swissData.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)

dataOfInterest = [d for d in data['allSongs'] if d['lyrics'] != ""]
print(f"Number of songs: {len(dataOfInterest)}")

firstVal = dataOfInterest[52]
lyricstoExamine = firstVal['lyrics']

print("First text")
print(firstVal)
print(lyricstoExamine)

if lyricstoExamine != "":
    langDetectStats(lyricstoExamine)