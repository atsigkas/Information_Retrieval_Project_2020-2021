import Crawler
import Query
import time
import Indexer

def main(inputCrawl):
    answerTaken = ''
    ourCrawler = Crawler.Crawler(inputCrawl[0], int(inputCrawl[1]), int(inputCrawl[2]), int(inputCrawl[3]))
    
    #-- Below we are executing the crawl, the indexer and the query--#
    while True:
        time.sleep(5)

        ourIndexer = Indexer.Indexer(ourCrawler.urlDocs)
        prosessors = ourIndexer.runMultithread()
        end1 = time.time()
        invDocFreq = ourIndexer.getIDF(prosessors)
        resultsOfTFIDF = ourIndexer.getTFIDF(prosessors, invDocFreq)
        dicFinal = ourIndexer.getIndexer(prosessors)
        end2 = time.time()

        #--Taking the given query--#
        ourQuery = Query.Query(dicFinal, invDocFreq, resultsOfTFIDF)

        #--Top k results user wants--#
        numOfTopKresults = int(input("Please insert the number of results that you want: "))
        ourQuery.topK(ourCrawler.urlDocs, numOfTopKresults)

        #-- Asking to continue the whole process {crawling/indexing/query}--#
        answerTaken = str(input("Do you wish to keep searching?\nType [Yes / No]--> ")).lower()
        if answerTaken == 'yes':
            inputCrawl = str(input("OK, please insert your crawl search,\nagain Type [URL PagesNum 0/1 ThreadsNum]: ")).split()
            ourCrawler.letsContinueCrawling(inputCrawl[0], int(inputCrawl[1]), int(inputCrawl[2]), int(inputCrawl[3]))
        else:
            break

def flask_main(inputCrawl):
    top_k = 10

    ourCrawler = Crawler.Crawler(inputCrawl[0], int(inputCrawl[1]), int(inputCrawl[2]), int(inputCrawl[3]))

    #--Below we are executing only the crawl--#
    while True:
        time.sleep(5)

        ourIndexer = Indexer.Indexer(ourCrawler.urlDocs)
        prosessors = ourIndexer.runMultithread()
        end1 = time.time()
        idf = ourIndexer.getIDF(prosessors)
        tf_idf_results = ourIndexer.getTFIDF(prosessors, idf)
        final_dic = ourIndexer.getIndexer(prosessors)
        end2 = time.time()

        return ourCrawler.scraped_pages


if __name__ == '__main__':
    inputForCrawling = str(input("Please insert your crawl search,\nType [URL PagesNum 0/1 ThreadsNum]: ")).split()
    main(inputForCrawling)


