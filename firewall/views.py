from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from lib.utilities import format_query_output
import time
import re
import os

def index(request):
    """ simple (regex) grep of firewall logs """

    query = dict([(str(param), str(val)) for param, val in request.GET.iteritems() if val])

    search_time = 0
    logfile = ''
    loglines = []
    if 'date' in query:
        if query['date'] == 'all':
            logfile = settings.FIREWALL_DIR + query['log_type'] + '/' + query['log_type'] + '.log'
        else:
            logfile = settings.FIREWALL_DIR + query['log_type'] + '/' + query['date'] + '.log'

        start = time.time()
        lines = read_line_generator(logfile)
        for line in lines:
            if re.search(query['filter'], line):
                loglines.append(line)
            if not line:
                break
        search_time = time.time()

    dates = get_log_window(settings.IS_DIR)

    return render_to_response('firewall/index.html', {'query': format_query_output(query), 'dates':dates, 'loglines':loglines, 'time': search_time})

def get_log_window(log_dir):
    """ Returns dates in which there are firewall logs for """

    files = sorted(os.listdir(log_dir))
    dates = []
    # Get the dates of the logs
    for file in files:
        date = file.split('.')[0]
        dates.append(str(date))
    # Sort most recent first
    dates = sorted(dates, reverse=True)
    try:
        dates.remove('log')
    except:
        pass
    return dates

def read_line_generator(logfile):
    fd = open(logfile)
    while True:
        line = fd.readline()
        if line:
            yield line
        else:
            break
