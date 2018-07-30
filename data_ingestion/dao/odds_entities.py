class OddsMeta:
    def __init__(self, sportsbook, type, odds, period = None):
        self.sportsbook = sportsbook
        self.type = type
        self.odds = odds
        self.period = period

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.sportsbook == other.sportsbook and self.type == other.type and self.odds == other.odds

    def __str__(self):
        return "sportsbook: {}, type: {}, odds: {}{}".format(self.sportsbook, self.type, '+' if self.odds > 0 else '', self.odds)

    def specific_type(self):
        return "_".join([self.period if self.period is not None else "", self.type, "_FAV" if self.odds < 0 else "DOG"])

class SpreadOdds:
    def __init__(self, sportsbook, odds, team, spread, period = None):
        self.meta = OddsMeta(sportsbook, "SPREAD", odds, period)
        self.team = team
        self.spread = spread

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.meta == other.meta and self.team == other.team and self.spread == other.spread

    def __str__(self):
        return "{{ {}, team: {}, spread: {}{} }}".format(self.meta, self.team, '+' if self.spread > 0 else '', self.spread)

class MoneyLineOdds:
    def __init__(self, sportsbook, odds, team, period = None):
        self.meta = OddsMeta(sportsbook, "MONEY_LINE", odds, period)
        self.team = team

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.meta == other.meta and self.team == other.team

    def __str__(self):
        return "{{ {}, team: {} }}".format(self.meta, self.team)

class TotalOdds:
    def __init__(self, sportsbook, type, odds, total, period = None):
        if type not in ["UNDER", "OVER"]:
            raise ValueError("Total type must be UNDER or OVER")
        self.meta = OddsMeta(sportsbook, type, odds, period)
        self.total = total

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.meta == other.meta and self.total == other.total

    def __str__(self):
        return "{{ {}, total: {} }}".format(self.meta, self.total)

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
        if odds.meta.specific_type() not in sb_map:
            sb_map[odds.meta.specific_type()] = [OddsOffering(timestamp, odds)]
        else:
            odds_list = sb_map[odds.meta.specific_type()]
            if odds_list[-1].odds != odds:
                odds_list.append(OddsOffering(timestamp, odds))

    def build(self):
        odds_list = []
        for sb in self.odds_map:
            for type in self.odds_map[sb]:
                for odds in self.odds_map[sb][type]:
                    odds_list.append(odds)
        return odds_list

class LineUrl(object):
    def __init__(self, url, sport_id, vendor_id, event_time_epoch_ms = None):
        self.url = url
        self.sport_id = sport_id
        self.vendor_id = vendor_id
        self.event_time_epoch_ms = event_time_epoch_ms
