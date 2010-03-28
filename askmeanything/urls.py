from django.conf.urls.defaults import *

urlpatterns = patterns('askmeanything.views',
    (r'^(?P<pollid>\d+)/$', 'show'),
    (r'^(?P<pollid>\d+)/results/$', 'results'),
    (r'^(?P<pollid>\d+)/vote/$', 'vote'),
    (r'^new/$', 'new'),
    (r'^(?P<pollid>\d+)/publish/$', 'publish'),
)