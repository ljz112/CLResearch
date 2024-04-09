import json
from fuzzywuzzy import fuzz
import spacy # because tokenizing more is better than tokenizing less imo
import re
# from metaphone import doublemetaphone
import random

nlp = spacy.load("fr_core_news_sm")
startingDate = '1990-01'
threshhold = 100 # when running, if you want to test turn dev parameter to true in examineLine
splitOnRe = r'[\s\-\']' # better safe than sorry

# calculate number of months from start to curr (in string format)
def noMonths(start, curr, dateMode):
    # only if you want to see all the years
    if dateMode == "year":
        return int(curr)

    startyear, startmonth = start.split('-')
    curryear, currmonth = curr.split('-')
    startyear = int(startyear)
    startmonth = int(startmonth)
    curryear = int(curryear)
    currmonth = int(currmonth)

    # math for calculating months
    if currmonth >= startmonth:
        return (12 * (curryear - startyear)) + (currmonth - startmonth)
    else:
        # 2000-10 and 2002-08 for example
        return (12 * (curryear - 1 - startyear)) + (12 + currmonth - startmonth)

# exploring methods for finding the membership (for the )
def fineTuneMembership(lyrics, slang, method = 'default'):

    # method 1: count all occurences of the slang as a substring in lyrics
    if method == 'default':
        count = lyrics.lower().count(slang)
        # if count >= 1:
            # print(lyrics)
        return count

    # method 2: more flexible with typographical variation
    if method == 'new':
        lines = lyrics.lower().split('\n')
        count = 0
        for line in lines:
            count += examineLine(line, slang)
        return count

# how to determine if a lexical borrowing occurs in a line (change dev if you want to see examples w lowered threshhold)
def examineLine(line, slang, isDisp = False, dev = False):

    # init a few things
    slangLen = len(slang)
    slangExtraWords = slang.count(' ')
    joinPunctuation = ["'", "-"]
    count = 0
    thresh = 80 if dev else threshhold

    # first, find max subst dist / str len in the string
    if fuzz.partial_ratio(slang, line) >= thresh:

        # tokenize line (if doesn't work as well try double metaphone)
        doc = nlp(line)
        tokens = [token.text for token in doc]
        i = 0
        for token in tokens:
            # if the ratio is (basically) the same as the partial ratio
            if fuzz.ratio(slang, token) >= thresh:
                if dev:
                    print("CASE 1")
                    print(line)
                count += 1
                if isDisp:
                    return True
            # edge case 1: there are multiple words in the slang
            elif (slangExtraWords > 0) and (i >= slangExtraWords) and (fuzz.ratio(slang, ' '.join(tokens[i-slangExtraWords : i+1])) >= thresh):
                if dev:
                    print("CASE 2")
                    print(line)
                count += 1
                if isDisp:
                    return True
            # edge case 2: the token was cut off by a joining punctuation, (eg ' or -)
            elif (slangLen > len(token)) and (i > 0) and (tokens[i - 1] in joinPunctuation) and (fuzz.ratio(slang, ''.join([tokens[i-2], tokens[i - 1], token])) >= thresh):
                if dev:
                    print("CASE 3")
                    print(line)
                count += 1
                if isDisp:
                    return True
            i += 1
    
    return False if isDisp else count


# for getting the plot of words over time
def getWordUsePlot(slang, mode = "total_num", dataOfInterest = [], dateMode = ""):

    if __name__ == "__main__":
        with open('../dataEntries/frenchData.json', 'r') as file:
            # Load the JSON data into a Python dictionary
            data = json.load(file)

        dataOfInterest = [d for d in data['allSongs'] if d['lyrics'].replace('\n', '').strip() != ""]
    # random seed just for testing
    # dataOfInterest = [dataOfInterest[random.randint(0, len(dataOfInterest) - 1)]]

    # need to make a dictionary for date then return the pairs
    graphDict = {}
    for di in dataOfInterest:
        # change date to granularity of month
        date = di['releaseDate']
        if '-' not in date:
            # if you only want months take this away
            if dateMode == "month":
                continue
            key = date + '-01'
        else:
            key = date[:-3]

        if dateMode == "year":
            key = key.split('-')[0]

        # print(key)
        
        # parse lyric in popularity measure you'd like to see
        lyrics = di['lyrics']
        if mode == "total_num":
            count = fineTuneMembership(lyrics, slang, 'new') # lyrics.lower().count(slang)
            if key in graphDict:
                graphDict[key] += count
            else:
                graphDict[key] = count
        elif mode == "freq":
            # Def use spacy later, but right now I feel like it's too slow
            # collect all the words in the lyrics, and basically have 2 things: 
            # number of occurences of word (adj on word length) and num total words
            
            # take away the [] blocks 
            lyrics = re.sub(r'\[.*?\]', '', lyrics)

            count = fineTuneMembership(lyrics, slang, 'new')
            wordMultiplier = slang.count(' ') + 1
            totalWords = 0
            lines = lyrics.lower().split('\n')
            for line in lines:
                # only not using spacy here because of the punctuation, just taking away the - and the '
                lineStrip = line.strip()
                if lineStrip != "":
                    words = re.split(splitOnRe, lineStrip)
                    totalWords += len(re.split(splitOnRe, lineStrip))
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
                    if examineLine(line, slang, True): 
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

    graphList = [(noMonths(startingDate, gd, dateMode), decideFormat(graphDict[gd])) for gd in graphDict]
    return graphList

# reminder: it's not really slang I'm looking at but lexical borrowings. so keeping it for this file but will be diff in others
if __name__ == "__main__":
    slangword = "wesh"
    mode = "disp"
    print(getWordUsePlot(slangword, mode))