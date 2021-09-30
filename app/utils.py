import datetime


def format_date(date, format=None):
    format = format or "%Y-%m-%d"
    date = datetime.datetime.strptime(date, format)
    return date.strftime("%d/%m/%Y")
