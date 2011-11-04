from django.conf.urls.defaults import *

urlpatterns = patterns('named.views',
                      (r'^$', 'index'),
)
