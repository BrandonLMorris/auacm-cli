"""Tests for compiled solution testing (yeah, I know that's confusing)"""

import auacm, unittest


class CompiledTestingTests(unittest.TestCase):
    """Tests for compiled solutions"""

    @classmethod
    def setUpClass(cls):
        """One time setup: make sure we can ping the real server"""
        result = auacm.main.test(['ping'])
        assert result == 'Connection successful! 200', ('Could not connect'
            'auacm server')

    def testCSolution(self):
        """Test a compiled C solution"""
        result = auacm.problems.test_solution(['solutions/parity.c'])
        self.assertIn('passed', result.lower())


if __name__ == '__main__':
    unittest.main()
