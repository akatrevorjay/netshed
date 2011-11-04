from django.conf.urls.defaults import *

urlpatterns = patterns('dhcp.views',
                      (r'^$', 'index'),
)
