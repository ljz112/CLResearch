######### IN USE FOR PROJECT


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

import numpy as np
import csv
import warnings
import json

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

# get the list of borrowed words I'm interested in
def getWords():
    # generate the words in a csv file
    csv_file_path = 'collectedData/borrowedWords.csv'
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
        wordData = list(csv.reader(file))

    # could add condition if " " not in wd[0]
    words = [wd[0].strip().lower() for wd in wordData[1:]]
    return words

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

    # print("embeddings now: ")
    # print(embeddings)
    # print("words now: ")
    # print(words)

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

    # print("Cluster assignment")
    # print(clustered_words)

    word_embeddings = [[words[i], embeddings[i]] for i in range(len(words))]

    visualize_clusters(clustered_words, word_embeddings)

# taken from chatGPT lol
def visualize_clusters(cluster_assignment, word_embeddings):
    # Initialize plot
    plt.figure(figsize=(10, 6))

    # Create a color map for clusters
    colors = plt.cm.get_cmap('tab10', len(cluster_assignment))

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
        plt.scatter(x, y, color=colors(cluster_id), label=f'Cluster {cluster_id}')
        # Annotate each point with the word label
        for i, label in enumerate(labels):
            plt.annotate(label, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.title('K-Means Clustering of Word Embeddings')
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    plt.legend()
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

    """
    # this seemed to return better results for the shorter words I'm looking for
    word0 = 'mec'
    word1 = 'homme'
    word2 = 'bro'
    
    print("Cosine similarity 1 - SkipGram : ",
        model.wv.similarity(word0, word1))
    
    print("Cosine similarity 2 - SkipGram : ",
        model.wv.similarity(word0, word2))
    """

# options of using urban dictionary embeddings
def ud_embeddings():

    """
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
    # Print the embeddings
    for word, embedding in zip(words, embeddings):
        print(f"Sentence: {word}")
        print(f"Embedding: {embedding}")
        print("------")
    """

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
            # print("HERE " + word1 + " " + word2)
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
        # print("Evaluating embeddings")
        limit = 0.5
        woiEmbed = findEmbed(ctrlWord)
        if woiEmbed is None:
            # print("No embedding for this word")
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
                    # print(word)
                    simWords.append(word)
        return simWords
    else:
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