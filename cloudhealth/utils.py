from datetime import date, timedelta


def _get_yesterdays_date():
    current = date.today()
    return date(current.year, current.month, current.day-1).strftime('%Y-%m-%d')

def _get_last_month():
    current = date.today()
    return date(current.year, current.month-1, current.day).strftime('%Y-%m')