import sys
import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:

    BANNED_SITE = -sys.float_info.max
    BANNED_SEARCH = -sys.float_info.max+1
    def __init__(self) -> None:
        pass
    #past_searchs is tuple is query and time
    def score(self, text, query, past_searches):
        score=0
        if self.containsBadWord(text): 
            return self.BANNED_SITE
        if self.containsBadWord(query):
            return self.BANNED_SEARCH
        text = self.filterCommonWords(text)
        
        score = math.log(self.similarityScoring(text,query)) + math.log(self.historicalScoring(text,query,past_searches)) + math.log(self.childfriendlyScoring(text))
        return score
    
    def similarityScoring(self,text,query):
        compareValue = self.compare(text,query)
        if(compareValue==0):
            compareValue = 0.00000000001
        return 1/(self.compare(text,query))

    def childfriendlyScoring(self, text):
        text = self.filterCommonWords(text)
        score = 0
        wordscoring=0
        #Positive Words
        wordscoring += self.countWords(text,"PositiveWords.txt")
        #Negative Words
        wordscoring += .5*self.countWords(text,"NegativeWords.txt")
        wordscoring /= len(text)
        return wordscoring
    
    def historicalScoring(self, text, query, past_searches):
        historicalScore = 0
        for search in past_searches:
            currentScore = 0
            currentScore += 1/search[1]
            currentScore += 1 - self.compare(query,search[0])
            historicalScore += math.log(currentScore*currentScore)
        return historicalScore


    def compare(self, textA, textB):
        corpus=[textA,textB]
        tfidf_vectorizer=TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
        return cosine_similarity(tfidf_matrix,tfidf_matrix)[0][1]

    def filterCommonWords(self, text):
        commonwordsfile = open("MostCommonWords.txt")
        commonwordslist = commonwordsfile.readlines()
        for commonword in commonwordslist:
            text=text.replace(commonword,"")
        return text

    def containsBadWord(self,text):
        badwordsfile = open('BadWords.txt')
        badwordslist = badwordsfile.readlines()
        for badword in badwordslist:
            badword=badword.replace('\n','')
            if (text.find(badword) != -1):
                return True
        return False


    def countWords(self,text,file):
        count = 0
        wordsfile = open(file)
        wordslist = wordsfile.readlines()
        for word in wordslist:
            word = word.replace('\n','')
            if (text.find(word) != -1):
                count= count + 1
        return count
    