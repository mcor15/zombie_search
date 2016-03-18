from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# At the top of your urls.py file, add the following line:
from django.conf import settings


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zombie_search_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^zombie_search/', include('zombie_search.urls')),
)


urlpatterns += staticfiles_urlpatterns()
# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
