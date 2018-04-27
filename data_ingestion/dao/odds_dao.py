import psycopg2
import numpy as np
import os
import datetime as dt

class LineUrl(object):
  def __init__(self, url, sport_id, vendor_id, event_time_epoch_ms = None):
    self.url = url
    self.sport_id = sport_id
    self.vendor_id = vendor_id
    self.event_time_epoch_ms = event_time_epoch_ms

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
    sport_id = get_sport_id_for_vendor(vendor_id, sport_name)

  with OddsConnection() as conn:
    with conn.cursor() as cur:
      query = "INSERT INTO line_url_scheduling (normalized_url, sport_id, vendor_id, event_time_epoch_ms) VALUES (%s, %s, %s, %s) ON CONFLICT (normalized_url) DO UPDATE SET event_time_epoch_ms = %s WHERE line_url_scheduling.normalized_url = %s AND EXCLUDED.event_time_epoch_ms IS NOT NULL;"
      cur.execute(query, (url, sport_id, vendor_id, event_time_epoch_ms, event_time_epoch_ms, url))
      conn.commit()

def upsert_game_data(game_data = None, sport_id = None, vendor_id = None):
  """ Upserts the given game_data into the line_data table"""

  if game_data is not None:
    vendor_id = vendor_id
    sport_id = sport_id

  if sport_id is None:
    if sport_name is None:
      raise ValueError("Must provide either sport_id or sport_name")
    sport_id = get_sport_id_for_vendor(vendor_id, sport_name)


  with OddsConnection() as conn:
    with conn.cursor() as cur:
      query = "INSERT INTO game_data (sport_id, vendor_id, game_time_epoch_ms,  home_team, away_team) VALUES (%s, %s, %s, %s, %s);"
      cur.execute(query, (sport_id, vendor_id, game_data.game_timestamp,  game_data.home_team, game_data.away_team))
      game_id = cur.fetchone()
      conn.commit()


      for sportsbook_name, line_array in game_data.line_dict.items():
        query = "INSERT INTO sportsbook (sportsbook_name) VALUES (%s) ON CONFLICT DO NOTHING;"
        cur.execute(query, (sportsbook_name,))
        conn.commit()

        for line in line_array:
          sportsbook_id = get_sportsbook_id(sportsbook_name)
          query = "INSERT INTO line_movement (sportsbook_id, game_id, line_snapshot_time_epoch_ms, money_line_fav, money_line_dog, spread_fav, spread_dog, total_over, total_under, fst_half_fav, fst_half_dog, snd_half_fav, snd_half_dog) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;"
          cur.execute(query, (sportsbook_id, game_id, line[0], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11]))
          conn.commit()

def get_sportsbook_id(sportsbook_name):
    with OddsConnection() as conn:
      with conn.cursor() as cur:
        get_sportsbook_id_query ="SELECT sportsbook_id FROM sportsbook WHERE sportsbook_name = %s"
        cur.execute(get_sportsbook_id_query, (sportsbook_name,))
        id_result = cur.fetchone()
        if (id_result is None):
          raise ValueError("No sportsbook found for name '%s'" % (sportsbook_name))

        return id_result[0]

def get_sport_id_for_vendor(vendor_id, sport_name):
  """Finds the Sport ID for the given vendor_id/sport_name combo"""

  with OddsConnection() as conn:
    with conn.cursor() as cur:
      get_sport_id_query ="SELECT sport_id FROM sport_alias_by_vendor WHERE vendor_id = %s AND sport_alias = %s"
      cur.execute(get_sport_id_query, (vendor_id, sport_name))
      id_result = cur.fetchone()
      if (id_result is None):
        raise ValueError("No sport found for vendor %d and name '%s'" % (vendor_id, sport_name))

      return id_result[0]

def get_line_urls(vendor_id, sport_id = None, earliest_event_date_epoch_ms = 0):
  """Gets all urls from the line_url_scheduling table for the given vendor_id and sport_id, where the event date is null or greater than the given earliest_event_date_epoch_ms"""

  with OddsConnection() as conn:
    with conn.cursor() as cur:
      if (sport_id is None):
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
            yield LineUrl(result[0], result[1], result[2], result[3])
