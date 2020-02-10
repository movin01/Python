from django.conf.urls import url
from django.contrib import messages
from . import views
import bcrypt


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$',views.success),
    url(r'^addauthorquote$', views.addauthorquote),
    url(r"^logout$", views.logout),
    url(r"^delete/(?P<quote_id>\d+)", views.delete), 
    url(r"^editquote/(?P<quote_id>\d+)", views.editquote),
    url(r"allquotes_by_user/(?P<user_id>\d+)", views.allquotes_by_user),
    url(r'update/(?P<quote_id>\d+)', views.update),
    url(r"update", views.update),
]
 
