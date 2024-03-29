from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^getConcerts', 'hearapp.views.getConcerts'),
    url(r'^getConcerts/(\d{7})$', 'hearapp.views.getConcerts'),
    url(r'^getSetlist/(.*)$', 'hearapp.views.getSetlist'),
    url(r'^$', 'hearapp.views.index', name='home'),
    url(r'^ajax/venues$', 'hearapp.views.getVenues'),
    # url(r'^wuzhear/', include('wuzhear.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
