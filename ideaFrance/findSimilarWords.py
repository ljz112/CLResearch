import json
from embeddingsPlayground import getWords, museWordEmbed
import numpy as np

ctrlWord = "pote"

print("Opening collected data")

# first open the bow file
with open('collectedData/bowFrenchDataNew.json', 'r') as file:
    data = json.load(file)
borrowedWords = getWords()
wordList = [w[0] for w in data['words'][0] if (w[0] not in borrowedWords)]

simWords = museWordEmbed(True, ctrlWord, wordList)

print(simWords)