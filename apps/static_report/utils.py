import datetime


def get_current_quarter() -> int:
    """
    Get the current quarter of the year.

    :returns: int
        The current quarter as an integer (1 to 4).
    """
    current_month = datetime.datetime.now().month
    quarter_count = 4

    return current_month//quarter_count + 1


def get_current_year() -> int:
    """
    Get the current year.

    :returns: int
        The current year as an integer (1 to 12).
    """
    return datetime.datetime.now().year
