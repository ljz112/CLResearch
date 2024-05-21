####### IN USE FOR PROJECT: scale the frequencies of graphs to # of times used in lyrics 


import json
from dataAnalysis import getAverageGraph
import numpy as np


# sum all the weights and put in this dictionary
with open('collectedData/allGraphsNew.json', 'r') as file:
    graphData = json.load(file)["year"]
    totalFreqs = getAverageGraph(graphData, False)
    totalFreqs = {str(tf[0]): tf[1] for tf in totalFreqs}

# just invert these to get your correct scale factor

# print the basic statistics of the usage of all borrowed words
with open('collectedData/totalWordCounts.json', 'r') as file: 
    factorData = json.load(file)["wordNumber"]["y"]
    wordCountArr = []
    for g in graphData:
        i = 0
        graph = graphData[g]
        sortGraph = sorted(graph, key=lambda point: point[0])
        sortGraph = [point[1] for point in sortGraph]
        wordCountArr.append(sum([round(sortGraph[i] * factorData[i]) for i in range(len(sortGraph))]))

    print(sum(wordCountArr))
    print("MEAN")
    print(np.mean(wordCountArr))
    print("MEDIAN")
    print(np.median(wordCountArr))
    print("STANDARD DEVIATION")
    print(np.std(wordCountArr))
    print(min(wordCountArr))
    print(max(wordCountArr))
    print(np.percentile(wordCountArr, 75) - np.percentile(wordCountArr, 25))

"""
scaleFactors = [[tf, 1 / totalFreqs[tf]] for tf in totalFreqs]
forJson = {}
data = sorted(scaleFactors, key=lambda point: point[0])
y_values = [point[1] for point in data]
forJson["wordNumber"] = {"y": y_values}
print(forJson)
"""
"""
json_data = json.dumps(forJson)
json_file_path = "collectedData/forRFileFactors.json"
with open(json_file_path, "w") as json_file:
    json_file.write(json_data)
print("All graphs uploaded to json file")
"""
