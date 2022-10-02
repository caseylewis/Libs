import unittest

try:
    from Libs.DataLib.date_helper import *
except:
    from DataLib.date_helper import *


class TestDates(unittest.TestCase):

    def test_get_date_plus_one_year(self):
        # SINGLE YEAR #############################
        # LEAP DAY/YEAR
        leap_day = datetime.datetime(2024, 2, 29)
        next_year = get_date_increment_year(leap_day)
        self.assertEqual(next_year, datetime.datetime(2025, 2, 28))
        # FIRST OF MONTH
        first_of_month = datetime.datetime(2022, 10, 1)
        next_year = get_date_increment_year(first_of_month)
        self.assertEqual(next_year, datetime.datetime(2023, 10, 1))
        # LAST OF MONTH
        last_of_month = datetime.datetime(2022, 12, 31)
        next_year = get_date_increment_year(last_of_month)
        self.assertEqual(next_year, datetime.datetime(2023, 12, 31))

        # MULTIPLE YEARS ##############################
        # LEAP DAY/YEAR + 4 years
        leap_day = datetime.datetime(2024, 2, 29)
        next_year = get_date_increment_year(leap_day, years=4)
        self.assertEqual(next_year, datetime.datetime(2028, 2, 29))
        # LEAP DAY/YEAR - 4 years
        leap_day = datetime.datetime(2024, 2, 29)
        next_year = get_date_increment_year(leap_day, years=-4)
        self.assertEqual(next_year, datetime.datetime(2020, 2, 29))

    def test_get_date_plus_one_month(self):
        # OUT OF BOUNDS ###################################
        first_of_year = datetime.datetime(2022, 1, 1)
        with self.assertRaises(MonthOutOfRange):
            get_date_plus_one_month(first_of_year, months=13)
        with self.assertRaises(MonthOutOfRange):
            get_date_plus_one_month(first_of_year, months=-12)
        # ADDING SINGLE MONTH #############################
        # March 31st
        march_end = datetime.datetime(2022, 3, 31)
        next_month = get_date_plus_one_month(march_end)
        self.assertEqual(next_month, datetime.datetime(2022, 4, 30))
        # DECEMBER 31st
        year_end = datetime.datetime(2022, 12, 31)
        next_month = get_date_plus_one_month(year_end)
        self.assertEqual(next_month, datetime.datetime(2023, 1, 31))

        # ADDING MULTIPLE MONTHS #############################
        # March 31st - July 31st
        march_end = datetime.datetime(2022, 3, 31)
        next_month = get_date_plus_one_month(march_end, months=4)
        self.assertEqual(next_month, datetime.datetime(2022, 7, 31))
        # March 31st - June 30th
        march_end = datetime.datetime(2022, 3, 31)
        next_month = get_date_plus_one_month(march_end, months=3)
        self.assertEqual(next_month, datetime.datetime(2022, 6, 30))

        # SUBTRACTING MONTHS #############################
        january_start = datetime.datetime(2022, 1, 1)
        previous_month = get_date_plus_one_month(january_start, months=-1)
        self.assertEqual(previous_month, datetime.datetime(2021, 12, 1))
        # January 31st - 2 months = November 30th
        january_start = datetime.datetime(2022, 1, 31)
        previous_month = get_date_plus_one_month(january_start, months=-2)
        self.assertEqual(previous_month, datetime.datetime(2021, 11, 30))



