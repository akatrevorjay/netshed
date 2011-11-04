from xmlrpclib import ServerProxy, Error, dumps
import urllib

class SSO():

    __config_vals = {}
    connected = None
    __server = None

    def __init__(self):
        config = self.sso_config()
        for key,val in config.items():
            self.__config_vals[key] = val

        # don't know enough about this library to know
        # if a lazy connection is a good idea
        self.__connect()

    def conf(self,key):
        try: return self.__config_vals[key]
        except: return None

    def __connect(self):
        try: self.__server = ServerProxy('https://%s%s'%(self.conf('sso_host'), self.conf('sso_path')))
        except: return 0
        self.connected = 1
        return 1

    def server(self):
        if self.__connect():
            return self.__server
        else:
            return None

    def rpc_creds(self):
        return '%s:%s' % (self.conf('sso_service'), self.conf('sso_password'))

    def auth(self, sid, redirect = True, extend = True):

        # use the value of extend as the index into the (0,1) tuple
        # (simulated ternary)
        ext = (0,1)[extend]
        if( not self.__connect() ):
            return None

        response = self.server().sso.session_check(self.rpc_creds(),sid,ext)
        return response['valid']
        #@TODO process response

    def login_url(self):
        return '%s?service=%s' % (self.conf('sso_login_url'), self.conf('sso_service'))

    def logout(self, sid, destroy_session = True):
        #from django.http import HTTPResponse
        #@TODO
        # delete the cookie
        # here's the info http://djangobook.com/en/1.0/chapter12/ (for django)

        self.server().sso.session_destroy(self.rpc_creds(), sid)

    def getuserinfo(self, username):
        return self.server().sso.getuserinfo_byusername(self.rpc_creds(), username)

    def getsessionuserinfo(self, sessid):
        try:
            ssodata = self.server().sso.session_userinfo(self.rpc_creds(), sessid)
        except:
            ssodata = None
        return ssodata

    def sso_config(self, param=""): 
        config = {}

        # initialize config with default values
        if not len(config.keys()): 
            config = {
                'auto'            : '0',

                # sso auth configuration
                'sso_service'     : 'net_dmca',
                'sso_password'    : 'saeFahb1',
                'sso_host'        : 'secure.onid.oregonstate.edu',
                'sso_path'        : '/sso/rpc',
                'sso_cookie'      : 'sso',
                'logout_page'     : 'logout.php',
                'logout_redirect' : '1',
                'sso_login_url'   : 'secure.onid.oregonstate.edu/login',

                # ssesion configuration
                'sess_enable'     : '1',
                'sess_cookie'     : 'sso',
                'sess_path'       : '/',
                'sess_host'       : 'oregonstate.edu',
                'sess_length'     : '3600',
                'sess_secure'     : '0',
                'db_host'         : 'db.cws.oregonstate.edu',
                'db_username'     : '',
                'db_password'     : '',
                'db_name'         : '',
                'db_table'        : 'session',
                'db_sid_col'      : 'sid',          # expected type: varchar(32)
                'db_expire_col'   : 'expire',       # expected type: unsigned int
                'db_data_col'     : 'data'     # expected type: text
            }

        
        # retrieve entire config array
        if (param == ""): 
            return config

        # set config params: overwrite only values specified
        elif (type(param) == dict):
            for key, value in param:
                config[key] = val
            return config

        # retrieve a single config param
        else:
            if (config[param]):
                return config[param]
            else:
                return None

#for testing
if __name__ == "__main__":
    pass


