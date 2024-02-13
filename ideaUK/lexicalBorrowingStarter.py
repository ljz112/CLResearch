# using until I can find something better, library taken from https://pypi.org/project/pylazaro/

from pylazaro import Lazaro

import json

tagger = Lazaro()


# code I got from the website to analze for borrwings
def analyzeForBorrowings(text):

    # The text we want to analyze for borrowing detection
    # text = "Inteligencia artificial aplicada al sector del blockchain, la e-mobility y las smarts grids entre otros; favoreciendo las interacciones colaborativas."

    # We run our tagger on the text we want to analyze
    result = tagger.analyze(text)

    # We get results
    print(text)
    print(result.borrowings_to_tuple())

    # print(result.tag_per_token())

with open("discographyData/output.json", "r") as file:
    data = json.load(file)

text = data['discography'][0]['lyrics']

# try all text first (looks like it only works when it's surrounded by spanish)
text = "Eso text es en espanol, My nephew weird as hell, he pull his pants down when he pee, mas de espanol aqui inteligencia artificial"
analyzeForBorrowings(text)