from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def search(request):
    return render(request, 'search/default.html', {})


def search_result(request, word):
    req = requests.get('http://search.daum.net/search?w=tot&q=' + word)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    objects = soup.findAll('a', attrs={'class': 'f_link_b'})

    results = []

    for obj in objects:
        # results[obj.text] = obj
        result = {'title': obj.text, 'link': obj['href']}
        results.append(result)

    return render(request, 'search/result.html', {'results': results, 'word': word})
