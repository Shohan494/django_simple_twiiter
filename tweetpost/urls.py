from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'tweet/$', tweet, name='tweet'),
    url(r'hashtag/$', hashtag_search, name='hashtag_search'),
]
