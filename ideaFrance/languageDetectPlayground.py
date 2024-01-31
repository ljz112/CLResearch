import random
# import langdetect # works okay, but lingua works better 
import json
from lingua import Language, LanguageDetectorBuilder # works well but biggest issue is you can't romanize anything
# import nltk
# import re

# nltk.download('punkt')
MAINLANG = "fr"
languages = [Language.SWAHILI, Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH] # Language.ARABIC (swahili used as replacement)
detector = LanguageDetectorBuilder.from_languages(*languages).build()
# detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build() # if you want all langs

def getDetectedLang(distrib):
    return str(distrib[0]).split(':')[0]

def onlyPunctuation(input_string):
    punctuation_pattern = re.compile(r'^[^\w\s\d]$')
    match = punctuation_pattern.search(input_string)
    return bool(match)


def langDetectStats(text):
    # get overall stats
    """
    distrib = langdetect.detect_langs(text)
    print("OVERALL DISTRIB")
    print(distrib)
    """
    # sep by \n
    lines = text.split('\n')
    print("LINES NOW")
    for l in lines:
        if l != "":
            # distrib = langdetect.detect_langs(l)
            distrib = detector.compute_language_confidence_values(l)
            print(l)
            print(distrib)
            continue
            if getDetectedLang(distrib) != "fr" or len(distrib) != 1:
                print(l)
                print(distrib)
                # go word level here
                """
                tokens = nltk.word_tokenize(l)
                print("KEY WORDS")
                for t in tokens:
                    if not (onlyPunctuation(t) or t.isdigit()):
                        distrib = langdetect.detect_langs(t)
                        if getDetectedLang(distrib) != "fr" or len(distrib) != 1:
                            print(t)
                            print(distrib)
                """





with open('../dataEntries/frenchData.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)

dataOfInterest = [d for d in data['allSongs'] if d['lyrics'] != ""]
numSongs = len(dataOfInterest)
print(f"Number of songs: {numSongs}")

toExamine = random.randint(0, numSongs - 1)

firstVal = dataOfInterest[toExamine]
lyricstoExamine = firstVal['lyrics']
# lyricstoExamine = "Allah"

print("First text")
print("SONG NAME: " + firstVal['name'])
print(lyricstoExamine)

langDetectStats(lyricstoExamine)