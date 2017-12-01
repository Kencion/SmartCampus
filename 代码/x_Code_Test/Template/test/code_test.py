'''
Created on 2017年12月1日

@author: Jack
'''
import unittest

class code_test(unittest.TestCase):
    
    def setUp(self):
        # Do something to initiate the test environment here.
        from x_Code_Test.Template.my_code.my_code import my_code
        self.my_code = my_code()
        print("set up")
        
    
    def tearDown(self):
        # Do something to clear the test environment here.
        print("set up")
 
    def test_plus(self):
        a = 1
        b = 2
        c = 3
        
        self.assertEqual(c, self.my_code.plus(a, b))

if __name__ == '__main__':
    unittest.main()
