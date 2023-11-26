import spacy
import wikiReader

# plan for parsing is on the google doc, in english for now
nlp = spacy.load("en_core_web_sm")

#code here (check that boolean)
def getRoots(text):
    doc = nlp(text)
    allRoots = []
    onlyParents = False
    for s in doc.sents:
        inSentence = []
        for e in s.ents:
            if e.label_ == 'NORP':
                if onlyParents:
                    referring = e.root.head.text.lower()
                    # maybe check if word2vec embedding is similar to the following words
                    hotWords = ['mother', 'father', 'parent', 'descent', 'ancestry', 'origin']
                    if any([(hw in referring) for hw in hotWords]):
                        inSentence.append(e.text)
                else:
                    inSentence.append(e.text)
        if inSentence == []:
            onlyParents = True
        allRoots += inSentence
    return allRoots

name = 'Ben Shapiro'

summ_txt, early_txt = wikiReader.getBlurbs(name)
print("AFTER ALG")
endList = list(set(getRoots(summ_txt) + getRoots(early_txt)))
print(endList)
