import unittest
from gae_server_test import GaeTestServer

print 'xxxx'
gae = GaeTestServer()

class TestCase(unittest.TestCase):

    def setUp(self):
        gae.boot_gae()

    def tearDown(self):
        gae.shutdown()
