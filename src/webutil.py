import json
import webapp2
import base64
import logging

class Error(Exception):
    """ Error """

class HttpError(Error):
    def __init__(self, code):
        self.code = code

class UnauthorizedError(HttpError):
    def __init__(self):
        super(UnauthorizedError, self).__init__(401)

class NotFoundError(HttpError):
    def __init__(self):
        super(NotFoundError, self).__init__(404)

def trim(string):
    if string == None:
        return None
    string = str(string).strip()
    if len(string) == 0:
        return None
    return string

class BaseHandler(webapp2.RequestHandler):

    def secure(self):
        return False

    def dispatch(self):
        try:
            if self.secure():
                self.check_user()
            super(BaseHandler, self).dispatch()
        except HttpError, e:
            self.response.set_status(e.code)
            self.resp_text('Error: %i\n' % e.code)
    
    def req_json(self):
        string = trim(self.request.body)
        if string == None:
            return None
        return json.loads(string)


    def resp_text(self, obj):
        self.response.headers['Content-Type'] = 'text/plain; charset=UTF-8'
        self.response.out.write(obj)

    def resp_json(self, obj):
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.response.out.write(json.dumps(obj, indent=True) + '\n')

    def req_header(self, name):
        return trim(self.request.headers.get(name))

    def req_user(self):
        header = self.req_header('Authorization')
        if header == None:
            return None
        header = header.replace('Basic ', '')
        header = base64.b64decode(header)
        header = header.split(':')
        username = trim(header[0])
        password = trim(header[1])
        if username == None:
            return None
        return { "username": username, "password": password }

    def is_cron(self):
        header = self.req_header('X-AppEngine-Cron')
        if header == 'true':
            return True
        return False

    def check_user(self):
        if self.is_cron():
            logging.info('auth cron')
            return
        user = self.req_user()
        if user == None:
            raise UnauthorizedError()
        if user['username'] != 'admin' and user['password'] != 'wr4th0fg0ds':
            raise UnauthorizedError()
        logging.info('auth basic %s', user['username'])

    def param(self, name):
        return trim(self.request.get(name))