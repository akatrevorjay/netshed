from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

def index(request):

    fd = open(settings.VIRTUALUSERS_FILE)
    virtualusers = fd.readlines()
    
    return render_to_response('virtualusers/index.html', {'virtualusers':virtualusers})
