####### IN USE FOR PROJECT: run the regression (for given set of languages) and output the coefficients, standard error, and CIs




import json
import csv
from slangTimeDistrib import startingDate, noMonths
from languageTree import LANGUAGE_TREE
from dataAnalysis import hasLangListVal
import statsmodels.api as sm
import numpy as np
import itertools
from open_files import getDataOfInterest

# gives you option to have dependent as raw count of words "count", number of songs it appears in "songs", and number of artists that say it "artist" 
mode = "artist"
treeToAnalyze = LANGUAGE_TREE
clusters = [tl['language'] for tl in treeToAnalyze] 

# model: statsmodels RLM (categorical dummy encoded)
# dependent: raw count of words, number of songs it appears in, and number of artists saying it (dependent on mode variable)
# independent: origin, pos, semantic, word length

# helper to format date like in slangtimedistrib
def formatDate(date):
    if '-' not in date:
        return date + '-01'
    else:
        return date[:-3]

data = getDataOfInterest()
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

y = []

if mode == "count":
    print("count")
    # use the weights to caluclate the average
    with open('collectedData/allGraphsNew.json', 'r') as file:
        graphData = json.load(file)["year"]
        y = []
        for gd in graphData:
            y.append([getWeightedAverage(graphData[gd], False)])

elif mode == "songs":
    print("songs")
    # all songs
    with open('collectedData/allGraphsSongCount.json', 'r') as file:
        graphData = json.load(file)["year"]
        for gd in graphData:
            miniGraph = graphData[gd]
            songSum = sum([mg[1] for mg in miniGraph])
            y.append(songSum)

elif mode == "artist":
    print("artist")
    # all artists
    with open('collectedData/allGraphsArtistCount.json', 'r') as file:
        graphData = json.load(file)["year"]
        for gd in graphData:
            miniGraph = graphData[gd]
            artistList = list(itertools.chain(*[mg[1] for mg in miniGraph]))
            artistSum = len(set(artistList))
            y.append(artistSum)

# now collect the inputs (X)
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

"""
# CSV for if you want to record all 3 outputs and export it alongside the inputs
forCSV = []
encodingRef = np.append(encodingRef, ['result_count', 'result_songs', 'result_artists'])
forCSV = np.array([encodingRef])
for i in range(len(y)):
    new_row = np.append(X[i], y[i])
    forCSV = np.vstack([forCSV, new_row])

with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(forCSV.tolist())
"""

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
json_file_path = "collectedData/forRFileErrBarsArtist.json"
with open(json_file_path, "w") as json_file:
    json_file.write(json_data)
print("All graphs uploaded to json file")
"""