from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^sign/up/$', sign_up, name='sign_up'),
    url(r'^sign/up/process/$', sign_up_process, name='sign_up_process'),
    url(r'^sign/up/success/$', sign_up_success, name='sign_up_success'),

    url(r'^sign/in/$', sign_in, name='sign_in'),
    url(r'^sign/in/process/$', sign_in_process, name='sign_in_process'),

    url(r'^sign/out/$', log_out, name='logout'),

    url(r'^follow/new_user/$', follow, name='follow'),
    url(r'^unfollow/new_user/$', unfollow, name='unfollow')
]
