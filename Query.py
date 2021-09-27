from Indexer import Indexer
import numpy as np

class Query:

    def __init__(self, dict_doc, idf, tfidf):
        self.dict_doc = dict_doc

        self.idf = idf
        self.docs_tf_idf = tfidf
        self.query_idf = {}
        self.query_tf = {}
        self.query_tf_idf = {}

        self.query = []
        self.relevant_docs = []
        self.cos_sim = {}
        self.runQuery()

    def getInput(self):
        self.query = str(input("Please, insert your query: ")).lower().split(' ')

    def preprocessQuery(self):
        #--Passing the inverted indexer--#
        self.getInput()
        #--Query's TF--#
        self.calcQueryTF()
        #--Finding relevant docs--#
        self.findRelevantDocs()
        #--Query's TFIDF--#
        self.calcTFIDF()
        self.calcCosineSimilarity()


    #--Calculating the TF of the query--#
    def calcQueryTF(self):
        for word in self.query:
            self.query_tf[word] = self.query.count(word)/len(self.query)

    #--Relevant documents including the query--#
    def findRelevantDocs(self):
        to_delete = []
        for word in self.query:
            try:
                for rel_doc in self.dict_doc[word]:
                    if rel_doc not in self.relevant_docs:
                        self.relevant_docs.append(rel_doc)
            except KeyError:
                print("Opps, the query: {} ,isn't found in documents".format(word))
                to_delete.append(word)

    #--Calculating the TFIDF of the query--#
    def calcTFIDF(self):
        for word in self.query:
            try:
                self.query_tf_idf[word] = self.idf[word] * self.query_tf[word]
            except KeyError:
                self.query_tf_idf[word] = 0

    def calcCosineSimilarity(self):
        for doc in self.relevant_docs:
            doc_vector = []
            query_vector = []
            for word in self.query:
                    # Take the relevant doc
                    doc_tfidf = self.docs_tf_idf[doc]
                    # From the relevant doc take the td-idf of the word
                    try:
                        doc_vector.append(doc_tfidf[word])
                    except KeyError:
                        doc_vector.append(0)
                    # From the Query take the tf-idf of the word
                    try:
                        query_vector.append(self.query_tf_idf[word])
                    except KeyError:
                        query_vector.append(0)

            self.cos_sim[doc] = self.someCalcs(doc_vector, query_vector)

    def someCalcs(self, x1, x2):
        sums = sum(x[0]*x[1] for x in zip(x1, x2))
        norm = np.linalg.norm(x1) * np.linalg.norm(x2)
        return sums/norm

    def runQuery(self):
        self.preprocessQuery()

    def topK(self, dic_doc, k):
        counter = 1
        sorted_dic = {key: value for key, value in sorted(self.cos_sim.items(), key=lambda item: item[1], reverse=True)}
        for i in sorted_dic.keys():
            print(counter, ": ", dic_doc[i].get_url())
            if counter >= k or counter > len(sorted_dic):
                return
            counter += 1
        relevance = input("Which docs were more relevant?\nType [Ex. 0 2 9]--> ")
        return
