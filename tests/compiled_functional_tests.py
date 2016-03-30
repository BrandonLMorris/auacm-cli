"""Tests for compiled solution testing (yeah, I know that's confusing)"""

import auacm, unittest, os


class CompiledTestingTests(unittest.TestCase):
    """Tests for compiled solutions"""

    @classmethod
    def setUpClass(cls):
        """One time setup: make sure we can ping the real server"""
        result = auacm.main.test(['ping'])
        assert result == 'Connection successful! 200', ('Could not connect'
            'auacm server')

        # Move to the solutions directory
        os.chdir(os.path.join(os.getcwd(), 'solutions'))


    @classmethod
    def tearDownClass(cls):
        """One time teardown"""
        # Move back to the original directory (in case more tests)
        os.chdir('..')


    def testCSolution(self):
        """Test a compiled C solution"""
        result = auacm.problems.test_solution(['parity.c'])
        self.assertIn('passed', result.lower())

    def testCppSolution(self):
        """Test a compiled C++ solution"""
        result = auacm.problems.test_solution(['parity.cpp'])
        self.assertIn('passed', result.lower())

    def testJavaSolution(self):
        """Test a compiled Java solution"""
        # The Java path screws things up. Change the directory
        result = auacm.problems.test_solution(['Parity.java'])
        self.assertIn('passed', result.lower())

    def testPython3Solution(self):
        """Test a Python3 solution"""
        result = auacm.problems.test_solution(['parity.py', '-p', '3'])
        self.assertIn('passed', result.lower())

    def testPython2Solution(self):
        """Test a Python2 solution"""
        result = auacm.problems.test_solution(
            ['parity_two.py', 'parity', '-p', '2'])
        self.assertIn('passed', result.lower())


if __name__ == '__main__':
    unittest.main()
