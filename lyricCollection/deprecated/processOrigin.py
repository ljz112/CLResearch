import spacy
import wikiReader
from sentence_transformers import SentenceTransformer
import numpy as np
import config


#sBERT stuff
embedder = SentenceTransformer('distiluse-base-multilingual-cased-v1')
# or should it be more linguistic minorities? test for later (nonetheless training for NORP entity)
takeAvgOf = []
sampleBackgrounds = ['American', 'Brazilian', 'Nigerian', 'German', 'Chinese', 'Arab', 'Jewish', 'Indian', 'Australian']
for sb in sampleBackgrounds:
    takeAvgOf.append(np.array(embedder.encode("He is " + sb)))
ctrlEmbed = np.mean(takeAvgOf, axis = 0)

# determines if something counts as a NORP entitiy based on the training of what is one
def similarEnough(text, threshhold = 0.7):
    thisEmbed = embedder.encode(text)
    dist = euclidean_distance(thisEmbed, ctrlEmbed)
    print(dist)
    return dist < threshhold

# a util function
def euclidean_distance(vector1, vector2):
    # Convert the input vectors to numpy arrays
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    # Calculate the Euclidean distance
    distance = np.linalg.norm(vector1 - vector2)
    return distance

# (fairly) accurate way to get all NORP ents of person for all languages, still need some embedding technique to ensure it corresponds to the right person
def getRoots(text, lang):
    nlp = spacy.load(config.LANG_SETTINGS[lang]['spacyKey'])
    
    roots = []

    doc = nlp(text)

    adjectives = [token.text for token in doc if token.pos_ == "ADJ"]

    for a in adjectives:
        # you prolly need the head thing and all but otherwise I think it works well
        sampleText = config.LANG_SETTINGS[lang]['sentence'] + a
        print(sampleText)
        if similarEnough(sampleText):
            roots.append(a)

    return roots

# main function to be called
def getAllRoots(query, lang):
    summ_txt, early_txt = wikiReader.getBlurbs(query, lang)
    print("AFTER ALG")
    endList = list(set(getRoots(summ_txt, lang) + getRoots(early_txt, lang)))
    return endList

if __name__ == "__main__":
    name = 'Snoop Dogg'

    summ_txt, early_txt = wikiReader.getBlurbs(name, 'en')
    print("AFTER ALG")
    endList = list(set(getRoots(summ_txt) + getRoots(early_txt)))
    print(endList)


"""
# older and doesn't consider place in sentence
#code here (check that boolean)
def getRoots(text):
    doc = nlp(text)
    allRoots = []
    onlyParents = False
    for s in doc.sents:
        inSentence = []
        print(s.ents)
        for e in s.ents:
            print(e.label_)
            if e.label_ == 'NORP' or e.label_ == 'MISC':
                if onlyParents:
                    referring = e.root.head.text.lower()
                    # maybe check if word2vec embedding is similar to the following words
                    hotWords = ['mother', 'father', 'parent', 'descent', 'ancestry', 'origin']
                    if any([(hw in referring) for hw in hotWords]):
                        inSentence.append(e.text)
                else:
                    print(e)
                    inSentence.append(e.text)
        if inSentence == []:
            onlyParents = True
        allRoots += inSentence
    return allRoots
"""




"""
def removeFunctionMarkingLater():
    # embedding stuff: not really sure what to do. word2vec has to be trained, fastText needs the huge vector files
    # you could say "his parents are Nigerian" or "he is of Nigerian origin". Basically a control sentence. But if a compound sentence, make sure to take away the clauses
    # distiluse-base-multilingual-cased-v1


    # you might need this for early/private life or smth else

    thatSentence = "He is Nigerian"

    print(encoded_input)

    def similarWords(thisWord):
        thatWord = "parent"

    print("Hello world")
"""
