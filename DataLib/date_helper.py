import datetime


def get_date_plus_one_year(date):
    month = date.month
    day = date.day
    year = date.year + 1
    try:
        next_year = datetime.datetime(year, month, day)
    except ValueError:
        next_year = datetime.datetime(year, month, day-1)

    return next_year
