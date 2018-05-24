import unittest
import sys, os
from data_ingestion import odds

class Test_odds(unittest.TestCase):
    def test(self):
        builder = odds.OddsUpdateBuilder()
        builder.add_odds(1527129123, SpreadOdds("Caesars", -110, "OKC", 4.5))
        builder.add_odds(1527129124, SpreadOdds("Caesars", -110, "CLE", -4.5))
        builder.add_odds(1527129125, MoneyLineOdds("Caesars", 150, "OKC"))
        builder.add_odds(1527129126, MoneyLineOdds("Caesars", -150, "CLE"))
        builder.add_odds(1527129127, MoneyLineOdds("Caesars", -150, "CLE"))
        for odds in builder.build():
            print(odds)

if __name__ == '__main__':
     unittest.main()
