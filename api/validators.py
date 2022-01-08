import datetime
from rest_framework.exceptions import ParseError


def validate_date_format(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ParseError(detail="Incorrect data format, should be YYYY-MM-DD")
