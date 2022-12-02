"""
Sample Tests
"""

from django.test import SimpleTestCase
from app import calc

class CalcTest(SimpleTestCase):
    """
    Test the calc module
    """

    def test_add_numbers(self):
        """
        Test addition function
        """

        res = calc.add(5, 6)

        self.assertEqual(res, 11)


    def test_subtract_numbers(self):
        """
        Test subtract function
        """

        res = calc.subtract(10, 15)

        self.assertEqual(res, 5)