from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'tweet/$', tweet, name='tweet'),
    url(r'hashtag/$', hashtag_search, name='hashtag_search'),

    url(r'^(?P<pk>\d+)/comment/$', add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', comment_remove, name='comment_remove'),
]
