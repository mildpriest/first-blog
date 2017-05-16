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
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
]