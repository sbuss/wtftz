from datetime import datetime
import time
from unittest import TestCase

import pytz

import wtftz


def _epoch(ts):
    return str(int(time.mktime(ts.timetuple())))


def _convert(ts, from_tz=pytz.utc, to_tz=pytz.timezone('US/Pacific')):
    # Convert from pacific to UTC
    local_time = from_tz.localize(ts)
    local_time = to_tz.normalize(local_time)
    return local_time.replace(tzinfo=None)


def _truncate_time(ts):
    return datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second)


class TestUtc(TestCase):
    def _test_times(self, val, ts):
        self.assertEqual(wtftz.convert(val, to_tz="pacific"), _convert(ts))
        self.assertEqual(wtftz.convert(val, to_tz="pst"), _convert(ts))
        self.assertEqual(wtftz.convert(val, to_tz="pdt"), _convert(ts))
        self.assertEqual(wtftz.convert(val, to_tz="utc"), ts)
        self.assertEqual(wtftz.convert(val, to_tz="gmt"), ts)

    def test_utc_epoch(self):
        ts = datetime.utcnow()
        epoch = _epoch(ts)
        self._test_times(epoch, _truncate_time(ts))

    def test_utc_epoch_milliseconds(self):
        ts = datetime.utcnow()
        epoch = _epoch(ts)
        epoch += ".{us}".format(us=ts.microsecond)
        self._test_times(epoch, ts)

    def test_utc_isoformat(self):
        ts = datetime.utcnow()
        self._test_times(ts.isoformat(), ts)

    def test_utc_isoformat_truncated(self):
        ts = datetime.utcnow()
        iso = ts.isoformat()
        # isoformat looks like 2012-12-10T18:31:29.214653
        iso = iso.split(".")[0]
        self._test_times(iso, _truncate_time(ts))


class TestCommonTZNames(TestCase):
    def _test_slang_tz(self, timestamp, slang_tz, actual_tz):
        """Test the slang timezone converter.

        Args:
            timestamp: The source timestamp, as UTC
            slang_tz: The common name for a timezone
            actual_tz: A proper pytz timezone
        """
        timezoned = _convert(timestamp, to_tz=actual_tz)
        epoch = _epoch(timestamp)
        self.assertEqual(_truncate_time(timezoned),
                         wtftz.convert(epoch, to_tz=slang_tz))
        self.assertEqual(
            timezoned, wtftz.convert(timestamp.isoformat(), to_tz=slang_tz))

    def test_utc(self):
        self._test_slang_tz(
            datetime.utcnow(), "utc", pytz.utc)
        self._test_slang_tz(
            datetime.utcnow(), "gmt", pytz.utc)
        self._test_slang_tz(
            datetime.utcnow(), "one timezone to rule them all", pytz.utc)

    def test_est(self):
        # Sorry, Australia, US/Eastern is more common!
        self._test_slang_tz(
            datetime.utcnow(), "est", pytz.timezone("US/Eastern"))
        self._test_slang_tz(
            datetime.utcnow(), "edt", pytz.timezone("US/Eastern"))
        self._test_slang_tz(
            datetime.utcnow(), "eastern", pytz.timezone("US/Eastern"))

    def test_cst(self):
        self._test_slang_tz(
            datetime.utcnow(), "cst", pytz.timezone("US/Central"))
        self._test_slang_tz(
            datetime.utcnow(), "cdt", pytz.timezone("US/Central"))
        self._test_slang_tz(
            datetime.utcnow(), "central", pytz.timezone("US/Central"))

    def test_mst(self):
        self._test_slang_tz(
            datetime.utcnow(), "mst", pytz.timezone("US/Mountain"))
        self._test_slang_tz(
            datetime.utcnow(), "mdt", pytz.timezone("US/Mountain"))
        self._test_slang_tz(
            datetime.utcnow(), "mountain", pytz.timezone("US/Mountain"))

    def test_pst(self):
        self._test_slang_tz(
            datetime.utcnow(), "pst", pytz.timezone("US/Pacific"))
        self._test_slang_tz(
            datetime.utcnow(), "pdt", pytz.timezone("US/Pacific"))
        self._test_slang_tz(
            datetime.utcnow(), "pacific", pytz.timezone("US/Pacific"))

    def test_real_tz_name(self):
        self._test_slang_tz(
            datetime.utcnow(), "US/Pacific", pytz.timezone("US/Pacific"))
        self._test_slang_tz(
            datetime.utcnow(),
            "America/Los_Angeles",
            pytz.timezone("America/Los_Angeles"))
        self._test_slang_tz(
            datetime.utcnow(), "Africa/Cairo", pytz.timezone("Africa/Cairo"))


class TestConvert(TestCase):
    def test_from_local_time(self):
        ts = datetime.now(pytz.timezone("US/Pacific"))
        self.assertEqual(
            wtftz.convert(ts, 'utc'),
            pytz.utc.normalize(ts).replace(tzinfo=None))

    def test_sys_date(self):
        s = "Mon Dec 10 23:31:50 PST 2012"
        ts_pst = datetime(2012, 12, 10, 23, 31, 50)
        self.assertEqual(ts_pst, wtftz.convert(s, 'pst'))
        ts_utc = datetime(2012, 12, 11, 7, 31, 50)
        self.assertEqual(ts_utc, wtftz.convert(s, 'utc'))

    def test_naive(self):
        ts = datetime.utcnow()
        converted = wtftz.convert(ts, 'pst', naive=False)
        self.assertFalse(converted.tzinfo is None)
        self.assertEqual(converted.tzinfo, pytz.timezone("US/Pacific"))
