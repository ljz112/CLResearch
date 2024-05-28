######### IN USE FOR PROJECT: use word2vec skipgram, urban dictionary, sentence embeddings, or Facebook MUSE, cluster, and evaluate similarity


import gensim
from gensim.models import fasttext, Word2Vec, KeyedVectors
from gensim.test.utils import datapath
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from nltk.tokenize import sent_tokenize, word_tokenize
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
from lang_trans.arabic import buckwalter
from languageTree import LANGUAGE_TREE
from dataAnalysis import hasLangListVal
from open_files import getWords

import numpy as np
import csv
import warnings
import json
import random

# just some setting up, change type of embedding here
mode = 3
modes = ['fr', 'en', 'es', 'it', 'de', 'ar']
onLang = -1
model = {}

if mode == 0:
    dimensionality = 300
elif mode == 1:
    dimensionality = 512
elif mode == 2:
    dimensionality = 100
elif mode == 3:
    dimensionality = 300
else:
    dimensionality = 1
defaultVec = [0.0] * dimensionality

# get the embedding of a word given a certain model
def getEmbed(word, function):
    try:
        return function(word)
    except KeyError as e:
        return None # defaultVec

# cluster the embeddings using k-means
def cluster(words, embeddings, num_clusters = 5):

    # optionally dimension reduction
    numDimMin = 2
    pca = PCA(n_components = numDimMin)
    pca.fit(embeddings)
    embeddings = pca.transform(embeddings)

    embedding_array = np.array(embeddings)
    # optionally normalize
    # embedding_array = normalize(embedding_array)

    # Apply K-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=1, n_init = 10)
    kmeans.fit(embedding_array)

    # Get cluster labels for each word
    cluster_labels = kmeans.labels_

    # Print the words and their corresponding cluster labels
    clustered_words = {}

    for word_id, cluster_id in enumerate(cluster_labels):
        if cluster_id not in clustered_words:
            clustered_words[cluster_id] = []
        clustered_words[cluster_id].append(words[word_id])

    word_embeddings = [[words[i], embeddings[i]] for i in range(len(words))]

    visualize_clusters(clustered_words, word_embeddings)

# plot the clusters found (taken from chatGPT)
def visualize_clusters(cluster_assignment, word_embeddings):

    # remove half of the elements found (for readability)
    other_assignment = {}
    for key in cluster_assignment:
        lookingAt = cluster_assignment[key]
        halfway_point = len(lookingAt) // 2
        other_assignment[key] = lookingAt[:halfway_point]
    cluster_assignment = other_assignment

    # "" for default k-means, "sem" for semantic, and "org" for origin (can change this based on what you'd like the coloring scheme to be)
    mode = "org"

    catArr = ["Identity-Based", "Occupational", "Food/Drugs", "Materials/Products", "Places", "Crime/Violence", "Sexual", "Expressions", "Grammatical/Other", "Arts-Related"]
    orgArr = ["Afroasiatic", "Romance", "Germanic", "Creoles", "Niger Congo", "East Asian", "Slavic", "Indo-Iranian", "Native American", "Other"]
    orgDict = {'afroasiatic': 1, 'lo': 10, 'romance': 2, 'east_asian': 6, 'creoles': 4, 'uralic': 10, 'dha': 10, 'germanic': 3, 'tml': 10, 'niger_congo': 5, 'slv': 7, 'tr': 10, 'indo_iranian': 8, 'native_american': 9, 'thi': 10, 'msh': 10, 'gr': 10, 'bsq': 10}
    wordData = getWords(True)

    # create dictionary for word -> semcat (no polysemy)
    actualSemCat = {}
    for wd in wordData[1:]:
        cat = wd[3] if type(wd[3]) == int else int(wd[3].split(",")[random.randrange(len(wd[3].split(",")))])
        actualSemCat[wd[0]] = cat - 1

    # create dictionary for word -> origin
    actualOrigins = {}
    typesOfOrg = []
    def checkAddOrigin(word, group, tree):
        if hasLangListVal(word, group, tree):
            actualOrigins[word] = orgDict[group] - 1
            typesOfOrg.append(group)
            return True
        return False
    for wd in wordData[1:]:
        for i in range(len(LANGUAGE_TREE)):
            endEurope = False
            if i == 7:
                for j in range(len(LANGUAGE_TREE[i]['children'])):
                    if checkAddOrigin(wd[0], LANGUAGE_TREE[i]['children'][j]['language'], LANGUAGE_TREE[i]['children']):
                        endEurope = True
                        break
                if endEurope:
                    break
            else:
                if checkAddOrigin(wd[0], LANGUAGE_TREE[i]['language'], LANGUAGE_TREE):
                    break

    # Initialize plot
    plt.figure(figsize=(10, 6))

    # Create a color map for clusters
    colors = plt.cm.get_cmap('tab10', len(cluster_assignment) if mode == "" else 10)

    # Plot each cluster separately
    for cluster_id, words in cluster_assignment.items():
        x = []
        y = []
        labels = []
        for word, embedding in word_embeddings:
            if word in words:
                x.append(embedding[0])
                y.append(embedding[1])
                labels.append(word)
        plt.scatter(x, y, color=colors(cluster_id), alpha=0, label=f'Cluster {cluster_id}')

        # Annotate each point with the word label
        for i, label in enumerate(labels):
            plt.annotate(label, (x[i], y[i]), color=colors(cluster_id) if mode == "" else colors(actualSemCat[label] if mode == 'sem' else actualOrigins[label]), textcoords="offset points", xytext=(0,0), va='center', ha='center')

    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=f'Cluster {i}' if mode == "" else (f'{catArr[i]}' if mode == 'sem' else f'{orgArr[i]}'),
                             markerfacecolor=colors(i), markersize=10) for i in range(len(cluster_assignment) if mode == "" else 10)]


    
    plt.title('K-Means Clustering of Word Embeddings' if mode == "" else ('Word Embeddings Colored with Manual Semantic Categories' if mode == 'sem' else 'Word Embeddings Colored with Word Origins'))
    plt.legend(handles=legend_handles)
    plt.grid(True)
    plt.show()


# option of using multilingual pretrained BERT sentence embeddings
def sentenceEmbed():

    model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

    words = getWords()

    embeddings = [(getEmbed(word, lambda w : model.encode(w)), word) for word in words]

    noneEmbeddings = [e[1] for e in embeddings if e[0] is None]
    print("Words with no embedding:")
    print(noneEmbeddings)
    print(len(noneEmbeddings))
    words = [e[1] for e in embeddings if e[0] is not None]
    embeddings = [e[0] for e in embeddings if e[0] is not None]

    cluster(words, embeddings)



# option of creating skip-gram embeddings from my corpus
def word2VecSkipGram():

    warnings.filterwarnings(action='ignore')

    #  Reads ‘alice.txt’ file
    with open('../dataEntries/frenchData.json', 'r') as file:
        # Load the JSON data into a Python dictionary
        data = json.load(file)

    s = ' '.join([d['lyrics'] for d in data['allSongs'] if d['lyrics'] != ""])
    
    # Replaces escape character with space
    f = s.replace("\n", " ")
    
    data = []
    
    # iterate through each sentence in the file
    for i in sent_tokenize(f):
        temp = []
    
        # tokenize the sentence into words
        for j in word_tokenize(i):
            temp.append(j.lower())
    
        data.append(temp)

    # now make it so that you can get each embedding and cluster it
    
    # skipGram model built
    model = gensim.models.Word2Vec(data, min_count=1, vector_size=100,
                                    window=5, sg=1)
    
    words = getWords()

    embeddings = [(getEmbed(word, lambda w : model.wv[word]), word) for word in words]

    noneEmbeddings = [e[1] for e in embeddings if e[0] is None]
    print("Words with no embedding:")
    print(noneEmbeddings)
    print(len(noneEmbeddings))
    words = [e[1] for e in embeddings if e[0] is not None]
    embeddings = [e[0] for e in embeddings if e[0] is not None]

    cluster(words, embeddings)

# options of using urban dictionary embeddings
def ud_embeddings():

    """
    # for opening urban dictionary embeddings
    import zipfile

    # expand the glove embeddings
    zip_file_path = 'embeddings/glove_embeddings.zip'

    # Extract the contents of the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall('other_temp_folder')
    """

    # Load the FastText model (only for words tho)
    model = fasttext.load_facebook_vectors('temp_folder/ud_basic.bin')

    words = getWords()

    embeddings = [(getEmbed(word, lambda w : model.get_vector(w)), word) for word in words]

    noneEmbeddings = [e[1] for e in embeddings if e[0] is None]
    print("Words with no embedding:")
    print(noneEmbeddings)
    print(len(noneEmbeddings))
    words = [e[1] for e in embeddings if e[0] is not None]
    embeddings = [e[0] for e in embeddings if e[0] is not None]

    cluster(words, embeddings)

    """
    import shutil
    shutil.rmtree('temp_folder')
    """

# option of using muse embeddings
def museWordEmbed(findSimilarWords = False, ctrlWord = "", otherWords = ""):

    # small helper to get the right path
    def getPath(lang):
        return '../../museData/MUSE/data/wiki.multi.' + lang + '.vec'

    # because the gensim doesn't work with arabic just doing this manually
    def manuallyMakeModel(lang):

        # helper to find the first non float index
        def firstNonStrInd(lineToArr):
            i = 0
            for l in lineToArr:
                try:
                    float(l)
                    return i if i > 0 else 1
                except:
                    i += 1

        with open(getPath(lang), 'r', encoding='utf-8') as f:
            num_words, dim = map(int, f.readline().split())

            # loop through the lines
            manualModel = {}
            for line in f:
                lineToArr = line.strip().split()
                firstEmbedInd = firstNonStrInd(lineToArr)
                wordToAdd = ' '.join(lineToArr[0:firstEmbedInd])
                embedToAdd = [float(e) for e in lineToArr[firstEmbedInd:]]
                # just ignore the ones that don't have the correct dimensionality
                if len(embedToAdd) != dim:
                    continue
                manualModel[wordToAdd] = embedToAdd
            
            return manualModel

    # function to load the next model (less common words)
    def loadNextModel():
        global onLang
        onLang += 1
        langToLoad = modes[onLang]
        print("LOADING " + langToLoad)
        word_vectors = KeyedVectors.load_word2vec_format(getPath(langToLoad), binary=False) if langToLoad != 'ar' else manuallyMakeModel(langToLoad)
        model[langToLoad] = word_vectors

    # to find the embedding
    def findEmbed(word):
        
        # hyphen case
        if ('-' in word) and (word.count('-') == 1):
            word1, word2 = word.split('-')
            word1Embed = findEmbed(word1)
            word2Embed = findEmbed(word2)
            if (word1Embed is None) or (word2Embed is None):
                return None
            # average of the vector sums
            return [float((word1Embed[i] + word2Embed[i]) / 2.0) for i in range(len(word1Embed))]
        
        # space case
        if (' ' in word) and (word.count(' ') >= 1):
            words = word.split(' ')
            words = [findEmbed(w) for w in words]
            if any(w is None for w in words):
                return None
            # average of the vector sums (out: loop thru cols)
            return [float(sum([words[i][j] for i in range(len(words))]) / len(words)) for j in range(len(words[0]))]

        for m in modes:
            # check if you need to load a new model
            if m not in model:
                loadNextModel()

            # attempt to find the embedding
            try:
                # this en to ar transliteration doesn't work well though
                return model[m][word if m != 'ar' else buckwalter.untransliterate(word)]
            except KeyError as e:
                continue
        return None # defaultVec


    if findSimilarWords:
        limit = 0.5
        woiEmbed = findEmbed(ctrlWord)
        if woiEmbed is None:
            return
        woiEmbed = np.array(woiEmbed)
        norm_woi = np.linalg.norm(woiEmbed)
        simWords = []
        for word in otherWords:
            otherEmbed = findEmbed(word)
            if otherEmbed is not None:
                otherEmbed = np.array(otherEmbed)
                norm_other = np.linalg.norm(otherEmbed)
                dot_prod = np.dot(woiEmbed, otherEmbed)
                similarity = dot_prod / (norm_woi * norm_other)
                if similarity >= limit:
                    simWords.append(word)
        return simWords
    else:
        # found manually because of difficulties transliterating arabic
        arabicWords = ["زِبْل", "بِالْجُزَاف", "هَيْجاء", "كلب", "قهوة", "فلوس", "السلام عليكم", "ما شاء الله", "إن شاء الله", "الحمد لله", "خلاص", "أستغفر الله", "ضحك", "أخ", "راجل", "مسكين", "حلال"]

        # initialization
        words = getWords() + arabicWords
        embeddings = [(findEmbed(word), word) for word in words]
        noneEmbeddings = [e[1] for e in embeddings if e[0] is None]
        print("Words with no embedding:")
        print(noneEmbeddings)
        print(len(noneEmbeddings))
        words = [e[1] for e in embeddings if e[0] is not None]
        embeddings = [e[0] for e in embeddings if e[0] is not None]
        cluster(words, embeddings)
    
if __name__ == "__main__":
    if mode == 0:
        print("URBAN DICTIONARY")
        ud_embeddings()
    elif mode == 1:
        print("SBERT")
        sentenceEmbed()
    elif mode == 2:
        print("WORD2VECSKIP")
        word2VecSkipGram()
    elif mode == 3:
        print("MUSE")
        museWordEmbed()