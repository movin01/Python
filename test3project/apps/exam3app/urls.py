from django.conf.urls import url
from django.contrib import messages
from . import views
import bcrypt


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^appointments$',views.appointments),
    url(r'^addappointmentpage$', views.addappointmentpage),
    url(r"^createappointment$", views.createappointment),
    url(r"^logout$", views.logout),
    url(r"^delete/(?P<apointment_id>\d+)", views.delete), 
    url(r"^editappointment/(?P<apointment_id>\d+)", views.editappointment),
    url(r"^editappointmentpage/(?P<apointment_id>\d+)", views.editappointmentpage),
    url(r"^update/(?P<apointment_id>\d+)$",views.update),
#     url(r"^update$", views.update),
]
 
