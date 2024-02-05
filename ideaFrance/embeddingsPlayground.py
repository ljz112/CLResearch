from gensim.models import fasttext
from gensim.test.utils import datapath
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize

import numpy as np
import csv


##### TODO next: try MUSE embeddings, and glance at embedding testing options

"""
import zipfile

# expand the ud embeddings
zip_file_path = 'embeddings/ud_embeddings.zip'

# Extract the contents of the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall('temp_folder')
"""

dimensionality = 300
defaultVec = [0.0] * dimensionality

# Load the FastText model (only for words tho)
model = fasttext.load_facebook_vectors('temp_folder/ud_basic.bin')


# generate the words in a csv file
csv_file_path = 'borrowedWords.csv'
with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
    wordData = list(csv.reader(file))

words = [wd[0].lower() for wd in wordData[1:] if " " not in wd[0]]

def debugFunction(word):
    try:
        vector = model.get_vector(word)
        return vector
    except KeyError as e:
        return defaultVec

embeddings = [debugFunction(word) for word in words]

print("Got the embeddings")

embedding_array = np.array(embeddings)
# optionally normalize
# embedding_array = normalize(embedding_array)

# Number of clusters (you can adjust this based on your needs)
num_clusters = 4

# Apply K-means clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=1)
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