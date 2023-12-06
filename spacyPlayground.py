import spacy
import wikiReader
from sentence_transformers import SentenceTransformer
import numpy as np

# a util function
def euclidean_distance(vector1, vector2):
    # Convert the input vectors to numpy arrays
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    
    # Calculate the Euclidean distance
    distance = np.linalg.norm(vector1 - vector2)
    
    return distance


# spaCy nlp stuff
### en_core_web_sm
### de_core_news_sm
nlp = spacy.load("de_core_news_sm")

#sBERT stuff
embedder = SentenceTransformer('distiluse-base-multilingual-cased-v1')
# or should it be more linguistic minorities? test for later
takeAvgOf = []
sampleBackgrounds = ['American', 'Brazilian', 'Nigerian', 'German', 'Chinese', 'Arab', 'Jewish', 'Indian', 'Australian']
for sb in sampleBackgrounds:
    takeAvgOf.append(np.array(embedder.encode("He is " + sb)))
ctrlEmbed = np.mean(takeAvgOf, axis = 0)


def similarEnough(text, threshhold = 0.9):
    thisEmbed = embedder.encode(text)
    dist = euclidean_distance(thisEmbed, ctrlEmbed)
    print(dist)
    return dist < threshhold



def getRoots(text):
    
    roots = []

    doc = nlp(text)

    adjectives = [token.text for token in doc if token.pos_ == "ADJ"]

    for a in adjectives:
        # you prolly need the head thing and all but otherwise I think it works well
        sampleText = "Er ist " + a
        print(sampleText)
        if similarEnough(sampleText):
            roots.append(a)

    return roots


name = 'Eminem (rapper)'

summ_txt, early_txt = wikiReader.getBlurbs(name)
print("AFTER ALG")
endList = list(set(getRoots(summ_txt) + getRoots(early_txt)))
print(endList)