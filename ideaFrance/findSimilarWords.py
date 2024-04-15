######## IN USE FOR PROJECT: use cosine similarity (along with embeddingsPlayground) to find all similar words to all collected borrowings


import json
from embeddingsPlayground import getWords, museWordEmbed
import numpy as np

# do this for every single category
borrowedWords = getWords()

# first open the bow file
with open('collectedData/bowFrenchDataNew.json', 'r') as file:
    data = json.load(file)
wordList = [w[0] for w in data['words'][0] if (w[0] not in borrowedWords)]

for bw in borrowedWords:
    simWords = museWordEmbed(True, bw, wordList)
    if (simWords is None) or (simWords == []):
        print(bw + " : None")
    else:
        print(bw + " has words:")
        print(simWords)