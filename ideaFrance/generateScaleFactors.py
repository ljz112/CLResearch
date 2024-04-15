####### IN USE FOR PROJECT: scale the frequencies of graphs to # of times used in lyrics 


import json
from dataAnalysis import getAverageGraph


# sum all the weights and put in this dictionary
with open('collectedData/allGraphsNew.json', 'r') as file:
    graphData = json.load(file)["year"]
    totalFreqs = getAverageGraph(graphData, False)
    totalFreqs = {str(tf[0]): tf[1] for tf in totalFreqs}

# just invert these to get your correct scale factor
scaleFactors = [[tf, 1 / totalFreqs[tf]] for tf in totalFreqs]
forJson = {}
data = sorted(scaleFactors, key=lambda point: point[0])
y_values = [point[1] for point in data]
forJson["wordNumber"] = {"y": y_values}
print(forJson)
"""
json_data = json.dumps(forJson)
json_file_path = "collectedData/forRFileFactors.json"
with open(json_file_path, "w") as json_file:
    json_file.write(json_data)
print("All graphs uploaded to json file")
"""
