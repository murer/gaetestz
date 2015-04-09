import optparse
import sys
import unittest
import os

def fix():
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

def test_all():
    suite = unittest.loader.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(suite)

def start_web():
    """ aaa """

if __name__ == '__main__':
        #test_all()
        start_web()
        
