from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', include('main.urls')),
    (r'^aruba/', include('aruba.urls')),
    (r'^dhcp/', include('dhcp.urls')),
    (r'^vpn/', include('vpn.urls')),
    (r'^cca/', include('cca.urls')),
    (r'^greylist/', include('greylist.urls')),
    (r'^header_reject/', include('header_reject.urls')),
    (r'^named/', include('named.urls')),
    (r'^virtualusers/', include('virtualusers.urls')),
    (r'^transport/', include('transport.urls')),
    (r'^firewall/', include('firewall.urls')),
    (r'^security/', include('security.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
)
