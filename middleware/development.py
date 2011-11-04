
class DevelopmentMiddleware(object):

    def process_request(self, request):
        request.session['username'] = 'development'
        return None
    
