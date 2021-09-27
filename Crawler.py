from bs4 import BeautifulSoup as bs
from queue import Queue, Empty
from urllib.parse import urljoin, urlparse
from Docs import Docs
import requests
import concurrent.futures
import time
import os

document_dict = {}
decline_list = ['filter', '?', 'jpg', 'png', 'tags', 'category']
black_list = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script']

class Crawler:

    def __init__(self, start_url, pages_to_crawl, flag, threads):
        self.urlDocs = []
        self.counter = 0
        self.url_dict = {}
        self.starting_url = start_url
        self.pages_to_crawl = pages_to_crawl
        self.starting_url = start_url
        # Scheme: 0 index "http or https"
        # Netloc: 1 index "in.gr" in our example
        self.root_url = '{}://{}'.format(urlparse(self.starting_url).scheme, urlparse(self.starting_url).netloc)
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=threads)
        self.scraped_pages = set([])
        self.to_crawl = Queue()
        self.to_crawl.put(self.starting_url)
        self.run()

    def linksParse(self, html):
        soup = bs(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            url = link['href']
            '''Reformating url. It returns category links like: '/category/life/pet-stories/'
               that's why we format it to: 'starting_url/category/life/pet-stories/' '''
            if url.startswith('/') or url.startswith(self.root_url):
                url = urljoin(self.root_url, url)
                if url not in self.scraped_pages:
                    self.to_crawl.put(url)
        return

    def postCallback(self, url):
        result = url.result()
        try:
            if result.status_code == 200:
                ''' Adding all the functionality.
                    While we successfully parsed the url, we can access the links and text'''
                self.linksParse(result.text)
                self.infoParse(result.text, result.url)
        except AttributeError:
            print("ERROR: Bad Response")
        return

    def scrape_page(self, url):
        try:
            request = requests.get(url)
            return request
        except requests.RequestException:
            print("None")
            return None

    def infoParse(self, html, url):
        soup = bs(html, "html.parser")
        text = "{} ".format(self.counter)
        self.url_dict[self.counter] = url

        for para in soup.find_all('p'):
            text += "{} ".format(para.get_text())
        text = ' '.join(text.split())
        self.urlDocs.append(Docs(self.counter, url, text))
        text += '\n'
        self.counter += 1

    @staticmethod
    def check_decline_characters(url):
        for i in decline_list:
            if i in url:
                return False
        return True

    def run(self):
        i = 0
        while i < self.pages_to_crawl:
            try:
                target_url = self.to_crawl.get()
                if (target_url not in self.scraped_pages) and self.check_decline_characters(target_url):
                    i += 1
                    print("Scraped URL: {} {}".format(i, target_url))
                    self.scraped_pages.add(target_url)
                    job = self.thread_pool.submit(self.scrape_page, target_url)
                    '''The returning attribute from the above line goes below
                        as attribute to the callback function'''
                    job.add_done_callback(self.postCallback)
                    time.sleep(0.1)

            except Empty:
                print("There are no more links!")
                return
            except Exception as e:
                print(e)
                continue

    def letsContinueCrawling(self, starting_url, pages_to_crawl, flag, threads):
        if flag == 0:
            self.urlDocs = []
        
        self.starting_url = starting_url
        self.pages_to_crawl = pages_to_crawl
        self.root_url = '{}://{}'.format(urlparse(self.starting_url).scheme, urlparse(self.starting_url).netloc)
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=threads)
        self.scraped_pages = set([])
        self.to_crawl = Queue()
        self.to_crawl.put(starting_url)
        self.run()