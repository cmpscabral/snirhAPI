import datetime


def currency(nr: float) -> str:
    return format(nr, "01,.2f").replace(",", " ").replace(".", ",")


def parse_date(date: str) -> datetime.date:
    return datetime.datetime.strptime(date.strip(), "%d-%m-%Y").date()


def format_date(date, format="%Y-%m-%d"):
    date = datetime.datetime.strptime(date, format)
    return date.strftime("%d/%m/%Y")
