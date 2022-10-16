
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

COMMON_WORDS = set()
file = open('engine/common_words.txt', 'r')
lines = file.readlines()
for line in lines:
    COMMON_WORDS.add(line.strip())

class Recommender:

    def __init__(self) -> None:
        pass

    def score(self, text, query, past_searches):
        t = text.split(" ")
        c = 0.0
        other = 0.0
        for word in t:
            if word in COMMON_WORDS and word != query:
                continue
            if similar(word, query) > 0.75:
                c+=1.0
            else:
                other+=1.0

        if c > 50: other = min(50*500, other)
        return c / other

    def compare(self, text1, text2):
        return similar(text1,text2)

    def compare_url(self, url1, url2):
        return similar(url1, url2)