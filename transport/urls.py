from django.conf.urls.defaults import *

urlpatterns = patterns('transport.views',
                      (r'^$', 'index'),
)
