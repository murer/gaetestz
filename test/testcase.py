import unittest
import httplib
import json as JSON
from gae_server_test import GaeTestServer

class Error(Exception):
    """ Error """

gae = GaeTestServer()

class TestCase(unittest.TestCase):

    def setUp(self):
        import main
        gae.boot_gae()
        gae.boot_web(8080, main.app)
        gae.server_forever_background()

    def tearDown(self):
        gae.shutdown()

def http_json(method, uri, content = None):
    conn = httplib.HTTPConnection('localhost', gae.port)
    try:
        if not content:
            req = conn.request(method, uri)
        else:
            json = JSON.dumps(content).encode('utf-8')
            req = conn.request(method, uri, json, { 'Content-Type': 'application/json; charset=utf-8' })
        resp = conn.getresponse()
        if(resp.status != 200):
            raise Error('Error on http client: %s' % (resp.status))
        json = resp.read()
        return JSON.loads(json)
    finally:
        conn.close()
