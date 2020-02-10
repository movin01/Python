from django.conf.urls import url
from django.contrib import messages
from . import views
import bcrypt


urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r"^logout", views.logout), 
]