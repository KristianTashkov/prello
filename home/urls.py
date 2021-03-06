from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login/$', views.login_request, name="login"),
    url(r'^logout/$', views.logout_request, name="logout"),
    url(r'^register/$', views.register_request, name="register"),
]
