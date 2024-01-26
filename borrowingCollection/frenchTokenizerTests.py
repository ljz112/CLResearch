import nltk
from nltk.tokenize import word_tokenize
import spacy
from fuzzywuzzy import fuzz

# Download the punkt tokenizer for French
# nltk.download('punkt')
nlp = spacy.load("fr_core_news_sm")

# Sample French text
french_text = "Ce sentiment d'kiffer."

# Tokenize the text
# tokens = word_tokenize(french_text, language='french')
tokens = nlp(french_text)

# Print the list of tokens
print("List of tokens:")
for token in tokens:
    # print(token)
    print(token.text)

substring = "petit"
larger_string = "J'suis trop p'tit"
fr = fuzz.partial_ratio(substring, larger_string)
print(fr)