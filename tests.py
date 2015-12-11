__author__ = 'nicholas'

import unittest
import cv_preamble
import datetime

class TestDateParser(unittest.TestCase):
    """Tests the cv_preamble.dateparse_str() function"""
    def test_string_input(self):
        value = cv_preamble.dateparse_str('3 Aug 2012')
        self.assertIsInstance(value, datetime.datetime)
        self.assertEqual(value, datetime.datetime(month=8, year=2012, day=3))

    def test_datetime_input(self):
        value_in = datetime.datetime(day=15, month=3, year=2015)
        value = cv_preamble.dateparse_str(value_in)
        self.assertIsInstance(value, datetime.datetime)
        self.assertEqual(value_in, value)

    def test_nondate_string_input(self):
            self.assertRaises(ValueError, cv_preamble.dateparse_str, 'Not a Date')
            self.assertRaises(ValueError, cv_preamble.dateparse_str, 'Aug 12 - May 2015')


if __name__ == '__main__':
    unittest.main()