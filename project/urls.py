from django.conf.urls.defaults import *
from django.contrib import admin
import authority

admin.autodiscover()
authority.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^polls/', include('project.askmeanything.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^authority/', include('authority.urls')),
)
