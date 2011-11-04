from django.conf.urls.defaults import *

urlpatterns = patterns('security.views',
                      (r'^$', 'index'),
)
