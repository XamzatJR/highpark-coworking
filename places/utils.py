from datetime import timedelta


def get_date_range(date):
    days = (date.end - date.start).days + 2
    date.start -= timedelta(1)
    return [date.start + timedelta(days=x) for x in range(days)]
