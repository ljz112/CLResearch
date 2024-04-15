####### IN USE FOR PROJECT: output data and plot graphs side by side (origin, semantic, POS, or just everything) to examine/perform data analysis

import json
import csv
from languageTree import LANGUAGE_TREE
from dataAnalysis import hasLangListVal, getAverageGraph
import matplotlib.pyplot as plt

# 0: origin, 1: semantic, 2: pos, 3: everything
analysisMode = 3

with open('collectedData/allGraphsNew.json', 'r') as file:
    graphData = json.load(file)["year"]

with open('collectedData/borrowedWords.csv', 'r', newline='', encoding='utf-8') as file:
    wordData = list(csv.reader(file))[1:]

graphSet = {}
if analysisMode == 0:
    # which tree to analyze? (doing broadest now)
    treeToAnalyze = LANGUAGE_TREE[7]['children']
    clusters = [tl['language'] for tl in treeToAnalyze]
    clusterThresh = 5
    graphData = {w: graphData[w] for w in graphData if any(hasLangListVal(w, i, treeToAnalyze) for i in clusters)}
    # for each word involved
    for c in clusters:
        specificData = {w: graphData[w] for w in graphData if hasLangListVal(w, c, treeToAnalyze)}
        if len(list(specificData.keys())) >= clusterThresh:
            graphSet[c] = getAverageGraph(specificData, True)

elif analysisMode == 1:
    def hasWordType(w, i):
        # find the word
        semCat = [row[3] for row in wordData if row[0] == w][0]
        if type(semCat) == int:
            return semCat == i
        else:
            semCats = semCat.split(",")
            return str(i) in semCats
    # semantic clusters time
    graphData = {w: graphData[w] for w in graphData}
    for i in range(10):
        specificData = {w: graphData[w] for w in graphData if hasWordType(w, i + 1)}
        # for each word need to find the 
        graphSet[str(i + 1)] = getAverageGraph(specificData, True)
elif analysisMode == 2:
    def hasPOSType(w, i):
        pos = [row[4 + i] for row in wordData if row[0] == w][0]
        return pos != ""
    graphData = {w: graphData[w] for w in graphData}
    for i in range(5):
        specificData = {w: graphData[w] for w in graphData if hasPOSType(w, i)}
        posWord = ["n", "v", "adj", "adv", "int"][i]
        graphSet[posWord] = getAverageGraph(specificData, True)
else:
    graphSet['everything'] = getAverageGraph(graphData, False)
forJson = {}

# now print the graph
for c in graphSet:
    # convert to array, organize
    data = sorted(graphSet[c], key=lambda point: point[0])
    # then plot
    x_values = [point[0] for point in data]
    y_values = [point[1] for point in data]
    # ONLY FOR SEMCAT (need to index forJson diff here too)
    # arr = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    forJson[c] = {"x": x_values, "y": y_values}
    plt.plot(x_values, y_values, label=c)

"""
# if you want to use your stuff for R do it here
json_data = json.dumps(forJson)
json_file_path = "collectedData/forRFilePOS.json"
with open(json_file_path, "w") as json_file:
    json_file.write(json_data)
print("All graphs uploaded to json file")
"""

plt.xlabel('Number')
plt.ylabel('Word Frequency')
plt.title('Words stacked together')
plt.legend(loc='upper left')
# plt.yscale('log')

plt.show()