from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def search(request):
    return render(request, 'search/default.html', {})


def search_result(request, word):
    url = 'http://search.daum.net/search?w=tot&q=' + word
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    objects = soup.findAll('a', attrs={'class': 'f_link_b'})

    results = []

    for obj in objects:
        result = {'title': obj.text, 'link': obj['href']}
        results.append(result)

    return render(request, 'search/result.html', {'results': results, 'word': word, 'url': url})
