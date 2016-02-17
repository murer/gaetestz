URL = 'http://localhost:8085'
def func():
    response = urlopen(URL)
    return response.read()

import unittest
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
import threading
from urllib2 import urlopen
from cStringIO import StringIO

def app_200_hello(environ,start_response):
    stdout = StringIO('Hello world')
    start_response("200 OK", [('Content-Type','text/plain')])
    return [stdout.getvalue()]

server = WSGIServer(('localhost', 8085), WSGIRequestHandler)
server.set_app(app_200_hello)

t = threading.Thread(target=server.serve_forever)
t.start()

class TestFunc(unittest.TestCase):
    def setUp(self):
        pass

    def test1(self):
        r = func()
        self.assertEqual(r, 'Hello world')

    def __del__(self):
        server.shutdown()

if __name__ == '__main__':
    unittest.main()
