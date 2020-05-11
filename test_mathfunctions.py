import unittest
import mathfunctions

class TestMathFunctions(unittest.TestCase):
    def test_isEven(self):
        # Invalid numbers: Returns False validOutputReturned
        self.assertAlmostEqual(mathfunctions.isEven("x")['validOutputReturned'],False)
        # Zero and Posibive numbers: Returns True validOutputReturned
        self.assertAlmostEqual(mathfunctions.isEven(0)['validOutputReturned'],True)
        self.assertAlmostEqual(mathfunctions.isEven(1)['validOutputReturned'],True)
        self.assertAlmostEqual(mathfunctions.isEven(2)['validOutputReturned'],True)
        # Validate result for 0, 1 and 2
        self.assertAlmostEqual(mathfunctions.isEven(0)['result'],True)
        self.assertAlmostEqual(mathfunctions.isEven(1)['result'],False)
        self.assertAlmostEqual(mathfunctions.isEven(2)['result'],True)

    def test_isPrime(self):
        # validOutputReturned is False for zero and negative
        for i in range(-10,10):
            if i <= 0:
                self.assertAlmostEqual(mathfunctions.isPrime(i)['validOutputReturned'],False)
            else:
                self.assertAlmostEqual(mathfunctions.isPrime(i)['validOutputReturned'],True)
        # Validate result for 1 through 10
        # 1:True, 2:True, 3:True, 4:False, 5:True, 6:False, 7:True, 8:False, 9:False, 10:False
        validResultList = [True,True,True,False,True,False,True,False,False,False]
        for i in range(10):
            self.assertAlmostEqual(mathfunctions.isPrime(i+1)['result'],validResultList[i])

