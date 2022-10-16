import re
import math
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from difflib import SequenceMatcher
import nltk
nltk.download(["averaged_perceptron_tagger", "punkt", "vader_lexicon"])

from nltk.sentiment import SentimentIntensityAnalyzer


class Recommender:

    def __init__(self) -> None:
        pass
    #past_searchs is tuple is query and time
    @staticmethod
    def score(inputText, inputQuery):
        #Clean Input
        text = Recommender.cleanText(inputText,True)
        query = Recommender.cleanText(inputQuery,False)
        #Check for size
        if len(text) == 0: return 0
        #Check for Bad Words
        #if Recommender.containsWords(inputText,"engine/recommender_data/BadWords.txt"): return -1
        #`if Recommender.containsWords(inputText,"engine/recommender_data/BadWords.txt"): return -1
        #Calculate Score
        score = (Recommender.polarityScoring(text)+Recommender.factScoring(text))*Recommender.get_similarity(text,query)
        print(score)
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
    def polarityScoring(text):
        scores = SentimentIntensityAnalyzer().polarity_scores(text)
        return (-0.75*scores['neg'] + 0.25*scores['neu'] + 0.5*scores['pos']) / (scores['compound']+0.000001)
    
    @staticmethod
    def factScoring(text):
        if Recommender.containsWords(text,"engine/recommender_data/EducationalSites.txt"):
            return 0.5
        return 0.0

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
