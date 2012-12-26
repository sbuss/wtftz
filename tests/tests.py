from datetime import datetime
import time
from unittest import TestCase

import pytz

import wtftz
from wtftz.parser import free_text


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
        ts = datetime.fromtimestamp(float(epoch))
        self._test_times(epoch, _truncate_time(ts))

    def test_utc_epoch_milliseconds(self):
        ts = datetime.utcnow()
        epoch = _epoch(ts)
        epoch += ".{us}".format(us=ts.microsecond)
        # datetime.fromtimestamp, which wtftz uses, always adds 0s to epochs,
        # so re-parse the timestamp so the results will always match.
        ts = datetime.fromtimestamp(float(epoch))
        self._test_times(epoch, ts)

    def test_trailing_zero(self):
        ts = datetime(2012, 12, 23, 14, 48, 0)
        epoch = _epoch(ts)
        epoch += ".{us}".format(us=ts.microsecond)
        ts = datetime.fromtimestamp(float(epoch))
        self._test_times(epoch, ts)

        ts = datetime(2012, 12, 23, 14, 48, 0, 9292)
        epoch = _epoch(ts)
        epoch += ".{us}".format(us=ts.microsecond)
        ts = datetime.fromtimestamp(float(epoch))
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

    def test_caps(self):
        self._test_slang_tz(
            datetime.utcnow(), "UTC", pytz.utc)
        self._test_slang_tz(
            datetime.utcnow(), "PST", pytz.timezone("US/Pacific"))

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
        #TODO: Make this test pass
        s = "Mon Dec 10 23:31:50 EST 2012"
        ts_pst = datetime(2012, 12, 10, 20, 31, 50)
        self.assertEqual(ts_pst, wtftz.convert(s, 'pst'))
        ts_utc = datetime(2012, 12, 11, 4, 31, 50)
        self.assertEqual(ts_utc, wtftz.convert(s, 'utc'))

    def test_naive(self):
        ts = datetime.utcnow()
        converted = wtftz.convert(ts, 'pst', naive=False)
        self.assertFalse(converted.tzinfo is None)
        self.assertEqual(converted.tzinfo, pytz.timezone("US/Pacific"))


class TestTimestampStrings(TestCase):
    def test_isoformat_utc(self):
        ts = datetime.utcnow()
        self.assertEqual(wtftz.convert(ts.isoformat(), 'utc'), ts)

    def test_isoformat_tz(self):
        ts = datetime.now(pytz.timezone("US/Pacific"))
        self.assertEqual(wtftz.convert(ts.isoformat(), 'pst', naive=False), ts)
        # Lie about the source timezone
        self.assertEqual(wtftz.convert(
            ts.isoformat(), from_tz='utc', to_tz='pst', naive=False), ts)


class TestFromTo(TestCase):
    def setUp(self):
        self.utc_ts = datetime.utcnow()
        self.utc_ts_str = self.utc_ts.isoformat()

        self.est_ts = _convert(self.utc_ts, to_tz=pytz.timezone("US/Eastern"))
        self.est_ts_str = self.est_ts.isoformat()

    def test_from_and_to(self):
        query = "{ts} from utc to est".format(ts=self.utc_ts.isoformat())
        result = wtftz.convert_free(query)
        self.assertEqual(result, self.est_ts)

        query = "{ts} from est to utc".format(ts=self.est_ts_str)
        result = wtftz.convert_free(query)
        self.assertEqual(result, self.utc_ts)

    def test_to(self):
        query = "{ts} to est".format(ts=self.utc_ts.isoformat())
        result = wtftz.convert_free(query)
        self.assertEqual(result, self.est_ts)

        est_stamped = self.est_ts.replace(tzinfo=pytz.timezone("US/Eastern"))
        query = "{ts} to est".format(ts=est_stamped.isoformat())
        result = wtftz.convert_free(query)
        self.assertEqual(result, self.est_ts)

        query = "{ts} to utc".format(ts=est_stamped.isoformat())
        result = wtftz.convert_free(query)
        self.assertEqual(result, self.utc_ts)

    def test_isoformat_tz_doesnt_match(self):
        est_stamped = self.est_ts.replace(tzinfo=pytz.timezone("US/Eastern"))
        query = "{ts} from utc to est".format(ts=est_stamped.isoformat())
        result = wtftz.convert_free(query)
        self.assertEqual(result, self.est_ts)

    def test_naive(self):
        ts = datetime.utcnow()
        converted = wtftz.convert_free("%s to pst" % ts, naive=False)
        self.assertFalse(converted.tzinfo is None)
        self.assertEqual(converted.tzinfo, pytz.timezone("US/Pacific"))

    def test_sysdate_free(self):
        s = "Mon Dec 10 23:31:50 EST 2012"
        ts_pst = datetime(2012, 12, 10, 20, 31, 50)
        query = "%s to pst" % s
        self.assertEqual(ts_pst, wtftz.convert_free(query))

    def test_sysdate_tz_doesnt_match(self):
        # TODO: Make this test pass
        s = "Mon Dec 10 23:31:50 EST 2012"
        target = datetime(2012, 12, 10, 20, 31, 50)
        query = "{ts} from utc to pst".format(ts=s)
        result = wtftz.convert_free(query)
        self.assertEqual(result, target)

    def _test_extraction(self, query, ts, fromz, toz):
        _ts, _fromz, _toz = free_text(query)
        self.assertEqual(ts, _ts)
        self.assertEqual(fromz, _fromz)
        self.assertEqual(toz, _toz)

    def test_simple_extraction(self):
        query_template = "{ts} from {fromz} to {toz}"
        query = query_template.format(ts=self.utc_ts_str,
                                      fromz="utc",
                                      toz="est")
        self._test_extraction(query, self.utc_ts_str, "utc", "est")
        query = query_template.format(ts=self.est_ts_str,
                                      fromz="gmt",
                                      toz="pdt")
        self._test_extraction(query, self.est_ts_str, "gmt", "pdt")
        query = query_template.format(ts=self.est_ts_str,
                                      fromz="est",
                                      toz="US/NewYork")
        self._test_extraction(query, self.est_ts_str, "est", "US/NewYork")

    def test_complex_extraction(self):
        query_template = "{ts} from {fromz} to {toz}"
        query = query_template.format(ts=self.utc_ts_str,
                                      fromz="the one true timezone",
                                      toz="US/Eastern")
        self._test_extraction(
            query, self.utc_ts_str, "the one true timezone", "US/Eastern")
        query = query_template.format(ts="4am",
                                      fromz="los angeles",
                                      toz="US/Central")
        self._test_extraction(
            query, "4am", "los angeles", "US/Central")

    def test_extraction_no_from(self):
        query_template = "{ts} to {toz}"
        query = query_template.format(ts=self.utc_ts_str,
                                      toz="US/Eastern")
        self._test_extraction(
            query, self.utc_ts_str, None, "US/Eastern")
        query = query_template.format(ts=self.est_ts_str,
                                      toz="US/Pacific")
        self._test_extraction(
            query, self.est_ts_str, None, "US/Pacific")

    def test_extraction_no_from_keyword(self):
        query_template = "{ts} {fromz} to {toz}"
        query = query_template.format(ts=self.est_ts_str,
                                      fromz="EST",
                                      toz="US/Pacific")
        self._test_extraction(
            query, self.est_ts_str, "EST", "US/Pacific")


class TestTimesWithoutDates(TestCase):
    def test_simple_bare_times(self):
        ts = wtftz.convert("10am", 'utc')
        self.assertEqual(ts.hour, 10)
        self.assertEqual(ts.minute, 0)
        ts = wtftz.convert("10pm", 'utc')
        self.assertEqual(ts.hour, 22)
        self.assertEqual(ts.minute, 0)
        day = ts.day

        ts = wtftz.convert("10pm", 'pst')
        self.assertEqual(ts.hour, 14)
        self.assertEqual(ts.day, day)
        self.assertEqual(ts.minute, 0)
        ts = wtftz.convert("10am", 'pst')
        self.assertEqual(ts.hour, 2)
        self.assertEqual(ts.day, day)
        self.assertEqual(ts.minute, 0)

    def test_times_with_minutes(self):
        ts = wtftz.convert("10:15pm", 'pst')
        self.assertEqual(ts.hour, 14)
        self.assertEqual(ts.minute, 15)
        self.assertEqual(
            wtftz.convert(_epoch(ts), from_tz="pst", to_tz="utc"),
            wtftz.convert(ts, from_tz="pdt", to_tz="utc"))
