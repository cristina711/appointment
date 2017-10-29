from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^appointments/$', views.appointments),
    url(r'^appointments/add$', views.add_appointment),
    url(r'^appointments/(?P<appointment_id>\d+)/edit$', views.edit_appointment),
    url(r'^appointments/(?P<appointment_id>\d+)/update$', views.update_appointment),
    url(r'^appointments/(?P<appointment_id>\d+)/delete$', views.delete_appointment),
]