import random
# import langdetect # works okay, but lingua works better 
import json
from unidecode import unidecode
import re
from lingua import Language, LanguageDetectorBuilder # works well but biggest issue is you can't romanize anything
import spacy

# nltk.download('punkt')
languages = [Language.SWAHILI, Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH] # Language.ARABIC (swahili used as replacement)
detector = LanguageDetectorBuilder.from_languages(*languages).build()
useDetect = False
if not useDetect:
    nlp = spacy.load("fr_core_news_sm")
    with open('../../../francais.txt', 'r', encoding='utf-8') as file:
        # Load the JSON data into a Python dictionary
        text = file.read()
        dictData = [s.strip() for s in text.split('\n') if s.strip() != '']
# detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build() # if you want all langs

def getDetectedLang(distrib):
    return str(distrib[0]).split(':')[0]

def onlyPunctuation(input_string):
    punctuation_pattern = re.compile(r'^[^\w\s\d]$')
    match = punctuation_pattern.search(input_string)
    return bool(match)

# for lingua
def analyzeDistrib(distrib):
    confidence = distrib[0]
    return confidence.language.name != "FRENCH" or confidence.value < 0.7

# to normalize the txt 
def textNormalize(text):
    text = unidecode(text.lower())
    text = text.replace("'", "e")
    text = re.sub(r'[^\w\s]','',text)
    if text.strip() == "":
        return "je"
    return text

# get overall lang detect stats
def langDetectStats(text):
    """
    distrib = langdetect.detect_langs(text)
    print("OVERALL DISTRIB")
    print(distrib)
    """
    # sep by \n
    lines = text.split('\n')
    notWords = []
    print("LINES/WORDS NOW")
    for l in lines:
        if l != "":
            if useDetect:
                distrib = detector.compute_language_confidence_values(l)
                if analyzeDistrib(distrib):
                    print(l)
                    print(distrib)
                continue
            else:
                # tokenize for words (TODO THERE ARE SOME CHARS NOT MATCHING IN HERE, esp phonetic/accented ones. file read or accent mapping)
                doc = nlp(l)
                tokens = [textNormalize(token.text) for token in doc]
                for t in tokens:
                    if t in dictData:
                        continue 
                    notWords.append(t)
    print(set(notWords))




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