from django.conf.urls.defaults import *

urlpatterns = patterns('askmeanything.views',
    (r'^(?P<poll_id>\d+)/$', 'show'),
    (r'^(?P<poll_id>\d+)/embed/$', 'embed'),
    (r'^(?P<poll_id>\d+)/results/$', 'results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'vote'),
    (r'^new/$', 'new'),
    (r'^(?P<poll_id>\d+)/publish/$', 'publish'),
)