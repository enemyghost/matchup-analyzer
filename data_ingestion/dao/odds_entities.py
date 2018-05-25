class OddsMeta:
    def __init__(self, sportsbook, type, odds):
        self.sportsbook = sportsbook
        self.type = type
        self.odds = odds

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.sportsbook == other.sportsbook and self.type == other.type and self.odds == other.odds

    def __str__(self):
        return "sportsbook: {}, type: {}, odds: {}{}".format(self.sportsbook, self.type, '+' if self.odds > 0 else '', self.odds)

class SpreadOdds:
    def __init__(self, sportsbook, odds, team, spread):
        self.meta = OddsMeta(sportsbook, "SPREAD", odds)
        self.team = team
        self.spread = spread

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.meta == other.meta and self.team == other.team and self.spread == other.spread

    def __str__(self):
        return "{{ {}, team: {}, spread: {}{} }}".format(self.meta, self.team, '+' if self.spread > 0 else '', self.spread)

    def specific_type(self):
        if self.spread >= 0:
            return "SPREAD_FAV"
        else:
            return "SPREAD_DOG"

class MoneyLineOdds:
    def __init__(self, sportsbook, odds, team):
        self.meta = OddsMeta(sportsbook, "MONEY_LINE", odds)
        self.team = team

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.meta == other.meta and self.team == other.team

    def __str__(self):
        return "{{ {}, team: {} }}".format(self.meta, self.team)

    def specific_type(self):
        if self.meta.odds < 0:
            return "MONEY_LINE_FAV"
        else:
            return "MONEY_LINE_DOG"

class TotalOdds:
    def __init__(self, sportsbook, type, odds, total):
        if type not in ["UNDER", "OVER"]:
            raise ValueError("Total type must be UNDER or OVER")
        self.meta = OddsMeta(sportsbook, type, odds)
        self.total = total

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.meta == other.meta and self.total == other.total

    def __str__(self):
        return "{{ {}, total: {} }}".format(self.meta, self.team, self.total)

    def specific_type(self):
        return self.meta.type

class OddsOffering:
    def __init__(self, timestamp, odds):
        self.timestamp = timestamp
        self.odds = odds

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.timestamp == other.timestamp and self.odds == other.odds

    def __str__(self):
        return "{{ timestamp: {}, odds: {} }}".format(self.timestamp, self.odds)

class OddsUpdateBuilder:
    def __init__(self):
        self.odds_map = {}

    def add_odds(self, timestamp, odds):
        if odds.meta.sportsbook not in self.odds_map:
            self.odds_map[odds.meta.sportsbook] = {}
        sb_map = self.odds_map[odds.meta.sportsbook]
        if odds.specific_type() not in sb_map:
            sb_map[odds.specific_type()] = [OddsOffering(timestamp, odds)]
        else:
            odds_list = sb_map[odds.specific_type()]
            if odds_list[-1].odds != odds:
                odds_list.append(OddsOffering(timestamp, odds))

    def build(self):
        odds_list = []
        for sb in self.odds_map:
            for type in self.odds_map[sb]:
                for odds in self.odds_map[sb][type]:
                    odds_list.append(odds)
        return odds_list
