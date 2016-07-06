from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^sign/up/$', sign_up, name='sign_up'),
    url(r'^sign/up/process/$', sign_up_process, name='sign_up_process'),
    url(r'^sign/up/success/$', sign_up_success, name='sign_up_success'),
    url(r'^sign/in/$', sign_in, name='sign_in'),
    url(r'^sign/in/process/$', sign_in_process, name='sign_in_process'),
    url(r'^sign/out/$', log_out, name='logout'),
    # this url is called via the ajax method with data
    url(r'^follow/new_user/$', follow, name='follow'),
    # this method is not a ajax method but a custom one
    url(r'^unfollow/(?P<pk>\d+)/$', unfollow, name='unfollow'),
    # following the mysite url rules, this page will be found at "user/list"
    url(r'^following_list/$', following_list, name='following_list'),
    url(r'^follower_list/$', follower_list, name='follower_list'),
    # following and follower profiles
    url(r'^following_profile/(?P<pk>\d+)/$', following_profile, name='following_profile'),
    url(r'^follower_profile/(?P<pk>\d+)/$', follower_profile, name='follower_profile'),
    # simnple profile page url
    url(r'^profile/(?P<pk>\d+)/$', profile, name='profile'),
]
