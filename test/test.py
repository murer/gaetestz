import unittest

def test_all():
    suite = unittest.loader.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    test_all()
