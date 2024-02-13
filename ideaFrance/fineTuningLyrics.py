import sys
sys.path.append('../lyricCollection')
from spotifyReader import collectMostSongs
from geniusReader import getLyric

import random

# basically just to test that the lyric data cleaning works well

frenchData = collectMostSongs('fr', 20, 2)

toExamine = random.sample(frenchData, 10)

print("SONGS")
print(toExamine)

for te in toExamine:
    getLyric(te[0], te[1][0], True)