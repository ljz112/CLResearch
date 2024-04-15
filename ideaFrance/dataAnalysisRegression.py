####### IN USE FOR PROJECT: run the regression (for given set of languages) and output the coefficients, standard error, and CIs




import json
import csv
from slangTimeDistrib import startingDate, noMonths
from languageTree import LANGUAGE_TREE
from dataAnalysis import hasLangListVal
import statsmodels.api as sm
from lingua import Language, LanguageDetectorBuilder
import numpy as np

languages = [Language.SWAHILI, Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.ITALIAN, Language.SPANISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()
treeToAnalyze = LANGUAGE_TREE
clusters = [tl['language'] for tl in treeToAnalyze] 

# model: statsmodels RLM (categorical dummy encoded)
# dependent: weighted average of the frequency 
# independent: origin, pos, semantic, word length

# helper to format date like in slangtimedistrib
def formatDate(date):
    if '-' not in date:
        return date + '-01'
    else:
        return date[:-3]

# get weights for weighted average (new and old)
with open('../dataEntries/frenchDataNew.json', 'r') as file:
    data1 = json.load(file)['allSongs']

with open('../dataEntries/frenchDataOldSongs.json', 'r') as file:
    data2 = json.load(file)['allSongs']
    data1 += data2
    data1 = [d for d in data1 if ((d['lyrics'].replace('\n', '').strip() != "") and (detector.compute_language_confidence_values(d['lyrics'])[0].language.name == "FRENCH"))]
    seen = {}
    data = []
    for item in data1:
        if item['lyrics'] not in seen:
            seen[item['lyrics']] = True
            data.append(item)

    # collect the weights for the number dict (change to year)
    numberDict = {}
    def addElement(element):
        if element in numberDict:
            numberDict[element] += 1
        else:
            numberDict[element] = 1
    for di in data:
        date = di['releaseDate']
        addElement(date.split("-")[0])

with open('collectedData/totalWordCounts.json', 'r') as file:
    totalWordCounts = json.load(file)['wordNumber']['y']
    totalWordInd = lambda year : int(year - 1991)

# helper to get weighted average (updating to have integral outputs of total years)
def getWeightedAverage(graph, avgFreq = False):
    if avgFreq:
        N = 0
        S = 0
        for g in graph:
            date, freq = g
            number = numberDict[str(date)]
            S += number
            N += number * freq
        return N / S
    else: 
        N = 0
        for g in graph:
            date, freq = g
            N += round(freq * totalWordCounts[totalWordInd(date)])
        return N
        
# use the weights to caluclate the average
with open('collectedData/allGraphsNew.json', 'r') as file:
    graphData = json.load(file)["year"]
    y = []
    for gd in graphData:
        y.append(getWeightedAverage(graphData[gd], False))

# now collect the inputs
with open('collectedData/borrowedWords.csv', 'r', newline='', encoding='utf-8') as file:
    wordData = list(csv.reader(file))[1:]
    X = []
    clen = len(clusters)
    clusterCounts = [0] * clen
    clusterThresh = 5
    semlen = 10
    posType = ["noun", "verb", "adj", "adv", "int"]
    posLen = len(posType)

    # make reference for the encoding
    encodingRef = ["word_length"]
    for c in clusters:
        encodingRef.append("language_" + c)
    for i in range(semlen):
        encodingRef.append("semcat_" + str(i + 1))
    for pos in posType:
        encodingRef.append("pos_" + pos)
    encodingRef = np.array(encodingRef)

    # gather the four data fields (dummy encoded)
    for w in wordData:
        word = w[0]
        # word length
        wordLen = len(word)
        # semantic category (split if )
        semArr = [0] * semlen
        semCat = w[3]
        if type(semCat) == int:
            semArr[semCat - 1] = 1
        else:
            semCats = semCat.split(",")
            for sc in semCats:
                semArr[int(sc) - 1] = 1
        posArr = [0] * posLen
        # part of speech
        for i in range(posLen):
            if w[4 + i] != "":
                posArr[i] = 1
        originArr = [0] * clen
        # language origin
        for i in range(clen):
            if hasLangListVal(word, clusters[i], treeToAnalyze): # w[1] == clusters[i]:
                originArr[i] = 1
                clusterCounts[i] += 1
                break
            if i == clen - 1:
                continue
        X.append([wordLen] + originArr + semArr + posArr)

    toDelete = []
    X = np.array(X)
    # deal with languages below the threshhold, take away language field for less dims
    for i in range(clen):
        if clusterCounts[i] < clusterThresh:
            toDelete.append(i + 1)
    X = np.delete(X, toDelete, axis=1)
    encodingRef = np.delete(encodingRef, toDelete)

# now do the data analysis code
rlm_model = sm.RLM(y, X, M=sm.robust.norms.HuberT())
rlm_results = rlm_model.fit()
print("REFERENCE")
print(encodingRef)
print("PARAMS")
print(rlm_results.params)
print("BSE")
print(rlm_results.bse)
print("P_VALS")
print(rlm_results.pvalues)
print("STATISTICALLY SIGNIFICANT")
print([r < 0.05 for r in rlm_results.pvalues])
# at 0.95 confidence
conf_ints = rlm_results.conf_int(0.05)
print("CONFIDENCE INTERVALS")
print(conf_ints)

forJson = [[rlm_results.params[i], conf_ints[i][0], conf_ints[i][1], encodingRef[i]] for i in range(len(encodingRef))]

"""
json_data = json.dumps(forJson)
json_file_path = "collectedData/forRFileErrBars.json"
with open(json_file_path, "w") as json_file:
    json_file.write(json_data)
print("All graphs uploaded to json file")
"""