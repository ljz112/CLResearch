import sys
sys.path.append('../lyricCollection')
from spotifyReader import collectMostSongs

country = 'fr'
splitYear = 2015

searchSize = 50
searchDepth = 15

# helper to add to graphDict
def addToGraph(year):
    if year in graphDict:
        graphDict[year] += 1
    else:
        graphDict[year] = 1

graphDict = {}

# get a distribution of songs over time round 1
print(f"Collecting data before {splitYear}...")
frenchData = collectMostSongs(country, searchSize, searchDepth)
numSongs = len(frenchData)
print(f"Collected {numSongs} songs for round 1.")

for fd in frenchData:
    releaseDate = fd[2]
    year = int(releaseDate.split("-")[0])
    if year > splitYear:
        continue
    addToGraph(str(year))

# get a distribution of songs over time round 2
searchSize = 25
searchDepth = 3

print(f"Collecting data after {splitYear}...")
frenchData = collectMostSongs(country, searchSize, searchDepth)
numSongs = len(frenchData)
print(f"Collected {numSongs} songs for round 2.")

for fd in frenchData:
    releaseDate = fd[2]
    year = int(releaseDate.split("-")[0])
    if year <= splitYear:
        continue
    addToGraph(str(year))

# convert to a list
graph = [(int(gd) - 1990, graphDict[gd]) for gd in graphDict]
# then output
print(graph)

# analysis:
# 25, 3 makes exponential increase over time
# 50, 3 has a higher plateau but same shape
# 25, 8 is somewhere in between
# 50, 8 has more too but it gets beyond exponential which is crazy


# outcome: 
# do a more intensive search for dates before 2015 (that's when curve starts spiking) 
# 50, 15 looks promising
# 50, 20 looks worse (also kinda asymptotic so 50, 15 it is)
