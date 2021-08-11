from tele_order.utils import constants
from pytz import timezone, UnknownTimeZoneError


def make_as_timezone(datetime, utc: str):
    try:
        user_timezone = timezone(utc)
        new_datetime = datetime.astimezone(user_timezone)
    except UnknownTimeZoneError:
        user_timezone = timezone(constants.DEVELOPERS_TIMEZONE)
        new_datetime = datetime.astimezone(user_timezone)
    return new_datetime


def convert_datetime_with_short_month(
        datetime, utc=constants.DEVELOPERS_TIMEZONE) -> str:
    new_datetime = make_as_timezone(datetime=datetime, utc=utc)
    result_datetime = new_datetime.strftime(
            f'%d {constants.MONTHS[int(new_datetime.strftime("%m")) - 1][1]} %Y')
    return result_datetime


def convert_datetime_with_hours_short(
        datetime, utc=constants.DEVELOPERS_TIMEZONE) -> str:
    new_datetime = make_as_timezone(datetime=datetime, utc=utc)
    result_datetime = new_datetime.strftime(
            f'%d {constants.MONTHS[int(new_datetime.strftime("%m")) - 1][1]} %Y %H:%M')
    return result_datetime


def convert_datetime_with_long_month(
        datetime, utc=constants.DEVELOPERS_TIMEZONE) -> str:
    new_datetime = make_as_timezone(datetime=datetime, utc=utc)
    result_datetime = new_datetime.strftime(
            f'%d {constants.MONTHS[int(new_datetime.strftime("%m")) - 1][2]} %Y')
    return result_datetime


def convert_datetime_with_hours_long(
        datetime, utc=constants.DEVELOPERS_TIMEZONE) -> str:
    new_datetime = make_as_timezone(datetime=datetime, utc=utc)
    result_datetime = new_datetime.strftime(
            f'%d {constants.MONTHS[int(new_datetime.strftime("%m")) - 1][2]} %Y %H:%M')
    return result_datetime
