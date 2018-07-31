import unittest
import sys, os
sys.path.insert(0,'..')
from data_ingestion.crawlers.spiders import parse_line_tables as parser

sportsbook = 'Atlantis'

class Test_odds_parsers(unittest.TestCase):

    def assert_equality(self, actual, odds, sportsbook_input, team=None, period=None, spread=None, total=None):
        if team is not None:
            self.assertEqual(actual.team, team)
        if spread is not None:
            self.assertEqual(actual.spread, spread)
        if total is not None:
            self.assertEqual(actual.total, total)
        self.assertEqual(actual.meta.odds, odds)
        self.assertEqual(actual.meta.sportsbook, sportsbook_input)
        self.assertEqual(actual.meta.period, period)


    def test_money_line_blank_string(self):
        blank_string = ''
        actual = parser.convert_money_line_string_to_odds_object(blank_string, sportsbook)
        self.assertEqual(actual, None)

    def test_money_line_negative(self):
        money_line_string_negative = 'MIA-190'
        actual = parser.convert_money_line_string_to_odds_object(money_line_string_negative, sportsbook)
        self.assert_equality(actual, odds=-190, team="MIA", sportsbook_input=sportsbook, period=None)

    def test_money_line_positive(self):
        money_line_string_positive = 'ATL+225'
        actual = parser.convert_money_line_string_to_odds_object(money_line_string_positive, sportsbook)
        self.assert_equality(actual, odds=225, team="ATL", sportsbook_input=sportsbook, period=None)

    def test_money_line_no_odds(self):
        money_line_string_no_odds = 'LAC XX'
        actual = parser.convert_money_line_string_to_odds_object(money_line_string_no_odds, sportsbook)
        self.assertEqual(actual, None)

    def test_spread_negative_int(self):
        spread_string_negative_int = 'LAC-3 -110'
        actual = parser.convert_spread_string_to_odds_object(spread_string_negative_int, sportsbook)
        self.assert_equality(actual, odds=-110, team="LAC", sportsbook_input=sportsbook, period=None, spread=-3)

    def test_spread_negative_decinmal(self):
        spread_string_negative_decimal = 'LAC-3.5 -110'
        actual = parser.convert_spread_string_to_odds_object(spread_string_negative_decimal, sportsbook)
        self.assert_equality(actual, odds=-110, team="LAC", sportsbook_input=sportsbook, period=None, spread=-3.5)

    def test_spread_positive_int(self):
        spread_string_positive_int = 'TOR+3 -110'
        actual = parser.convert_spread_string_to_odds_object(spread_string_positive_int, sportsbook)
        self.assert_equality(actual, odds=-110, team="TOR", sportsbook_input=sportsbook, period=None, spread=3)

    def test_spread_positive_decimal(self):
        spread_string_positive_decimal = 'TOR+2.5 -110'
        actual = parser.convert_spread_string_to_odds_object(spread_string_positive_decimal, sportsbook)
        self.assert_equality(actual, odds=-110, team="TOR", sportsbook_input=sportsbook, period=None, spread=2.5)

    def test_spread_pk(self):
        spread_string_pk = 'TORPK -110'
        actual = parser.convert_spread_string_to_odds_object(spread_string_pk, sportsbook)
        self.assert_equality(actual, odds=-110, team="TOR", sportsbook_input=sportsbook, period=None, spread=0)

    def test_spread_xx_xx(self):
        spread_string_xx_xx = 'PHIXX XX'
        actual = parser.convert_spread_string_to_odds_object(spread_string_xx_xx, sportsbook)
        self.assertEqual(actual, None)

    def test_over_under_int(self):
        over_under_int = '47.0 -110'
        actual = parser.convert_total_over_to_odds_object(over_under_int, sportsbook)
        self.assert_equality(actual, odds=-110, team=None, sportsbook_input=sportsbook, spread=None, period=None, total=47.0)

    def test_over_under_decimal(self):
        over_under_decimal = '46.5 -110'
        actual = parser.convert_total_over_to_odds_object(over_under_decimal, sportsbook)
        self.assert_equality(actual, odds=-110, team=None, sportsbook_input=sportsbook, spread=None, period=None, total=46.5)

    def test_over_under_xx_xx(self):
        over_under_xx_xx = 'XX XX'
        actual = parser.convert_total_over_to_odds_object(over_under_xx_xx, sportsbook)
        self.assertEqual(actual, None)

    def test_period_negative_decimal(self):
        period_negative_decimal = 'DAL-0.5'
        actual = parser.convert_period_to_odds_object(period_negative_decimal, sportsbook, period=1)
        self.assert_equality(actual, odds=-110, team="DAL", spread=-0.5, sportsbook_input=sportsbook, period=1)

    def test_period_negative_decimal(self):
        period_positive_decimal = 'DAL+1.5'
        actual = parser.convert_period_to_odds_object(period_positive_decimal, sportsbook, period=1)
        self.assert_equality(actual, odds=-110, team="DAL", spread=1.5, sportsbook_input=sportsbook, period=1)

    def test_period_negative_decimal(self):
        period_negative_int = 'GNB-2'
        actual = parser.convert_period_to_odds_object(period_negative_int, sportsbook, period=2)
        self.assert_equality(actual, odds=-110, team="GNB", spread=-2, sportsbook_input=sportsbook, period=2)

    def test_period_negative_decimal(self):
        period_positive_int = 'DAL+2'
        actual = parser.convert_period_to_odds_object(period_positive_int, sportsbook, period=2)
        self.assert_equality(actual, odds=-110, team="DAL", spread=2, sportsbook_input=sportsbook, period=2)

    def test_period_pk(self):
        period_pk = 'GNBPK'
        actual = parser.convert_period_to_odds_object(period_pk, sportsbook, period=2)
        self.assert_equality(actual, odds=-110, team="GNB", spread=0, sportsbook_input=sportsbook, period=2)

if __name__ == '__main__':
     unittest.main()
