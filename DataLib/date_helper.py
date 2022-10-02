import datetime

_MONTHS_IN_YEAR = 12


def get_date_increment_year(date, years=1):
    """
    Allows you to get a datetime.datetime object of a different year, or the closest thing to it.

    Handles leap years (February 29th) by decrementing by one day, so that it will remain as the last day of February.
    :param date: datetime.datetime object
    :param years: Number of years to increment OR decrement (decrement by passing negative integer)
    :return: datetime.datetime object
    """
    month = date.month
    day = date.day
    year = date.year + years
    try:
        next_year = datetime.datetime(year, month, day)
    except ValueError:
        next_year = datetime.datetime(year, month, day-1)

    return next_year


def get_date_plus_one_month(date, months=1):
    """
    Allows you to get a datetime.datetime object of a different month, or the closest thing to it.

    Handles passing over a year (December 31st) by setting month to January and incrementing the year.
    For example December 31st, 2022 + 1 year ends up as January 31st, 2023.

    Values greater than 11 or less than -11 not valid as the get_date_increment_year() function should be used instead.
    :param date: datetime.datetime object
    :param months: Number of months to increment OR decrement (decrement by passing negative integer)
    :return:datetime.datetime object
    """
    if -(_MONTHS_IN_YEAR - 1) > months or months > _MONTHS_IN_YEAR - 1:
        exc_text = f"Invalid month: [{months}]. " \
                   f"Please use get_date_increment_year() function if incrementing months outside of -12 to 11."
        raise MonthOutOfRange(exc_text)

    month = date.month + months
    day = date.day
    year = date.year
    if month > _MONTHS_IN_YEAR:
        month = month % _MONTHS_IN_YEAR
        year += 1
    elif month < 1:
        month += _MONTHS_IN_YEAR
        year -= 1
    try:
        next_month = datetime.datetime(year, month, day)
    except ValueError:
        next_month = datetime.datetime(year, month, day-1)
    return next_month


class MonthOutOfRange(Exception):
    pass
