import datetime

from dateutil import parser as date_parser
import pytz

from .timezones import common_timezones
from .parser import free_text


def convert(timestamp, to_tz="utc", from_tz="utc", naive=True):
    """Convert a timestamp from one timezone to another.

    Args:
        timestamp: The timestamp you want to convert.
        to_tz: The timezone you want to end up in.
        from_tz: The timezone of the original timestamp, if needed.
        naive: If True, then strip the tzinfo from the converted timestamp,
               if False then leave it.
    Returns a timestamp in the requested timezone.
    """
    if not to_tz:
        to_tz = "utc"
    if not from_tz:
        from_tz = "utc"
    from_timezone = common_tz_name_to_real_tz(from_tz)
    to_timezone = common_tz_name_to_real_tz(to_tz)
    timestamp = parse_timestamp(timestamp)
    if not hasattr(timestamp, 'tzinfo') or timestamp.tzinfo is None:
        timestamp = from_timezone.localize(timestamp)
    timestamp = timestamp.astimezone(to_timezone)
    if naive:
        return timestamp.replace(tzinfo=None)
    else:
        return timestamp


def convert_free(query):
    ts, fromz, toz = free_text(query)
    return convert(ts, toz, fromz)


def common_tz_name_to_real_tz(name):
    """Convert the name of a timezone to a real timezone.

    Args:
        name: The name of the timezone. eg "est" or "US/Eastern"
    Returns a tzinfo.
    """
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
    """Try to parse the given timestamp.

    Args:
        timestamp: The timestamp you want to parse. Accepts epoch,
                   isoformat, and anything python-dateutil can handle.
    Returns a timestamp.
    """
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
