from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^list/python/$', views.ctg_list_py, name='ctg_list_py'),
    url(r'^list/java/$', views.ctg_list_java, name='ctg_list_java'),
    url(r'^list/javascript/$', views.ctg_list_javascript, name='ctg_list_javascript'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.edit, name='edit'),
]