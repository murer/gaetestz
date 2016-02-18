import unittest
import testcase
from google.appengine.ext import ndb

class TwoTestCase(testcase.TestCase):

    def testtwo(self):
        class TestModel(ndb.Model):
            pass
        user_key = ndb.Key('User', 'ryan')
        ndb.put_multi([TestModel(parent=user_key), TestModel(parent=user_key)])
        self.assertEqual(0, TestModel.query().count(3))
        self.assertEqual(2, TestModel.query(ancestor=user_key).count(3))

if __name__ == '__main__':
        unittest.main()
