from nis import match
from django.shortcuts import render

from engine.database import get_personalized_data
from engine.webcrawler import Crawler

score_threshold = 0.1
page_threshold = 5
match_threshold = 0.8
url_match_threshold = 0.8


def query(request):
    return render(request, 'engine/home.html')
    
def results(request):
    context = None
    if request.method == "POST":
        query = request.POST.get('search')
        context = get_page(query, 0)

    if context is None:
        return render(request, 'engine/results.html')
    return render(request, 'engine/results.html', context)

def next(request):
    context = None
    if request.method == "POST":
        query = request.POST.get('search')
        page_number = request.POST.get('pageNumber')
        if page_number == "": page_number = 0
        else: page_number = int(page_number)
        context = get_page(query, page_number+1)

    if context is None:
        return render(request, 'engine/results.html')
    return render(request, 'engine/results.html', context)

def prev(request):
    context = None
    if request.method == "POST":
        query = request.POST.get('search')
        page_number = request.POST.get('pageNumber')
        if page_number == "": page_number = 0
        else: page_number = int(page_number)
        context = get_page(query, max(0,page_number-1))

    if context is None:
        return render(request, 'engine/results.html')
    return render(request, 'engine/results.html', context)

def get_page(query, page_number):
    if query == "":
        return None
    else:
        # get starting urls
        urls = ['https://google.com/search?q='+query]

        # load personalized data
        
        # crawl web
        crawler = Crawler(score_threshold, page_threshold, match_threshold, url_match_threshold)
        results = crawler.crawl(urls, query, page_number) # each item is (title, description, url)
        
        context = {
            'results':results,
            'query': query,
            'pageNumber': page_number
        }
        return context

def about(request):
    return render(request, 'engine/about.html')