import unittest
import sys, os
sys.path.insert(0,'..')
from dao import odds_entities

class Test_odds(unittest.TestCase):
    def test(self):
        builder = odds_entities.OddsUpdateBuilder()
        builder.add_odds(1527129123, odds_entities.SpreadOdds("Caesars", -110, "OKC", 4.5))
        builder.add_odds(1527129124, odds_entities.SpreadOdds("Caesars", -110, "CLE", -4.5))
        builder.add_odds(1527129125, odds_entities.MoneyLineOdds("Caesars", 150, "OKC"))
        builder.add_odds(1527129126, odds_entities.MoneyLineOdds("Caesars", -150, "CLE"))
        builder.add_odds(1527129127, odds_entities.MoneyLineOdds("Caesars", -150, "CLE"))
        for odds in builder.build():
            print(odds)

if __name__ == '__main__':
     unittest.main()
