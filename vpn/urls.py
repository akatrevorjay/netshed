from django.conf.urls.defaults import *

urlpatterns = patterns('vpn.views',
                      (r'^$', 'index'),
)
