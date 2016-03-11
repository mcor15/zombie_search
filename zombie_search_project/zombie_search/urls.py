from django.conf.urls import patterns, url
from zombie_search import views

urlpatterns = patterns('',
    url(r'^$', views.total_kills, name='home'),
    url(r'^total_kills/$', views.total_kills, name='home'),
	url(r'^most_kills/$', views.most_kills, name='home'),
	url(r'^total_days/$', views.total_days, name='home'),
	url(r'^avg_days/$', views.avg_days, name='home'),
    url(r'^play/$', views.splash, name='splash_screen'),
	url(r'^game/$', views.game, name='game'),
    url(r'^profile/(?P<user_slug>\w+)/$', views.profile, name ='profile'),
	url(r'^about/$', views.about, name='about'),
	url(r'^login/$', views.player_login, name='login'),
	url(r'^register/$', views.register, name='register'),
	url(r'^logout/$', views.player_logout, name='logout'),
	)