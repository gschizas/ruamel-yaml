# coding: utf-8

"""
http://yaml.org/type/timestamp.html specifies the regexp to use
for datetime.date and datetime.datetime construction. Date is simple
but datetime can have 'T' or 't' as well as 'Z' or a timezone offset (in
hours and minutes). This information was originally used to create
a UTC datetime and then discarded

examples from the above:

canonical:        2001-12-15T02:59:43.1Z
valid iso8601:    2001-12-14t21:59:43.10-05:00
space separated:  2001-12-14 21:59:43.10 -5
no time zone (Z): 2001-12-15 2:59:43.10
date (00:00:00Z): 2002-12-14

Please note that a fraction can only be included if not equal to 0

"""

import pytest    # NOQA
import ruamel.yaml   # NOQA

from roundtrip import round_trip, dedent, round_trip_load, round_trip_dump  # NOQA


class TestDateTime:
    def test_date_only(self):
        round_trip("""
        - 2011-10-02
        """, """
        - 2011-10-02
        """)

    def test_zero_fraction(self):
        round_trip("""
        - 2011-10-02 16:45:00.0
        """, """
        - 2011-10-02 16:45:00
        """)

    def test_long_fraction(self):
        round_trip("""
        - 2011-10-02 16:45:00.1234      # expand with zeros
        - 2011-10-02 16:45:00.123456
        - 2011-10-02 16:45:00.12345612  # round to microseconds
        - 2011-10-02 16:45:00.1234565   # round up
        - 2011-10-02 16:45:00.12345678  # round up
        """, """
        - 2011-10-02 16:45:00.123400    # expand with zeros
        - 2011-10-02 16:45:00.123456
        - 2011-10-02 16:45:00.123456    # round to microseconds
        - 2011-10-02 16:45:00.123457    # round up
        - 2011-10-02 16:45:00.123457    # round up
        """)

    def test_canonical(self):
        round_trip("""
        - 2011-10-02T16:45:00.1Z
        """, """
        - 2011-10-02T16:45:00.100000Z
        """)

    def test_spaced_timezone(self):
        round_trip("""
        - 2011-10-02T11:45:00 -5
        """, """
        - 2011-10-02T11:45:00-5
        """)

    def test_normal_timezone(self):
        round_trip("""
        - 2011-10-02T11:45:00-5
        - 2011-10-02 11:45:00-5
        - 2011-10-02T11:45:00-05:00
        - 2011-10-02 11:45:00-05:00
        """)

    def test_no_timezone(self):
        round_trip("""
        - 2011-10-02 6:45:00
        """, """
        - 2011-10-02 06:45:00
        """)

    def test_explicit_T(self):
        round_trip("""
        - 2011-10-02T16:45:00
        """, """
        - 2011-10-02T16:45:00
        """)

    def test_explicit_t(self):  # to upper
        round_trip("""
        - 2011-10-02t16:45:00
        """, """
        - 2011-10-02T16:45:00
        """)

    def test_no_T_multi_space(self):
        round_trip("""
        - 2011-10-02   16:45:00
        """, """
        - 2011-10-02 16:45:00
        """)

    def test_iso(self):
        round_trip("""
        - 2011-10-02T15:45:00+01:00
        """)

    def test_zero_tz(self):
        round_trip("""
        - 2011-10-02T15:45:00+0
        """)

    def test_issue_45(self):
        round_trip("""
        dt: 2016-08-19T22:45:47Z
        """)
