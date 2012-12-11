import pytz


common_timezones = {
    'est': pytz.timezone('US/Eastern'),
    'edt': pytz.timezone('US/Eastern'),
    'eastern': pytz.timezone('US/Eastern'),
    'cst': pytz.timezone('US/Central'),
    'cdt': pytz.timezone('US/Central'),
    'central': pytz.timezone('US/Central'),
    'mst': pytz.timezone('US/Mountain'),
    'mdt': pytz.timezone('US/Mountain'),
    'mountain': pytz.timezone('US/Mountain'),
    'pst': pytz.timezone('US/Pacific'),
    'pdt': pytz.timezone('US/Pacific'),
    'pacific': pytz.timezone('US/Pacific'),
    'utc': pytz.utc,
    'gmt': pytz.utc,
    'universal': pytz.utc,
    'one timezone to rule them all': pytz.utc
}
