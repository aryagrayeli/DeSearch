import re
import math
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from difflib import SequenceMatcher

class Recommender:

    def __init__(self) -> None:
        pass
    #past_searchs is tuple is query and time
    @staticmethod
    def score(inputText, inputQuery, intputpast_searches):
        #Clean Input
        text = Recommender.cleanText(inputText,True)
        query = Recommender.cleanText(inputQuery,False)
        past_searches = []
        for search in intputpast_searches:
            past_searches.append((Recommender.cleanText(search[0],False),search[1]))
        #Check for size
        if len(text) == 0: return 0
        #Check for Bad Words
        #if Recommender.containsWords(inputText,"engine/recommender_data/BadWords.txt"): return -1
        #`if Recommender.containsWords(inputText,"engine/recommender_data/BadWords.txt"): return -1
        #Calculate Score
        print( str(Recommender.get_similarity(text,query)) +" "+ str(Recommender.childfriendlyScoring(text)) +" "+ str(Recommender.historicalScoring(text,query,past_searches)))
        score = (Recommender.childfriendlyScoring(text)*Recommender.historicalScoring(text,query,past_searches))**Recommender.get_similarity(text,query) 
        return score

# Similarity Check

    @staticmethod
    def get_similarity(text, query):
        q = [query]
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform([text])
        X = X.T.toarray()
        df = pd.DataFrame(X)
        q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
        # Calculate the similarity
        val = np.dot(df.loc[:, 0].values, q_vec) / np.linalg.norm(df.loc[:, 0 ]) * np.linalg.norm(q_vec)
        if val==0 : 
            return 0
        return val

    @staticmethod
    def compare(textA,textB):
        textA = Recommender.cleanText(textA,True)
        textB = Recommender.cleanText(textB,True)
        return Recommender.get_similarity(textA,textB)

# Scoring Metricologies  

    @staticmethod
    def childfriendlyScoring(text):
        totalPositiveWords = Recommender.countWords(text,"engine/recommender_data/PositiveWords.txt")
        totalNegativeWords = Recommender.countWords(text,"engine/recommender_data/NegativeWords.txt")
        totalWords = totalPositiveWords + totalNegativeWords
        if totalWords == 0 :
            return 0.1
        ratio = totalPositiveWords/totalWords
        #Further Polarize ration
        return ratio

    @staticmethod
    def historicalScoring(text, query, past_searches):
        historicalScore = 0
        oldestTime = Recommender.getOldestSearch(past_searches)
        for search in past_searches:
            currentScore = Recommender.get_similarity(text,search[0])
            currentScore *= abs((float(search[1])/oldestTime))
            print(currentScore)
            if(currentScore==0): 
                currentScore = .01
            historicalScore*=currentScore
        if(historicalScore==0):
            return .1
        return historicalScore^(1/len(past_searches))
        

#Input Cleaning

    @staticmethod
    def containsWords(inputText,file):
        text = inputText.split()
        wordsfile = open(file)
        wordslist = wordsfile.readlines()
        for word in wordslist:
            word=word.replace('\n','')
            if word in text:
                return True
        return False

    @staticmethod
    def cleanText(text, checkCommonality):
        cleaned_string = ""
        wordList = text.split()
        for words in wordList:
            # Remove Unicode
            cleaned_word = re.sub(r'[^\x00-\x7F]+', ' ', words)
            # Remove Mentions
            cleaned_word = re.sub(r'@\w+', '', cleaned_word)
            # Lowercase the document
            cleaned_word = cleaned_word.lower()
            # Remove punctuations
            cleaned_word = re.sub(r'[%s]' % re.escape(string.punctuation), ' ',cleaned_word)
            # Lowercase the numbers
            cleaned_word = re.sub(r'[0-9]', '', cleaned_word)
            # Remove the doubled space
            cleaned_word = re.sub(r'\s{2,}', ' ', cleaned_word)
            if not checkCommonality or not Recommender.isCommonWord(cleaned_word):
                cleaned_string += cleaned_word + " "
        return cleaned_string
        
    @staticmethod 
    def isCommonWord(word):
        commonWordsFile = open("engine/recommender_data/MostCommonWords.txt")
        commonWordsList = commonWordsFile.readlines()
        for i in range(len(commonWordsList)):
            commonWordsList[i] = commonWordsList[i].replace('\n','')
        if word in commonWordsList:
            return True
        return False

#Miscellaneous
    @staticmethod
    def countWords(text,file):
        count = 0
        wordsfile = open(file)
        wordslist = wordsfile.readlines()
        for word in wordslist:
            word = word.replace('\n','')
            if (text.find(word) != -1):
                count = count + 1
        return count
    
    @staticmethod
    def getOldestSearch(past_searches):
        oldestTime = 0
        for search in past_searches:
            oldestTime = max(oldestTime, float(search[1]))
        return oldestTime

    def compare_url(self, url1, url2):
        return SequenceMatcher(None, url1, url2).ratio()
