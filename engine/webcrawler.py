
from bs4 import BeautifulSoup 
from bs4.element import Comment
import requests 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from engine.recommender import Recommender

class Crawler:

    def __init__(self, score_threshold, page_threshold, match_threshold, url_match_threshold) -> None:
        self.stored_urls = []
        self.score_threshold = score_threshold
        self.page_threshold = page_threshold
        self.match_threshold = match_threshold
        self.url_match_threshold = url_match_threshold
        self.recommender = Recommender()

    def crawl(self, urls, query, page_number):
        start_url = urls[0]
        while urls:
            if(len(self.stored_urls) >= (self.page_threshold * (page_number+1))):
                break

            next_process = []
            for url in urls:
                text = read_text(url)
                score = self.recommender.score(text, query)
                if score > self.score_threshold:
                    if self.check_seen_urls(url, score):
                        continue
                    if url != start_url:
                        self.stored_urls.append((score,url))
                    next_process+=self.get_urls(url)

                    if(len(self.stored_urls) >= (self.page_threshold * (page_number+1))):
                        break

            urls = next_process

        self.stored_urls.sort(reverse=True)
        out_urls = self.stored_urls[self.page_threshold*page_number: self.page_threshold*(page_number+1)]
        return [get_info(url[1]) for url in out_urls]

    def check_seen_urls(self, url, score):
        for i in range(len(self.stored_urls)):
            s = self.stored_urls[i][0]
            seen_url = self.stored_urls[i][1]
            if self.match(seen_url, url) > self.match_threshold:
                if score > s:
                    self.stored_urls[i] = (score, url)
                return True
        return False

    def match(self, url1, url2):
        return self.recommender.compare(read_text(url1), read_text(url2))

    def get_urls(self, url_in):
        page = requests.get(url_in, verify=False).text
        soup = BeautifulSoup(page,'html.parser')
        listings = soup.find_all("a")
        urls = []
        for content in listings:
            try:
                url = content["href"]
            except KeyError:
                continue
            if 'google.com' in url_in:
                if url[:7] != "/url?q=" or 'support.google.com' in url_in or 'accounts.google.com' in url_in:
                    continue
                url = url[7:].split("&sa=U&ved=")[0]
            elif check_bad_url(url):
                continue

            new = True
            for seen_url in urls:
                if self.recommender.compare_url(seen_url, url) > self.url_match_threshold:
                    new = False
                    break
            
            if new:
                urls.append(url)

        return urls


def read_text(url):
    page = requests.get(url, verify=False).text
    soup = BeautifulSoup(page,'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def check_bad_url(url):
    return 'google.com' in url or 'youtube.com' in url or (url[:8] != "https://" and url[:3] != "www") or 'twitter' in url

def get_info(url):
    page = requests.get(url, verify=False).text
    soup = BeautifulSoup(page,'html.parser')
    titles = soup.findAll('title')
    metas = [meta.attrs['content'] for meta in soup.find_all('meta') if 'name' in meta.attrs and meta.attrs['name'] == 'description']

    title = "No Title Found"
    meta = "No Description Found"
    if len(titles): title = titles[0].get_text()
    if len(metas):
        meta = metas[0]
        if len(meta) > 100:
            meta = meta[:100]+"..."

    return (title, meta, url)