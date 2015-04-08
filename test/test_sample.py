import tsutil
tsutil.fix()

import unittest
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

class SampleTestCase(unittest.TestCase):


  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
    self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
    self.testbed.init_memcache_stub()

  def tearDown(self):
    self.testbed.deactivate()

  def testEventuallyConsistentGlobalQueryResult(self):
    class TestModel(ndb.Model):
      pass
    user_key = ndb.Key('User', 'ryan')
    ndb.put_multi([TestModel(parent=user_key), TestModel(parent=user_key)])
    self.assertEqual(0, TestModel.query().count(3))
    self.assertEqual(2, TestModel.query(ancestor=user_key).count(3))

if __name__ == '__main__':
    unittest.main()
