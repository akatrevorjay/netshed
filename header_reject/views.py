from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from lib.utilities import pymongo_query, format_query_output, get_log_window

def index(request): 
    """ GET request to mongoengine db queries """            
                 
    query = dict([(str(param), str(val).lower()) for param, val in request.GET.iteritems() if val])
    
    # generic pymongo query from utilities
    loglines = pymongo_query(query, 'header_reject', settings.LOCAL)

    dates = get_log_window(settings.HEADER_REJECT_DIR, settings.LOCAL)
    return render_to_response('header_reject/index.html', {'query': format_query_output(query), 'dates':dates, 'loglines':loglines})

