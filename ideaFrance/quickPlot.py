import matplotlib.pyplot as plt
import json
from slangTimeDistrib import getWordUsePlot
from lingua import Language, LanguageDetectorBuilder
from fuzzywuzzy import fuzz
import re

languages = [Language.SWAHILI, Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.ITALIAN, Language.SPANISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

# change the word you want to analyze
word = "hola"
mode = "freq"
dateMode = "year" # "" for month but year gets added as january, "month" for all month specific ones, "year" for only the year

# collect the data
with open('../dataEntries/frenchDataNew.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)
# filter to french speaking ones only (7262/9497 songs)
startData = [d for d in data['allSongs'] if ((d['lyrics'].replace('\n', '').strip() != "") and (detector.compute_language_confidence_values(d['lyrics'])[0].language.name == "FRENCH"))]
# remove duplicates
seen = {}
dataOfInterest = []
for item in startData:
    if item['lyrics'] not in seen:
        seen[item['lyrics']] = True
        dataOfInterest.append(item)

# make the graph

data = getWordUsePlot(word, mode, dataOfInterest, dateMode)

"""
# open the data
with open('collectedData/allGraphs.json', 'r') as file:
    data = json.load(file)[word]
"""

# visualize the graph
data = sorted(data, key=lambda point: point[0])

# Extract x and y values from the data
x_values = [point[0] for point in data]
y_values = [point[1] for point in data]

# Plot the data as a line plot
plt.plot(x_values, y_values)

# Add labels and title
plt.xlabel('Year' if dateMode == "year" else 'Months after 1990')
plt.ylabel('Word Frequency')
plt.title('Usage of "' + word + '" over time in French rap lyrics')

# Display the plot
plt.show()
