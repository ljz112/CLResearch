import wikipediaapi
import re
import config

def earlyText(sections, rightSection = "early life"):
    print(sections)
    for s in sections:
        if rightSection in s.title.lower():
            return remove_parentheses(s.text)
    return ""

def firstBlurb(text):
    return remove_parentheses(text.split("\n")[0])

def remove_parentheses(text):
    # Use a regular expression to remove everything inside parentheses
    cleaned_text = re.sub(r'[\u0028-\u0029\u005B-\u005D].*?[\u0028-\u0029\u005B-\u005D]', '', text)
    return cleaned_text


def getBlurbs(subject, lang):
    wiki_wiki = wikipediaapi.Wikipedia(config.WIKI_NAME, lang)
    searchName = subject.replace(' ', '_')
    page = wiki_wiki.page(searchName)
    if page.exists():
        summ_text = firstBlurb(page.summary)
        early_text = firstBlurb(earlyText(page.sections))
        # the 2 text blurbs you should analyze
        print("SUMMARY")
        print(summ_text)
        # change this early life thing
        print("EARLY LIFE")
        print(early_text)
        return [summ_text, early_text]

if __name__ == "__main__":
    print("Usually shouldn't have this called itself but ok")