=====
wtftz
=====

WTF Timezones?!
===============

I can't convert UTC to PST in my head, and google can't do it for me either.

Every timezone converter website is full of spam and the worst UX imaginable.

wtftz assumes you're trying to convert a UTC timestamp
------------------------------------------------------

.. code:: python

    print(wtftz.convert("2012-12-10T18:31:29.214653", "pst"))
    # 2012-12-10 10:31:29.214653

unless you're not
-----------------

Note the embedded timezone in this iso-formatted string.

.. code:: python

    print(wtftz.convert("2012-12-10T18:31:29.214653-08:00", "pst"))
    # 2012-12-10 18:31:29.214653

wtftz knows a few common abbreviations for timezones
----------------------------------------------------

.. code:: python

    print(wtftz.convert("1355236920", "est"))
    # 2012-12-11 01:42:00
    # Sorry, Australia! EST is most commonly used for US/Eastern!

wtftz gives back tzinfo-free timestamps because python's timezones are broken!
------------------------------------------------------------------------------

.. code:: python

    print(wtftz.convert(datetime.datetime.now(), from_tz="pst", to_tz="utc"))
    # 2012-12-11 06:45:04.075608
    print(wtftz.convert(datetime.datetime.now(), from_tz="pst", to_tz="eastern"))
    # 2012-12-11 01:45:18.343536

wtftz knows that you don't know if the current time is PST or PDT
-----------------------------------------------------------------

But it does the right thing, using PST or PDT when appropriate

.. code:: python

    print(wtftz.convert(datetime.datetime.now(), "pst"))
    # 2012-12-11 06:48:39.860947
    print(wtftz.convert(datetime.datetime.now(), "pdt"))
    # 2012-12-11 06:48:39.860947

wtftz knows that you work with systems with nonstandard timestamp formats
-------------------------------------------------------------------------

.. code:: python

    print(wtftz.convert('2012/10/7 12:25:46', 'pst'))
    # 2012-10-07 19:25:46 
    print(wtftz.convert('7 October 2012 12:25:46', 'pst'))
    # 2012-10-07 19:25:46 

wtftz will accept proper timezone names, too
--------------------------------------------

.. code:: python

    print(wtftz.convert(datetime.datetime.now(), "US/Pacific"))
    # 2012-12-10 15:04:03.644934
    print(wtftz.convert(datetime.datetime.now(), "America/Chicago"))
    # 2012-12-10 17:04:03.650494

But it can't handle everything
------------------------------

.. code:: python

    print(wtftz.convert('2012:10:7:12:25:46', 'pst'))
    # ...
    # ValueError: Cannot parse timestamp 2012:10:7:12:25:46

Use it from the shell!
----------------------

.. code:: sh

    $ date && ./wtftz "`date`" pst && ./wtftz "`date`" utc
    Mon Dec 10 23:43:06 PST 2012
    2012-12-10 23:43:06
    2012-12-11 07:43:06
    $ date +%s && ./wtftz "`date +%s`" utc
    1355211747
    2012-12-10 23:42:27

Wtftz can also handle free text strings
---------------------------------------

.. code:: python

    print(wtftz.convert_free("1355236920 to est"))
    # 2012-12-11 01:42:00
    print(wtftz.convert_free("2012-12-10T18:31:29.214653-08:00 to est"))
    # 2012-12-10 21:31:29.214653
    print(wtftz.convert_free("2012-12-10T18:31:29.214653 from pst to est"))
    # 2012-12-10 21:31:29.214653
    print(wtftz.convert_free("2012-12-10T18:31:29.214653 from utc to est"))
    # 2012-12-10 13:31:29.214653

Installation
============

`wtftz <http://pypi.python.org/pypi/wtftz>`_ is in the cheese shop, so just:

.. code:: sh

    pip install wtftz

Development
===========

Issues and Pull Requests are welcome!

I'm looking to expand the list of common timezone names to include foreign
(to me) timezones and make the free-text parser smarter.


Testing
-------

Tests are important. Pull requests will not be accepted without them.

.. code:: sh

    python -m unittest discover

Readme
------

This README should be updated with examples as new behavior is added. To
ensure that the file is formatted correctly, please check it:

.. code:: sh

    pip install docutils
    pip install pygments
    python setup.py --long-description | rst2html.py > output.html

Ensure that the file parses and looks good.
