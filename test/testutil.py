import httplib
import json as JSON

class Error(Exception):
    """ Error """

def http_json(method, host, port, uri, content = None):
    conn = httplib.HTTPConnection(host, port)
    try:
        print 'x', host, port, uri
        conn.request(method, uri)
        resp = conn.getresponse()
        if(resp.status != 200):
            raise Error('Error on http client: %s' % (resp.status))
        json = resp.read()
        return JSON.loads(json)
    finally:
        conn.close()
