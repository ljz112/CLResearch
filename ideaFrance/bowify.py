import json
import gensim
import pprint
from gensim import corpora
from gensim.utils import simple_preprocess
from lingua import Language, LanguageDetectorBuilder

languages = [Language.SWAHILI, Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.ITALIAN, Language.SPANISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

### just so I can view the french songs in a BOW approach (all together with combined counts)

# open the file

with open('../dataEntries/frenchDataNew.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)

startData = [d['lyrics'] for d in data['allSongs'] if ((d['lyrics'].replace('\n', '').strip() != "") and (detector.compute_language_confidence_values(d['lyrics'])[0].language.name == "FRENCH"))]
# remove duplicates
seen = {}
doc_list = []
for item in startData:
    if item not in seen:
        seen[item] = True
        doc_list.append(item)


doc_tokenized = [simple_preprocess(doc) for doc in doc_list]
doc_tokenized = [[element for sublist in doc_tokenized for element in sublist]]

dictionary = corpora.Dictionary()

BoW_corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in doc_tokenized]

id_words = [[(dictionary[id], count) for id, count in line] for line in BoW_corpus]

json_data = json.dumps({'words': id_words})
json_file_path = "bowFrenchDataNew.json"
with open(json_file_path, "w") as json_file:
    json_file.write(json_data)