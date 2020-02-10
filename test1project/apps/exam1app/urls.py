from django.conf.urls import url
from django.contrib import messages
from . import views
import bcrypt


urlpatterns = [
    url(r'^$', views.index),
    url(r'^quotes$', views.quotes),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r"^logout", views.logout), 
    url(r"^addauthorquote", views.addauthorquote), 
    url(r"^delete", views.delete), 
    url(r"^editmyaccount", views.editmyaccount),
    url(r"^update", views.update), 
]

