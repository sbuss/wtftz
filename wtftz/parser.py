import re


def free_text(query):
    template = re.compile(r"(.*)from(.*)to(.*)")
    matches = template.findall(query)
    if len(matches) > 0:
        match = matches[0]
        ts = match[0].strip()
        fromz = match[1].strip()
        toz = match[2].strip()
    else:
        ts = query
        fromz = ""
        toz = ""
    return (ts, fromz, toz)
