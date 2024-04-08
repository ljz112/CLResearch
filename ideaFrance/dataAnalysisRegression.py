import json
import csv
from slangTimeDistrib import startingDate, noMonths
from languageTree import LANGUAGE_TREE
from dataAnalysis import hasLangListVal
import statsmodels.api as sm

treeToAnalyze = LANGUAGE_TREE
clusters = [tl['language'] for tl in treeToAnalyze] 

# model: statsmodels RLM (assumption of only one per thing)
# dependent: weighted average of the frequency 
# independent: origin, pos, semantic, word length

# helper to format date like in slangtimedistrib
def formatDate(date):
    if '-' not in date:
        return date + '-01'
    else:
        return date[:-3]

# get weights for weighted average
with open('../dataEntries/frenchDataNew.json', 'r') as file:
    data = json.load(file)['allSongs']

    numberDict = {}

    def addElement(element):
        if element in numberDict:
            numberDict[element] += 1
        else:
            numberDict[element] = 1

    for di in data:
        date = di['releaseDate']
        addElement(str(noMonths(startingDate, formatDate(date), "")))

# helper to get weighted average
def getWeightedAverage(graph):
    N = 0
    S = 0
    for g in graph:
        date, freq = g
        number = numberDict[str(date)]
        S += number
        N += number * freq
    return N / S
        
# use the weights to caluclate the average
with open('collectedData/allGraphs.json', 'r') as file:
    graphData = json.load(file)
    y = []
    for g in graphData:
        y.append(getWeightedAverage(graphData[g]))

# now collect the inputs
with open('collectedData/borrowedWordsOldJustInCase.csv', 'r', newline='', encoding='utf-8') as file:
    wordData = list(csv.reader(file))[1:]
    X = []
    for w in wordData:
        word = w[0]
        # word length
        wordLen = len(word)
        # semantic category
        semCat = int(w[3])
        # part of speech
        for i in range(5):
            if w[4 + i] != "":
                pos = i
                break
        # language origin
        for i in range(len(clusters)):
            if hasLangListVal(word, clusters[i], treeToAnalyze):
                origin = i 
                break
        X.append([wordLen, semCat, pos, origin])


with open('collectedData/borrowedWords.csv', 'r', newline='', encoding='utf-8') as file:
    allWords = list(csv.reader(file))[1:]
    allWords = [w[0].strip() for w in allWords]
    print(allWords)
    dupeWords = [item for item in set(allWords) if list(allWords).count(item) > 1]
    print(dupeWords)
# now do the data analysis code
rlm_model = sm.RLM(y, X, M=sm.robust.norms.HuberT())
rlm_results = rlm_model.fit()
print(rlm_results.params)
print(rlm_results.bse)
print(rlm_results.pvalues)