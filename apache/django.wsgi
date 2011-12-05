import os
import sys
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'netshed.production_settings'

path = '/data/www/netshed'
if path not in sys.path:
    sys.path.append(path)

path = '/data/www/'
if path not in sys.path:
    sys.path.append(path)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
