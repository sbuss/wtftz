import re


def free_text(query):
    """Parse a string into the parameters for `convert`.

    Args:
        query - A string with a time, and a source and destination timezone.
    Returns a triplet (timestamp, from_timezone, to_timezone) parsed from
    the query.

    Ex:
    >>> free_text("2012-12-23T14:23:03.826437-05:00 to pst")
    ('2012-12-23T14:23:03.826437-05:00', None, 'pst')
    """
    try:
        return _from_to(query)
    except Exception:
        pass

    try:
        return _to(query)
    except Exception:
        pass

    raise MismatchException("%s does not match a known pattern" % query)


def _from_to(query):
    """Try to parse a `from` and `to` timezone from the query.

    Args:
        query - A string with a time, and a source and destination timezone.
    Returns a triplet (timestamp, from_timezone, to_timezone) parsed from
    the query.

    >>> _from_to("2012-12-23T14:23:03.826437 from est to pst")
    ('2012-12-23T14:23:03.826437', 'est', 'pst')
    """
    template = re.compile(r"(.*)from(.*)to(.*)")
    matches = template.findall(query)
    if len(matches) == 1:
        match = matches[0]
        ts = match[0].strip()
        fromz = match[1].strip()
        toz = match[2].strip()
        return (ts, fromz, toz)
    raise MismatchException()


def _to(query):
    """Try to parse a `to` timezone from the query.

    Args:
        query - A string with a time, and a source and destination timezone.
    Returns a triplet (timestamp, from_timezone, to_timezone) parsed from
    the query.

    >>> _to("2012-12-23T14:23:03.826437 to pst")
    ('2012-12-23T14:23:03.826437', None, 'pst')
    """
    template = re.compile(r"(.*)to(.*)")
    fromz = None
    matches = template.findall(query)
    if len(matches) == 1:
        match = matches[0]
        ts = match[0].strip()
        toz = match[1].strip()
        return (ts, fromz, toz)
    raise MismatchException()


class MismatchException(Exception):
    pass
