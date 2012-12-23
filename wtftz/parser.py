import re


def free_text(query):
    """Parse a string into the parameters for `convert`.

    Returns a triplet (timestamp, from_timezone, to_timezone) parsed from
    the query.

    Ex:
    >>> convert_free("2012-12-23T14:23:03.826437-05:00 to pst")
    ("2012-12-23T14:23:03.826437-05:00", None, "pst")
    """
    try:
        return _from_to(query)
    except Exception:
        pass

    try:
        return _to(query)
    except Exception:
        pass

    raise MismatchException("%s does not match" % query)


def _from_to(query):
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
