from django.http import HttpResponseRedirect, HttpResponse
import xmlrpclib
import sso
from django.core.exceptions import ObjectDoesNotExist

class SingleSignOnMiddleware(object):

    def process_request(self, request):

        sso_class = sso.SSO()
        sid = request.COOKIES.get('sso', '')        
        
        valid = sso_class.auth(sid)
        
        if valid:
            username = sso_class.getsessionuserinfo(sid)['userinfo']['username']
            request.session['username'] = username
        else:
            return HttpResponseRedirect("https://" + sso_class.login_url())

    def logout(self, sid):
        sso_class = sso.SSO()

        sso_class.logout(sid)

    def valid_user(self, username):
        sso_class = sso.SSO()

        try:
            sso_class.getuserinfo(username)
        except:
            return False
        return True
            

    
