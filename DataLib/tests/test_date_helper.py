import unittest

try:
    from Libs.DataLib.date_helper import *
except:
    from DataLib.date_helper import *


class TestDates(unittest.TestCase):

    def test_get_date_plus_one_year(self):
        # LEAP DAY/YEAR
        leap_day = datetime.datetime(2024, 2, 29)
        next_year = get_date_plus_one_year(leap_day)
        self.assertEqual(next_year, datetime.datetime(2025, 2, 28))
        # FIRST OF MONTH
        first_of_month = datetime.datetime(2022, 10, 1)
        next_year = get_date_plus_one_year(first_of_month)
        self.assertEqual(next_year, datetime.datetime(2023, 10, 1))
        # LAST OF MONTH
        last_of_month = datetime.datetime(2022, 12, 31)
        next_year = get_date_plus_one_year(last_of_month)
        self.assertEqual(next_year, datetime.datetime(2023, 12, 31))



