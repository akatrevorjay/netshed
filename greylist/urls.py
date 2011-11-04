from django.conf.urls.defaults import *

urlpatterns = patterns('greylist.views',
                      (r'^$', 'index'),
)
