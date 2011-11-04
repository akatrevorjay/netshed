from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

def index(request):

    fd = open(settings.TRANSPORT_FILE)
    transport = fd.readlines()
    
    return render_to_response('transport/index.html', {'transport':transport})
