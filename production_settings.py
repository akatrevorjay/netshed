# Django settings for netshed project.
import os
from lib.utilities import connect_mongo_session

connect_mongo_session()

GREYLIST_HOST = ''
GREYLIST_USER = ''
GREYLIST_PASS = ''
GREYLIST_DB   = ''

DATABASES = {
    'default': {
        'USER': 'dummy',
        'NAME': 'dummy', 
        'HOST': 'localhost',
        'ENGINE': 'dummy', 
        'USER': 'dummy',
        'PASSWORD': '',
    },

    'dmca': {
        'NAME': '*',
        'HOST': '*',
        'ENGINE': 'django.db.backends.mysql',
        'USER': '*',
        'PASSWORD': '*',
        'PORT': *,
    },

    'net': {
        'NAME': '*',
        'HOST': '*',
        'ENGINE': 'django.db.backends.mysql',
        'USER': '*',
        'PASSWORD': '*',
        'PORT': *,
    },
}

SESSION_ENGINE = "mongoengine.django.sessions"

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Los_Angeles'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_DOC_ROOT = os.path.join(os.path.abspath(os.getcwd()), 'site_media')

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = '-!ntxfqaj16d&p_8otere67@&ttw)zo8haa@j*l+x#8gpx55yx'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'netshed.middleware.authentication.SingleSignOnMiddleware',
    'netshed.middleware.development.DevelopmentMiddleware',
)

ROOT_URLCONF = 'netshed.urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.sessions',
    'main',
    'dhcp',
    'vpn',
    'cca',
    'greylist',
    'header_reject',
    'named',
    'firewall',
    'virtualusers',
    'transport',
    'security',
)

LOCAL = False
DHCP_DIR = 'dhcp'
VPN_DIR = 'vpn'
CCA_DIR = 'cca'
GREYLIST_DIR = 'greylist'
HEADER_REJECT_DIR = 'header_reject'
NAMED_DIR = 'named'
VIRTUALUSERS_FILE = '/data/www/netshed/site_media/virtualusers.orst.static'
TRANSPORT_FILE = '/data/www/netshed/site_media/smtp_transport.static'
IS_DIR = '/var/log/fw/ISsvcs-FW/'
PBSF_DIR = '/var/log/fw/PBSFsvcs-FW/'
FIREWALL_DIR = '/var/log/fw/'
