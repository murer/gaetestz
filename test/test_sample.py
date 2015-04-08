import tsutil
tsutil.fix()

import unittest
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

class SampleTestCase(unittest.TestCase):


  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
    # Create a consistency policy that will simulate the High Replication consistency model.
    self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
    # Initialize the datastore stub with this policy.
    self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
    # Initialize memcache stub too, since ndb also uses memcache
    self.testbed.init_memcache_stub()

  def tearDown(self):
    self.testbed.deactivate()

  def testEventuallyConsistentGlobalQueryResult(self):
    class TestModel(ndb.Model):
      pass

    import src.main as main
    print main.Ping

    user_key = ndb.Key('User', 'ryan')
    # Put two entities
    ndb.put_multi([TestModel(parent=user_key), TestModel(parent=user_key)])

    # Global query doesn't see the data.
    self.assertEqual(0, TestModel.query().count(3))
    # Ancestor query does see the data.
    self.assertEqual(2, TestModel.query(ancestor=user_key).count(3))

if __name__ == '__main__':
    unittest.main()
    #unittest.TextTestRunner(verbosity=2).run(unittest.loader.TestLoader().discover('.'))
