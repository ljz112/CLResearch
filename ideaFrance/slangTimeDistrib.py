# what would I like to test? 

# 1) getting the temporal changes graph (right now only based on frequency, lowered) (dispersion next, research this before tho)
# 2) looking for transcription things and how to overcome them (edit distance idea?)

import json

"""
import spacy
nlp = spacy.load("fr_core_news_sm")
"""

startingDate = '1990-01'

# calculate number of months from start to curr (in string format)
def noMonths(start, curr):
    startyear, startmonth = start.split('-')
    curryear, currmonth = curr.split('-')
    startyear = int(startyear)
    startmonth = int(startmonth)
    curryear = int(curryear)
    currmonth = int(currmonth)
    if currmonth >= startmonth:
        return (12 * (curryear - startyear)) + (currmonth - startmonth)
    else:
        # 2000-10 and 2002-08 for example
        return (12 * (curryear - 1 - startyear)) + (12 + currmonth - startmonth)

# for getting the plot of words over time
def getWordUsePlot(slang, mode = "total_num"):

    with open('../dataEntries/frenchData.json', 'r') as file:
        # Load the JSON data into a Python dictionary
        data = json.load(file)

    dataOfInterest = data['allSongs']
    # dataOfInterest = [d for d in data['allSongs'] if slang in d['lyrics'].lower()]
    # print(f"Number of songs with the word {slang}: {len(dataOfInterest)}")

    # need to make a dictionary for date then return the pairs
    graphDict = {}
    for di in dataOfInterest:
        # change date to granularity of month
        date = di['releaseDate']
        if '-' not in date:
            key = date + '-01'
        else:
            key = date[:-3]
        
        # parse lyric in popularity measure you'd like to see
        lyrics = di['lyrics']
        if mode == "total_num":
            count = lyrics.lower().count(slang)
            if key in graphDict:
                graphDict[key] += count
            else:
                graphDict[key] = count
        elif mode == "freq":
            # Def use spacy later, but right now I feel like it's too slow
            # collect all the words in the lyrics, and basically have 2 things: 
            # number of occurences of word (adj on word length) and num total words
            count = lyrics.lower().count(slang)
            wordMultiplier = slang.count(' ') + 1
            totalWords = 0
            lines = lyrics.lower().split('\n')
            for line in lines:
                words = line.strip().split(' ')
                totalWords += len(words)
            if key in graphDict:
                graphDict[key][0] += count
                graphDict[key][1] += totalWords
            else:
                graphDict[key] = [count, totalWords]
        elif mode == "disp":
            # average the frequency of lines that the word pops up in the song
            lines = lyrics.lower().split('\n')
            numLines = 0
            lineWithSlang = 0
            for line in lines:
                if line.strip() != "":
                    if slang in line: 
                        lineWithSlang += 1
                    numLines += 1

            if numLines == 0:
                dispRatio = 0
            else:
                dispRatio = lineWithSlang / numLines

            if key in graphDict:
                graphDict[key] += [dispRatio]
            else:
                graphDict[key] = [dispRatio]

    # final graph to print
    def decideFormat(element):
        if mode == "freq":
            return element[0] / element[1]
        elif mode == "disp":
            return sum(element) / len(element)
        else:
            return element

    graphList = [(noMonths(startingDate, gd), decideFormat(graphDict[gd])) for gd in graphDict]
    return graphList

slangword = "allah"
mode = "disp"
print(getWordUsePlot(slangword, mode))