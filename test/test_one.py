
import test_case
import httplib
from google.appengine.ext import ndb

class OneTestCase(test_case.TestCase):

    def test_one(self):
        class TestModel(ndb.Model):
            pass
        user_key = ndb.Key('User', 'ryan')
        ndb.put_multi([TestModel(parent=user_key), TestModel(parent=user_key)])
        self.assertEqual(0, TestModel.query().count(3))
        self.assertEqual(2, TestModel.query(ancestor=user_key).count(3))

    def test_twice(self):
        self.test_one()

    def test_web(self):
        conn = httplib.HTTPConnection('localhost', test_case.gae.port)
        conn.request('GET', '/s/ping')
        resp = conn.getresponse()
        self.assertEqual(200, resp.status)
        self.assertEqual('OK', resp.reason)
        self.assertEqual('pong', resp.read())
        conn.close()

    def test_web_twice(self):
        self.test_web()
