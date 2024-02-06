import gensim
from gensim.models import fasttext, Word2Vec
from gensim.test.utils import datapath
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from nltk.tokenize import sent_tokenize, word_tokenize
from sentence_transformers import SentenceTransformer

import numpy as np
import csv
import warnings
import json


# just some setting up, change type of embedding here
mode = 0

if mode == 0:
    dimensionality = 300
elif mode == 1:
    dimensionality = 512
elif mode == 2:
    dimensionality = 100
defaultVec = [0.0] * dimensionality

# get the list of borrowed words I'm interested in
def getWords():
    # generate the words in a csv file
    csv_file_path = 'borrowedWords.csv'
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
        wordData = list(csv.reader(file))

    words = [wd[0].lower() for wd in wordData[1:] if " " not in wd[0]]
    return words

# get the embedding of a word given a certain model
def getEmbed(word, function):
    try:
        return function(word)
    except KeyError as e:
        return defaultVec

# cluster the embeddings using k-means
def cluster(words, embeddings, num_clusters = 4):
    """
    # optionally dimension reduction
    numDimMin = 10
    pca = PCA(n_components = numDimMin)
    pca.fit(embeddings)
    embeddings = pca.transform(embeddings)
    """

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

    print(clustered_words)

# option of using multilingual pretrained BERT sentence embeddings
def sentenceEmbed():

    model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

    words = getWords()

    embeddings = [getEmbed(word, lambda w : model.encode(w)) for word in words]

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

    embeddings = [getEmbed(word, lambda w : model.wv[word]) for word in words]

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

    embeddings = [getEmbed(word, lambda w : model.get_vector(w)) for word in words]

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