from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from lib.utilities import pymongo_query, format_query_output, get_log_window, format_query_input
from netshed.greylist.models import Greylist

def index(request):
    """ GET request to mongoengine db queries """

    query = dict([(str(param), str(val).lower()) for param, val in request.GET.iteritems() if val])

    loglines = []
    db_results = ''
    if 'search' in query:
        if query['search'] == 'search':

            # generic pymongo query from utilities
            loglines = pymongo_query(query, 'greylist', settings.LOCAL)

        # greylist database search
        elif query['search'] == 'database query':
            del query['date']
            del query['search']
            db_results = Greylist.objects.filter(**format_query_input(query))

    dates = get_log_window(settings.DHCP_DIR, settings.LOCAL)
    return render_to_response('greylist/index.html', {'db_results': db_results, 'query': format_query_output(query), 'dates':dates, 'loglines':loglines})

