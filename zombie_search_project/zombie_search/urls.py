from django.conf.urls import patterns, url
from zombie_search import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import password_reset

urlpatterns = patterns('',
    url(r'^$', views.init_leaderboard, name='home'),
    url(r'^play/$', views.splash, name='splash_screen'),
	url(r'^game/(?P<houseNumber>[\w\-]+)/(?P<roomNumber>[\w\-]+)/(?P<action>[\w\-]+)/$', views.game, name='game'),
    url(r'^profile/(?P<user_slug>[\w\-]+)/$', views.profile, name ='profile'),
	url(r'^update/', views.update, name='update'),
	url(r'^about/$', views.about, name='about'),
	url(r'^login/$', views.player_login, name='login'),
	url(r'^register/$', views.register, name='register'),
	url(r'^logout/$', views.player_logout, name='logout'),
    url(r'^change_password/$', views.password_change ,name='change_password'),
    #password recory urls
    url(r'^reset/$', views.reset, name='reset'),
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.reset_confirm, name='password_reset_confirm'),
    url(r'^reset/sent/$', auth_views.password_reset_done, name='password_reset_done'),

    url(r'^load_leaderboard/$', views.init_leaderboard, name='update_leaderboard'),
    url(r'leader/$',views.init_board,name="home"),
    url(r'render_players/$',views.update_board,name="home"),
	)
