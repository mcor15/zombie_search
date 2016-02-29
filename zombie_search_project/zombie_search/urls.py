from django.conf.urls import patterns, url
from zombie_search import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
	url(r'^about', views.about, name='about'),
	url(r'^login', views.login, name='login'),
	url(r'^register', views.register, name='register'),)