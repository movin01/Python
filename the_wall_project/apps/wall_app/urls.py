from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^wall$', views.wall),
    url(r'^create_user$', views.create_user),
    url(r'^destroy_session$', views.logout),
    url(r'^login$', views.login),
    url(r'^post_message$', views.post_message),
    url(r'^post_comment$', views.post_comment),
    url(r'^destroy_message$', views.destroy_message)
]