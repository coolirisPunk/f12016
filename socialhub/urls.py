from .views import *
from django.conf.urls import patterns, url, include

urlpatterns = [
    url(r'^$', getposts, name='home'),
    url(r'^get-picture-facebook/$', get_picture_facebook, name='get-picture-facebook'),
]

