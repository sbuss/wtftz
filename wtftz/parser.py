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
    >>> free_text("2012-12-23T14:23:03.826437 from to pst")
    ('2012-12-23T14:23:03.826437-05:00', 'est', 'pst')
    >>> free_text("Mon Dec 10 23:31:50 EST 2012 to UTC")
    ("Mon Dec 10 23:31:50 2012", "EST", "UTC")
    """
    query, toz = _to(query)
    query, fromz = _from(query)
    return (query, fromz, toz)


def _to(query):
    """Try to parse a `to` timezone from the query.

    Args:
        query - A string with a time, and a source and destination timezone.
    Returns a tuple (query, to_timezone_string) parsed from the query. The
    query will be have the `to` timezone removed. If no timezone is found,
    return (query, None).

    >>> _to("2012-12-23T14:23:03.826437 to pst")
    ('2012-12-23T14:23:03.826437', 'pst')
    """
    pattern = re.compile(r"to ?(.*)")
    matches = pattern.findall(query)
    if len(matches) > 0:
        toz = matches[0]
        query = pattern.sub("", query, 1)
        return (query.strip(), toz.strip())
    else:
        raise MismatchException()


def _from(query):
    """Extract the `from ...` part of a query.

    Args:
        query - A string with a time, and a source and destination timezone.
    Returns a tuple (query, from_timezone_string) parsed from the query. The
    query will be have the from timezone removed. If no timezone is found,
    return (query, None).

    >>> _from("2012-12-23T14:23:03.826437 from est")
    ('2012-12-23T14:23:03.826437', 'est')

    If no `from` keyword is in this query, we will attempt to find a suitable
    timezone in the query string.
    """
    pattern = re.compile(r"from ([A-Za-z/ ]+)")
    matches = pattern.findall(query)
    if len(matches) > 0:
        fromz = matches[0]
        query = pattern.sub("", query, 1)
        return (query.strip(), fromz.strip())

    return _implicit_from(query)


def _implicit_from(query):
    """There *is* a source timezone in the query, but no from keyword.

    Args:
        query - A string with a time, and a source and destination timezone.
    Returns a triplet (timestamp, from_timezone, to_timezone) parsed from
    the query.

    >>> _implicit_from("2012-12-23T14:23:03.826437 est")
    ('2012-12-23T14:23:03.826437', 'est')
    >>> _implicit_from("Mon Dec 10 23:31:50 EST 2012")
    ("Mon Dec 10 23:31:50 2012", "EST")
    """
    pattern = re.compile(r"^([A-Za-z/]+)$")
    tokens = query.split(" ")
    for count, token in enumerate(tokens[::-1]):
        matches = pattern.findall(token)
        if len(matches) > 0:
            fromz = matches[0]
            if len(fromz) <= 1:
                continue
            query = " ".join(tokens[0:len(tokens) - count - 1] +
                             tokens[len(tokens) - count:])
            return (query.strip(), fromz.strip())
    return (query.strip(), None)


class MismatchException(Exception):
    pass
