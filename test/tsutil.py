import optparse
import sys
import unittest
import os

fixed = False

def fix():
    if fixed:
        print 'already fixed'
        return
    sdk_path = '.gen/google_appengine'
    if os.path.exists(os.path.join(sdk_path, 'platform/google_appengine')):
      sys.path.insert(0, os.path.join(sdk_path, 'platform/google_appengine'))
    else:
      sys.path.insert(0, sdk_path)
    sys.path.insert(0, '.')
    import dev_appserver
    dev_appserver.fix_sys_path()
    try:
      import appengine_config
    except ImportError:
      print "Note: unable to import appengine_config."

def main(test_path):
    suite = unittest.loader.TestLoader().discover(test_path)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main('test')
    
