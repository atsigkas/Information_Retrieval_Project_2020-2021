from nltk.stem import *
from nltk.corpus import stopwords
from multiprocessing.dummy import Pool
import math
import nltk
import string
import concurrent.futures

cachedStopWords = stopwords.words("english")

class Indexer:

    def __init__(self, docs):
        self.docs = docs
        self.doc_dict = {}
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=8)
        self.count = 0

    #--Tokenize words and removes punctuation, numbers, lowercase letters--# 
    def tokenize(self, read):
        translator = read.translate(str.maketrans('', '', string.punctuation))
        not_numbs = ''.join([i for i in translator if not i.isdigit()])
        not_numbs = not_numbs.lower()
        not_numbs = (not_numbs.encode('ascii', 'ignore')).decode("utf-8")
        nltk_tokens = nltk.word_tokenize(not_numbs)
        return nltk_tokens

    #--Deleting stop words--#
    def deleteStopWords(self, words):
        new_words = [w for w in words if w not in cachedStopWords]
        return new_words

    #--Performing lemmatization on words--#
    def lemmatization(self, words):
        lemmatizer = WordNetLemmatizer()
        result = [lemmatizer.lemmatize(w, pos='v') for w in words]
        return result

    def deletePuncts(self, read):
        puncts = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
        for i in read:
            if i in puncts:
                read = read.replace(i, ' ')
        return read

    #--Calculating TF--#
    def getTF(self, ntlk_tokens):
        tf = {}
        for word in ntlk_tokens:
            tf[word] = ntlk_tokens.count(word)/len(ntlk_tokens)
        return tf

    #--Calculating IDF--#
    def getIDF(self, doc_dict):
        idf = {}
        unique = self.getUniques(doc_dict)
        for i in unique:
            count = 0
            for j in doc_dict.values():
                if i in j:
                    count += 1
            idf[i] = math.log10(len(doc_dict)/count+1)
        return idf

    #--Calculating TFIDF--#
    def getTFIDF(self, data, idf_s):
        tfidf = {}
        for key, value in data.items():
            tfidf[key] = self.getTF(value)
        for doc, tf_values in tfidf.items():
            for token, score in tf_values.items():
                tf = score
                idf = idf_s[token]
                tf_values[token] = tf * idf
        return tfidf

    def getUniques(self, data):
        unique = []
        for i in data.values():
            unique = unique + i
        dist = nltk.FreqDist(unique)
        return list(dist.keys())

    #--Getting inverted indexer--#
    def getIndexer(self, data):
        unique = self.getUniques(data)
        indexer = {}
        for w in unique:
            for docs, token in data.items():
                if w in token:
                    if w in indexer.keys():
                        indexer[w].append(docs)
                    else:
                        indexer[w] = [docs]
        return indexer

    def processDoc(self):
        for i in self.docs:
            tokens = self.tokenize(i.get_text())
            final_doc = self.lemmatization(tokens)
            self.doc_dict[i.get_num()] = final_doc


    def runMultithread(self):
        self.processDoc()
        return self.doc_dict

    def getDict(self):
        return self.doc_dict
