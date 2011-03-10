from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mowish/', include('mowish.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'mowish.app.views.index', name='index'),

    url(r'^user/signup/', 'django.views.generic.simple.direct_to_template', {'template': 'signup.html'}, name='signup'),
    (r'^user/add/', 'mowish.app.views.user_add'),
    (r'^user/activate/(\w+)/$', 'mowish.app.views.user_activate'),
    (r'^user/login/', 'mowish.app.views.user_login'),
    (r'^user/logout/', 'mowish.app.views.user_logout'),
    
    (r'^movie/(\d+)/([\w-]+)/$', 'mowish.app.views.movie'),
    (r'^movie/(\d+)/$', 'mowish.app.views.movie', {'slug': ''}),
    (r'^movie/(\d+)/rate/([\w-]+)/$', 'mowish.app.views.movie_rate'),
    (r'^movie/(\d+)/status/([\w-]+)/$', 'mowish.app.views.movie_status'),
    (r'^movie/add/', 'mowish.app.views.movie_add'),
            
    (r'^person/(\d+)/([\w-]+)/$', 'mowish.app.views.person'),
    (r'^person/(\d+)/$', 'mowish.app.views.person', {'slug': ''}),    
    
    (r'^movies/list/', 'mowish.app.views.movies_list'),    
    (r'^movies/from/(\d+)/([\w-]+)/$', 'mowish.app.views.movies_from'),
    (r'^movies/from/(\d+)/$', 'mowish.app.views.movies_from', {'slug': ''}),        
    (r'^movies/recommendations/', 'mowish.app.views.movies_recommendations'),
    (r'^movies/toplist/', 'mowish.app.views.movies_toplist'),    

    url(r'^my/list/', 'mowish.app.views.my_list', name='my_list'),
    url(r'^my/profile/', 'mowish.app.views.my_profile', name='my_profile'),
    
)

# only for development purposes
if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        )    