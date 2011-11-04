from django.conf.urls.defaults import *

urlpatterns = patterns('firewall.views',
                      (r'^$', 'index'),
)
