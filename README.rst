wtftz
=====

WTF Timezones?!

I can't convert UTC to PST in my head, and google can't do it for me either.

Every timezone converter website is full of spam and the worst UX imaginable.

wtftz assumes you're trying to convert a UTC timestamp
------------------------------------------------------

    print(wtftz.convert("2012-12-10T18:31:29.214653", "pst"))
    # 2012-12-10 10:31:29.214653

wtftz knows a few common abbreviations for timezones
----------------------------------------------------

    print(wtftz.convert("1355236920", "est"))
    # 2012-12-11 01:42:00
    # Sorry, Australia! EST is most commonly used for US/Eastern!

wtftz gives back tzinfo-free timestamps because python's timezones are broken!
------------------------------------------------------------------------------

    print(wtftz.convert(datetime.datetime.now(), from_tz="pst", to_tz="utc"))
    # 2012-12-11 06:45:04.075608
    print(wtftz.convert(datetime.datetime.now(), from_tz="pst", to_tz="eastern"))
    # 2012-12-11 01:45:18.343536

wtftz knows that you don't know if the current time is PST or PDT
-----------------------------------------------------------------

But it does the right thing, using PST or PDT when appropriate

    print(wtftz.convert(datetime.datetime.now(), "pst"))
    # 2012-12-11 06:48:39.860947
    print(wtftz.convert(datetime.datetime.now(), "pdt"))
    # 2012-12-11 06:48:39.860947

wtftz knows that you work with systems with nonstandard timestamp formats
-------------------------------------------------------------------------

    print(wtftz.convert('2012/10/7 12:25:46', 'pst'))
    # 2012-10-07 19:25:46 
    print(wtftz.convert('7 October 2012 12:25:46', 'pst'))
    # 2012-10-07 19:25:46 

wtftz will accept proper timezone names, too
--------------------------------------------

    print(wtftz.convert(datetime.datetime.now(), "US/Pacific"))
    # 2012-12-10 15:04:03.644934
    print(wtftz.convert(datetime.datetime.now(), "America/Chicago"))
    # 2012-12-10 17:04:03.650494

But it can't handle everything
------------------------------

    print(wtftz.convert('2012:10:7:12:25:46', 'pst'))
    # ...
    # ValueError: Cannot parse timestamp 2012:10:7:12:25:46

Use it from the shell!
----------------------

    $ date && ./wtftz "`date`" pst && ./wtftz "`date`" utc
    Mon Dec 10 23:43:06 PST 2012
    2012-12-10 23:43:06
    2012-12-11 07:43:06
    $ date +%s && ./wtftz "`date +%s`" utc
    1355211747
    2012-12-10 23:42:27
