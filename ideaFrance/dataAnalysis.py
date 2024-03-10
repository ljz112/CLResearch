import numpy as np
from scipy.stats import chisquare, chi2
import json
import csv
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d
import math
from languageTree import LANGUAGE_TREE

# open the data
with open('collectedData/allGraphs.json', 'r') as file:
    graphData = json.load(file)

with open('collectedData/borrowedWords.csv', 'r', newline='', encoding='utf-8') as file:
    wordData = list(csv.reader(file))[1:]

treeToAnalyze = LANGUAGE_TREE[10]['children']

# get the average graph
def getAverageGraph(graph):
    n = len(graph)
    # if it's smaller than this, it's susceptible to outliers, so take the median
    threshhold = 40
    """
    if n < threshhold:
        return getMedianGraph(graph)
    """
    graphDict = {}
    for g in graph:
        for pt in graph[g]:
            time = str(pt[0])
            if time in graphDict:
                graphDict[time] += pt[1]
            else:
                graphDict[time] = pt[1]
    return np.array([[int(t), float(graphDict[t] / n)] for t in graphDict])

# get the median graph
def getMedianGraph(graph):
    n = len(graph)
    graphDict = {}
    for g in graph:
        for pt in graph[g]:
            time = str(pt[0])
            if time in graphDict:
                graphDict[time].append(pt[1])
            else:
                graphDict[time] = [pt[1]]
    return np.array([[int(t), np.median(graphDict[t])] for t in graphDict])

# get 5 features of the graph
def getFeatures(graph):
    # need to sort the graph by increasing x value
    graph = graph[graph[:,0].argsort()]
    # 1/2: maximum (both x and y)
    y_points = graph[:, 1]
    max_ind = np.argmax(y_points)
    max_value = graph[max_ind][1]
    max_time = graph[max_ind][0]
    # 3: find median value
    # print(y_points)
    med_value = np.median(y_points)
    # 4: find area under curve
    x_points = graph[:, 0]
    area_value = np.trapz(y_points, x_points)
    # 5: number of local maxima (on smoothed graph)
    smoothed_y = gaussian_filter1d(y_points, sigma=1)
    peaks, _ = find_peaks(smoothed_y)
    num_local_maxima = len(peaks)
    return [max_value, max_time, med_value, area_value, num_local_maxima]

# for the semantic clusters
def getSemCat(word):
    return int([w[3] for w in wordData if w[0] == word][0])

# for the part of speech
def hasPOS(word, ind):
    # then check that specific ind
    return [w[ind + 4] for w in wordData if w[0] == word][0].strip() == "c"

# search the tree
def searchTree(lt, origin):
    if lt['language'] == origin:
        return True
    if lt['children'] == []:
        return False
    for c in lt['children']:
        if searchTree(c, origin):
            return True
    return False

# find the language group
def findLangGroup(origin):
    for lt in treeToAnalyze:
        if searchTree(lt, origin):
            return lt['language']

# for the list format of languages
def hasLangListVal(word, group):
    origin = [w[1] for w in wordData if w[0] == word][0]
    langGroup = findLangGroup(origin)
    return langGroup == group

def adjNum(num, const, i):
    scaleTo = 10.0
    x = const / scaleTo
    return num / x if x != 0.0 else 0.0
    # num / x = scaleTo
    # num / scaleTo = x
    """
    if i == 0:
        return num * 20000
    if i == 1:
        return num / 20
    if i == 2:
        return num * 150000
    if i == 3:
        return num * 400
    if i == 4: 
        return num / 3
    """

def print_results(clusters, observed, expected, p_value, i):
    print(["Max", "Max X", "Median", "Area", "Maxima"][i])
    print(clusters)
    print("Observed")
    print(observed)
    print("Expected")
    print(expected)
    print("P value")
    print(p_value)
    print()
        

# first get the average graph 
clusters = [tl['language'] for tl in treeToAnalyze]
before = graphData
graphData = {w: graphData[w] for w in graphData if any(hasLangListVal(w, i) for i in clusters)}
averageGraph = getAverageGraph(graphData)
features = getFeatures(averageGraph)

# now for every semantic cluster
featureDict = {}
df = len(clusters) - 1
for i in clusters:
    specificData = {w: graphData[w] for w in graphData if hasLangListVal(w, i)}
    # print(specificData.keys())
    specificGraph = getAverageGraph(specificData)
    specificFeatures = getFeatures(specificGraph)
    featureDict[i] = specificFeatures

# now perform the testing
for i in range(len(features)):
    observed = [adjNum(featureDict[j][i], features[i], i) for j in clusters]
    expected = [adjNum(features[i], features[i], i) for j in clusters]
    chiSum = 0
    for j in range(len(clusters)):
        chiSum += float(((observed[j] - expected[j])**2) / expected[j]) if expected[j] != 0.0 else 0.0
    p_value = 1 - chi2.cdf(chiSum, df)
    print_results(clusters, observed, expected, p_value, i)

"""
# from sklearn.linear_model import LinearRegression
# for working with regression (redacted)

def getSemCat(word):
    return int([w[3] for w in wordData if w[0] == word][0])

X = []
Y = []

for gd in graphData:
    dataList = graphData[gd]
    semCat = getSemCat(gd)
    X += [semCat for i in range(len(dataList))]
    Y += dataList

X = np.array(X)
Y = np.array(Y)

reg = LinearRegression().fit(Y, X)

# 0.002064460177274463 lmao
print(reg.score(Y, X))
"""