import unittest
import sys, os
sys.path.insert(0,'..')
from dao import odds_entities as oddities

class Test_add_odds(unittest.TestCase):
    def test(self):

        #Exact duplicate data (Only one should be added)
        odds1 = (1527129122, oddities.MoneyLineOdds("Caesars", -150, "CLE"))
        odds2 = (1527129122, oddities.MoneyLineOdds("Caesars", -150, "CLE"))
        odds3 = (1527129122, oddities.SpreadOdds("Atlantis", 110, "OKC", 4.5))
        odds4 = (1527129122, oddities.SpreadOdds("Atlantis", 110, "OKC", 4.5))

        #Consecutive timestamp no-change data (Only one should be added)
        odds5 = (1527129123, oddities.MoneyLineOdds("Caesars", -140, "CLE"))
        odds6 = (1527129124, oddities.MoneyLineOdds("Caesars", -140, "CLE"))
        odds7 = (1527129123, oddities.SpreadOdds("Atlantis", -110, "OKC", 5.5))
        odds8 = (1527129124, oddities.SpreadOdds("Atlantis", -110, "OKC", 5.5))

        #Consecutive timestamp with updated values (All should be added)
        odds9 =  (1527129125, oddities.MoneyLineOdds("Caesars", -140, "CLE"))
        odds10 = (1527129126, oddities.MoneyLineOdds("Caesars", -130, "CLE"))
        odds11 = (1527129125, oddities.SpreadOdds("Atlantis", -110, "OKC", 6.5))
        odds12 = (1527129126, oddities.SpreadOdds("Atlantis", -110, "OKC", 7.5))

        # A -> B -> B -> A consecutive timestamp pattern (Should add A,B,A)
        odds13 = (1527129127, oddities.MoneyLineOdds("Caesars", -120, "CLE"))
        odds14 = (1527129128, oddities.MoneyLineOdds("Caesars", -110, "CLE"))
        odds15 = (1527129129, oddities.MoneyLineOdds("Caesars", -110, "CLE"))
        odds16 = (1527129130, oddities.MoneyLineOdds("Caesars", -120, "CLE"))


        input_odds_list = [odds1, odds2, odds3, odds4, odds5, odds6, odds7, odds8,
                           odds9, odds10, odds11, odds12, odds13, odds14, odds14,
                           odds15, odds16]

        expected_output = [oddities.OddsOffering(odds1[0], odds1[1]), oddities.OddsOffering(odds5[0], odds5[1]),
                           oddities.OddsOffering(odds10[0], odds10[1]), oddities.OddsOffering(odds13[0], odds13[1]),
                           oddities.OddsOffering(odds14[0], odds14[1]), oddities.OddsOffering(odds16[0], odds16[1]),
                           oddities.OddsOffering(odds3[0], odds3[1]), oddities.OddsOffering(odds7[0], odds7[1]),
                           oddities.OddsOffering(odds11[0], odds11[1]), oddities.OddsOffering(odds12[0], odds12[1])]

        builder = oddities.OddsUpdateBuilder()

        for odds in input_odds_list:
            odds_offering = oddities.OddsOffering(odds[0], odds[1])
            builder.add_odds(odds_offering.timestamp, odds_offering.odds)

        odds_list = builder.build()

        for odds in odds_list:
            print(odds)

        self.assertEqual(odds_list, expected_output)

if __name__ == '__main__':
     unittest.main()
