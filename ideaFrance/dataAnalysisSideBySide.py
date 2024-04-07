### objective: output data and plot graphs side by side to examine/perform data analysis

import json
import csv
from languageTree import LANGUAGE_TREE
from dataAnalysis import hasLangListVal, getAverageGraph
import matplotlib.pyplot as plt

# 0: origin, 1: semantic, 2: pos
analysisMode = 0

with open('collectedData/allGraphs.json', 'r') as file:
    graphData = json.load(file)

with open('collectedData/borrowedWords.csv', 'r', newline='', encoding='utf-8') as file:
    wordData = list(csv.reader(file))[1:]

graphSet = {}
if analysisMode == 0:
    # which tree to analyze? (doing broadest now)
    treeToAnalyze = LANGUAGE_TREE[6]['children']
    clusters = [tl['language'] for tl in treeToAnalyze] 
    graphData = {w: graphData[w] for w in graphData if any(hasLangListVal(w, i, treeToAnalyze) for i in clusters)}
    # for each word involved
    for c in clusters:
        specificData = {w: graphData[w] for w in graphData if hasLangListVal(w, c, treeToAnalyze)}
        graphSet[c] = getAverageGraph(specificData, False)

elif analysisMode == 1:
    pass
else:
    pass

# now print the graph
for c in graphSet:
    # convert to array, organize
    data = sorted(graphSet[c], key=lambda point: point[0])
    # then plot
    x_values = [point[0] for point in data]
    y_values = [point[1] for point in data]
    plt.plot(x_values, y_values, label=c)

plt.xlabel('Number')
plt.ylabel('Word Frequency')
plt.title('Words stacked together')
plt.legend(loc='upper left')
# plt.yscale('log')

plt.show()