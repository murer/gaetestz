import httplib
import json as JSON

class Error(Exception):
    """ Error """

def http_json(method, host, port, uri, content = None):
    conn = httplib.HTTPConnection(host, port)
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
