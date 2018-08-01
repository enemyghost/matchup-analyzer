import psycopg2
import numpy as np
import os
import datetime as dt
import uuid
from data_ingestion.dao import odds_entities

class OddsConnection(object):
    def __init__(self):
        # Read database config from env.
        host = os.getenv("ODDS_DB_HOST", "localhost")
        dbname = os.getenv("ODDS_DB_NAME", "odds")
        user = os.getenv("ODDS_DB_USER")
        password = os.getenv("ODDS_DB_PASSWORD")

        if (host is None or dbname is None or user is None or password is None):
            raise ValueError("Could not load database config from env")

        self.connection_string = "host=%s dbname=%s user=%s password=%s" % (host, dbname, user, password)

    def __enter__(self):
        self.connection = psycopg2.connect(self.connection_string)
        return self.connection

    def __exit__(self, type, value, traceback):
        self.connection.close()

def upsert_line_url(url = None, vendor_id = None, sport_id = None, sport_name = None, event_time_epoch_ms = None, line_url = None):
    """ Upserts the given data into the line_url_scheduling table"""

    if line_url is not None:
        vendor_id = line_url.vendor_id
        sport_id = line_url.sport_id
        url = line_url.url
        event_time_epoch_ms = line_url.event_time_epoch_ms

    if url is None or vendor_id is None:
        raise ValueError("Must provide URL and vendor_id")

    if sport_id is None:
        if sport_name is None:
            raise ValueError("Must provide either sport_id or sport_name")
        sport_id = get_sport_id_for_alias(sport_name, vendor_id)

    with OddsConnection() as conn:
        with conn.cursor() as cur:
            query = "INSERT INTO line_url_scheduling (normalized_url, sport_id, vendor_id, event_time_epoch_ms) VALUES (%s, %s, %s, %s) ON CONFLICT (normalized_url) DO UPDATE SET event_time_epoch_ms = %s WHERE line_url_scheduling.normalized_url = %s AND EXCLUDED.event_time_epoch_ms IS NOT NULL;"
            cur.execute(query, (url, sport_id, vendor_id, event_time_epoch_ms, event_time_epoch_ms, url))
            conn.commit()

def upsert_game_data(game_data):
    """ Upserts the given game_data into the game_data and appropriate odds tables"""

    if game_data is None:
        raise ValueError("Game data is required")

    # TODO add validation of game_data fields
    vendor_id = game_data.vendor_id
    sport_id = game_data.sport_id
    game_time_epoch_ms = game_data.game_timestamp
    home_team_id = get_team_id_for_alias(game_data.home_team, vendor_id)
    away_team_id = get_team_id_for_alias(game_data.away_team, vendor_id)
    venue_id = get_venue_id_for_team(home_team_id)

    with OddsConnection() as conn:
        with conn.cursor() as cur:
            game_id = upsert_game(sport_id, home_team_id, away_team_id, venue_id, game_time_epoch_ms)
            cur.execute("DELETE FROM odds WHERE game_id = %s and vendor_id = %s", (game_id, vendor_id))

            known_team_ids = { }
            for offering in game_data.odds_list:
                odds_id = str(uuid.uuid4())
                period = offering.odds.meta.period
                odds = offering.odds.meta.odds
                sportsbook_id = get_sportsbook_id_for_alias(offering.odds.meta.sportsbook, vendor_id)
                offering_epoch_ms = offering.timestamp

                if isinstance(offering.odds, odds_entities.MoneyLineOdds):
                    team_id = known_team_ids.setdefault(offering.odds.team, get_team_id_for_alias(offering.odds.team, vendor_id))
                    insert_money_line_odds(cur, odds_id, vendor_id, sportsbook_id, game_id, offering_epoch_ms, team_id, odds, period)
                elif isinstance(offering.odds, odds_entities.SpreadOdds):
                    team_id = known_team_ids.setdefault(offering.odds.team, get_team_id_for_alias(offering.odds.team, vendor_id))
                    spread = offering.odds.spread
                    insert_spread_odds(cur, odds_id, vendor_id, sportsbook_id, game_id, offering_epoch_ms, team_id, spread, odds, period)
                elif isinstance(offering.odds, odds_entities.TotalOdds):
                    total_score = offering.odds.total
                    isUnder = True if offering.odds.meta.type == "UNDER" else False
                    insert_total_odds(cur, odds_id, vendor_id, sportsbook_id, game_id, offering_epoch_ms, total_score, odds, isUnder, period)
                else:
                    raise ValueError("Unhandled offering type " + str(type(offering)))
        conn.commit()

def upsert_game(sport_id, home_team_id, away_team_id, venue_id, game_time_epoch_ms):
    with OddsConnection() as conn:
        with conn.cursor() as cur:
            new_game_id = str(uuid.uuid4())
            upsert_game_query ="INSERT INTO game (game_id, sport_id, home_team_id, away_team_id, venue_id, game_time_epoch_ms) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;"
            cur.execute(upsert_game_query, (new_game_id, sport_id, home_team_id, away_team_id, venue_id, game_time_epoch_ms))
            conn.commit()
            return get_game_id(sport_id, home_team_id, game_time_epoch_ms)

def get_game_id(sport_id, home_team_id, game_time_epoch_ms):
    with OddsConnection() as conn:
        with conn.cursor() as cur:
            get_game_id_query = "SELECT game_id FROM game WHERE sport_id = %s AND home_team_id = %s AND game_time_epoch_ms = %s"
            cur.execute(get_game_id_query, (sport_id, home_team_id, game_time_epoch_ms))
            game_id = cur.fetchone()
            if (game_id is None):
                raise ValueError("No game found for sport_id: %s, game_timestamp: %s, home_team_id: %s" % (sport_id, game_timestamp, home_team_id))
            return game_id[0]

def insert_money_line_odds(cur, odds_id, vendor_id, sportsbook_id, game_id, offered_time_epoch_ms, team_id, odds, period = None):
    odds_query = "INSERT INTO odds (odds_id, odds_type_id, vendor_id, sportsbook_id, game_id, offered_time_epoch_ms, odds) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (odds_id) DO UPDATE SET odds = EXCLUDED.odds;"
    ml_odds_query = "INSERT INTO money_line_odds (odds_id, team_id) VALUES (%s, %s) ON CONFLICT (odds_id) DO UPDATE SET team_id = EXCLUDED.team_id;"
    cur.execute(odds_query, (odds_id, 1, vendor_id, sportsbook_id, game_id, offered_time_epoch_ms, odds))
    cur.execute(ml_odds_query, (odds_id, team_id))
    if (period is not None and (period == 1 or period == 2)):
        cur.execute("UPDATE odds SET period = '%s' WHERE odds_id = %s", (period, odds_id))

def insert_spread_odds(cur, odds_id, vendor_id, sportsbook_id, game_id, offered_time_epoch_ms, team_id, spread, odds, period = None):
    odds_query = "INSERT INTO odds (odds_id, odds_type_id, vendor_id, sportsbook_id, game_id, offered_time_epoch_ms, odds) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (odds_id) DO UPDATE SET odds = EXCLUDED.odds;"
    spread_odds_query = "INSERT INTO spread_odds (odds_id, team_id, spread) VALUES (%s, %s, %s) ON CONFLICT (odds_id) DO UPDATE SET team_id = EXCLUDED.team_id, spread = EXCLUDED.spread;"
    cur.execute(odds_query, (odds_id, 2, vendor_id, sportsbook_id, game_id, offered_time_epoch_ms, odds))
    cur.execute(spread_odds_query, (odds_id, team_id, spread))
    if (period is not None and (period == 1 or period == 2)):
        cur.execute("UPDATE odds SET period = '%s' WHERE odds_id = %s", (period, odds_id))

def insert_total_odds(cur, odds_id, vendor_id, sportsbook_id, game_id, offered_time_epoch_ms, total_score, odds, isUnder, period = None):
    odds_query = "INSERT INTO odds (odds_id, odds_type_id, vendor_id, sportsbook_id, game_id, offered_time_epoch_ms, odds) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (odds_id) DO UPDATE SET odds = EXCLUDED.odds;"
    total_odds_query = "INSERT INTO total_odds (odds_id, total_score) VALUES (%s, %s) ON CONFLICT (odds_id) DO UPDATE SET total_score = EXCLUDED.total_score;"
    cur.execute(odds_query, (odds_id, 3 if isUnder else 4, vendor_id, sportsbook_id, game_id, offered_time_epoch_ms, odds))
    cur.execute(total_odds_query, (odds_id, total_score))
    if (period is not None and (period == 1 or period == 2)):
        cur.execute("UPDATE odds SET period = '%s' WHERE odds_id = %s", (period, odds_id))

def get_sportsbook_id_for_alias(sportsbook_alias, vendor_id):
    with OddsConnection() as conn:
        with conn.cursor() as cur:
            get_sportsbook_id_query ="SELECT sa.sportsbook_id FROM sportsbook_alias sa INNER JOIN sportsbook_alias_by_vendor sav USING (sportsbook_alias_id) WHERE sa.sportsbook_alias = %s AND sav.vendor_id = %s;"
            cur.execute(get_sportsbook_id_query, (sportsbook_alias,vendor_id))
            sportsbook_id = cur.fetchone()
            if (sportsbook_id is None):
                raise ValueError("No sportsbook found for name %s and vendor %s" % (sportsbook_alias, vendor_id))
            return sportsbook_id[0]

def get_team_id_for_alias(team_alias, vendor_id):
    with OddsConnection() as conn:
        with conn.cursor() as cur:
            get_team_id_query = "SELECT team_id FROM team_alias ta INNER JOIN team_alias_by_vendor tav USING(team_alias_id) WHERE ta.team_alias = %s AND tav.vendor_id = %s;"
            cur.execute(get_team_id_query, (team_alias, vendor_id))
            team_id = cur.fetchone()
            if (team_id is None):
                raise ValueError("No team found for team name %s, vendor %s" % (team_alias, vendor_id))
            return team_id

def get_sport_id_for_alias(sport_alias, vendor_id):
    """Finds the Sport ID for the given vendor_id/sport_name combo"""
    with OddsConnection() as conn:
        with conn.cursor() as cur:
            get_sport_id_query ="SELECT sport_id FROM sport_alias sa INNER JOIN sport_alias_by_vendor sav USING(sport_alias_id) WHERE sa.sport_alias = %s AND sav.vendor_id = %s;"
            cur.execute(get_sport_id_query, (sport_alias, vendor_id))
            sport_id = cur.fetchone()
            if (sport_id is None):
                raise ValueError("No sport found for sport name %s, vendor %d" % (sport_alias, vendor_id))
            return sport_id[0]

def get_venue_id_for_team(home_team_id):
    with OddsConnection() as conn:
        with conn.cursor() as cur:
            get_venue_query="SELECT venue_id FROM team where team_id = %s"
            cur.execute(get_venue_query, (home_team_id))
            venue_id = cur.fetchone()
            if (venue_id is None):
                raise ValueError("No venue found for home team %s" % (home_team_id))
            return venue_id[0]

def get_line_urls(vendor_id, sport_id = None, earliest_event_date_epoch_ms = 0):
    """Gets all urls from the line_url_scheduling table for the given vendor_id and sport_id, where the event date is null or greater than the given earliest_event_date_epoch_ms"""
    with OddsConnection() as conn:
        with conn.cursor() as cur:
            if sport_id is None:
                query = "SELECT normalized_url, sport_id, vendor_id, event_time_epoch_ms FROM line_url_scheduling WHERE vendor_id = %s AND (event_time_epoch_ms IS NULL OR event_time_epoch_ms >= %s) ORDER BY vendor_id, sport_id, event_time_epoch_ms;"
                cur.execute(query, (vendor_id, earliest_event_date_epoch_ms))
            else:
                query = "SELECT normalized_url, sport_id, vendor_id, event_time_epoch_ms FROM line_url_scheduling WHERE vendor_id = %s AND (event_time_epoch_ms IS NULL OR event_time_epoch_ms >= %s) AND sport_id = %s ORDER BY vendor_id, sport_id, event_time_epoch_ms;"
                cur.execute(query, (vendor_id, earliest_event_date_epoch_ms, sport_id))

            while True:
                results = cur.fetchmany(100)
                if not results:
                    break
                for result in results:
                    yield odds_entities.LineUrl(result[0], result[1], result[2], result[3])
