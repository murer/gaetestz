import unittest
from gae_server_test import GaeTestServer

print 'xxxx'
gae = GaeTestServer()

class TestCase(unittest.TestCase):

    def setUp(self):
        import main
        gae.boot_gae()
        gae.boot_web(8080, main.app)
        gae.server_forever_background()

    def tearDown(self):
        gae.shutdown()
