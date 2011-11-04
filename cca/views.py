from django.template import RequestContext
from django.shortcuts import render_to_response
from lib.utilities import pymongo_query, format_query_output, get_log_window
from django.conf import settings

def index(request):
    """ GET request to pymongo db queries """

    query = dict([(str(param), str(val).lower()) for param, val in request.GET.iteritems() if val])

    # generic pymongo query from utilities
    loglines = pymongo_query(query, 'cca', settings.LOCAL)

    dates = get_log_window(settings.CCA_DIR, settings.LOCAL)
    return render_to_response('cca/index.html', {'query': format_query_output(query), 'dates':dates, 'loglines':loglines})

