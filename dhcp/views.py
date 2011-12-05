from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from lib.utilities import pymongo_query, get_log_window, format_query_output
import time

def index(request):
    """ GET request to mongoengine db queries """

    query = dict([(str(param), str(val).lower()) for param, val in request.GET.iteritems() if val])

    # generic pymongo query from utilities
    start = time.time()
    loglines = pymongo_query(query, 'dhcp', settings.LOCAL)
    search_time = time.time() - start

    dates = get_log_window('dhcp', settings.LOCAL)
    return render_to_response('dhcp/index.html', {'query': format_query_output(query), 'dates':dates, 'loglines':loglines, 'time':search_time})

