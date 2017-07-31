import unittest
import pytz

from datetime import datetime, time, timedelta

from smsurvey.schedule.time_rule.time_rule import NoRepeatTimeRule, RepeatsDailyTimeRule


class TestNoRepeatTimeRule(unittest.TestCase):

    def test_gets_timestamp(self):
        now = datetime.now()
        tr = NoRepeatTimeRule(now)
        self.assertTrue(len(tr.get_date_times()) == 1)
        self.assertEqual(now, tr.get_date_times()[0])

    def test_from_params(self):
        tr = NoRepeatTimeRule.from_params("2020-12-12 11:59:12")
        self.assertTrue(len(tr.get_date_times()) == 1)
        self.assertEqual(datetime.strptime("2020-12-12 11:59:12", "%Y-%m-%d %H:%M:%S"), tr.get_date_times()[0])


class TestRepeatsDailyTimeRule(unittest.TestCase):

    def test_gets_timestamp(self):
        starting_from = datetime.now()
        every = 2
        until = starting_from + timedelta(days=100)
        run_at = time(tzinfo=pytz.utc).replace(hour=12, minute=0, second=0, microsecond=0)
        tr = RepeatsDailyTimeRule(starting_from, every, until, run_at)
        dts = tr.get_date_times()
        print(tr.to_params)
        self.assertTrue(len(dts) == 50)

        for dt in dts:
            self.assertEqual(dt.hour, run_at.hour)
            self.assertEqual(dt.minute, run_at.minute)
            self.assertEqual(dt.second, run_at.second)

    def test_from_params(self):
        params = "2017-07-31~2~2017-11-08~12:00:00 UTC"
        tr = RepeatsDailyTimeRule.from_params(params)
        dts = tr.get_date_times()
        self.assertTrue(len(dts) == 50)

        run_at = time(tzinfo=pytz.utc).replace(hour=12, minute=0, second=0, microsecond=0)

        for dt in dts:
            self.assertEqual(dt.hour, run_at.hour)
            self.assertEqual(dt.minute, run_at.minute)
            self.assertEqual(dt.second, run_at.second)