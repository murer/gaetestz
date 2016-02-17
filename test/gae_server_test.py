import os
import sys
import threading
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler

def resolve_sdk_path():
    path = None
    if os.path.isfile('.gen/google_appengine/dev_appserver.py'):
        print 'find installed'
        path = '.gen/google_appengine'
    if not path:
        for p in os.environ['PATH'].split(os.pathsep):
            check = os.path.join(p, 'dev_appserver.py')
            if os.path.exists(check):
                directory = os.path.dirname(os.path.abspath(check))
                directory = os.path.dirname(directory)
                path = directory
                break
    if path:
        possible = os.path.join(path, 'platform/google_appengine')
        if os.path.exists(possible):
            path = possible
    if not path:
        raise 'Python sdk not found'
    return path

class GaeTestServer(object):

    def __init__(self):
        self.sdk_path = resolve_sdk_path()
        print 'python sdk found', self.sdk_path
        sys.path.insert(0, self.sdk_path)
        import dev_appserver
        dev_appserver.fix_sys_path()
        sys.path.insert(0, 'src')
        self.testbed = None
        self.httpd = None

    def boot_gae(self):
        from google.appengine.api import memcache
        from google.appengine.ext import ndb
        from google.appengine.ext import testbed
        from google.appengine.datastore import datastore_stub_util
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        self.testbed.init_memcache_stub()

    def boot_web(self, port, app):
        self.port = port
        self.httpd = WSGIServer(('localhost', port), WSGIRequestHandler)
        self.httpd.set_app(app)

    def server_forever_background(self):
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.start()

    def server_forever(self):
        self.httpd.serve_forever()

    def shutdown(self):
        if self.testbed:
            self.testbed.deactivate()
        if self.httpd:
            self.httpd.shutdown()
            self.httpd = None

def main():
    gae = GaeTestServer()
    gae.boot_gae()
    import main
    gae.boot_web(8080, main.app)
    gae.server_forever()
    gae.shutdown()

if __name__ == '__main__':
    main()
