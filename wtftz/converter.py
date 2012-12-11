import datetime

from dateutil import parser as date_parser
import pytz

from .timezones import common_timezones


def convert(timestamp, to_tz="utc", from_tz="utc", naive=True):
    from_timezone = common_tz_name_to_real_tz(from_tz)
    to_timezone = common_tz_name_to_real_tz(to_tz)
    timestamp = parse_timestamp(timestamp)
    if not hasattr(timestamp, 'tzinfo') or timestamp.tzinfo is None:
        timestamp = from_timezone.localize(timestamp)
    timestamp = timestamp.astimezone(to_timezone)
    return timestamp.replace(tzinfo=None)


def common_tz_name_to_real_tz(name):
    if isinstance(name, datetime.tzinfo):
        return name
    if name in common_timezones:
        return common_timezones[name]
    try:
        return pytz.timezone(name)
    except Exception:
        pass
    return pytz.UTC


def parse_timestamp(timestamp):
    if isinstance(timestamp, datetime.datetime) or \
            isinstance(timestamp, datetime.time):
        return timestamp

    try:
        timestamp = float(timestamp)
        # Must have an epoch
        try:
            return datetime.datetime.fromtimestamp(timestamp)
        except Exception:
            pass
    except Exception:
        pass

    timestamp = str(timestamp)
    try:
        return date_parser.parse(timestamp)
    except Exception:
        pass

    raise ValueError("Cannot parse timestamp {ts}".format(ts=timestamp))
