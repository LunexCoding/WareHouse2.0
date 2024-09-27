from datetime import datetime
from .consts import Constants


def isTimestamp(value):
    try:
        if '.' in value:
            value = float(value)
            datetime.fromtimestamp(value)
            return True
        return False
    except (ValueError, OverflowError):
        return False


def convertDateToTimestamp(date):
    try:
        return datetime.strptime(date, Constants.DATETIME_FORMAT).timestamp()
    except ValueError:
        return date


def convertTimestampToDate(timestamp):
    return datetime.fromtimestamp(float(timestamp)).strftime(Constants.DATETIME_FORMAT)
