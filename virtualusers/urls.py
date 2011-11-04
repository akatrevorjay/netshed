from django.conf.urls.defaults import *

urlpatterns = patterns('virtualusers.views',
                      (r'^$', 'index'),
)
