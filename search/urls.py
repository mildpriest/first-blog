from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^search/(?P<word>.+)/$', views.search_result, name='search_result'),
]