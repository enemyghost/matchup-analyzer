CREATE TABLE IF NOT EXISTS vendor (
  vendor_id integer PRIMARY KEY,
  vendor_name varchar(1024) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS sport (
  sport_id integer PRIMARY KEY,
  sport_name varchar(1024) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS sport_alias_by_vendor (
  vendor_id integer REFERENCES vendor DEFAULT NULL,
  sport_id integer REFERENCES sport,
  sport_alias varchar(1024) NOT NULL,
  PRIMARY KEY (vendor_id, sport_id)
);

CREATE TABLE IF NOT EXISTS line_url_scheduling (
  normalized_url varchar(2000) PRIMARY KEY,
  sport_id integer NOT NULL REFERENCES sport_alias_by_vedor,
  vendor_id integer NOT NULL REFERENCES vendor,
  event_time_epoch_ms bigint
);

CREATE TABLE IF NOT EXISTS sportsbook (
  sportsbook_id serial PRIMARY KEY,
  sportsbook_name varchar NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS game_data (
  game_id serial PRIMARY KEY,
  sport_id integer,
  vendor_id integer,
  game_time_epoch_ms bigint,
  home_team_id int REFERENCES team_alias_by_vendor,
  away_team_id int REFERENCES team_alias_by_vendor,
  UNIQUE (sport_id, game_time_epoch_ms, home_team_id, away_team_id)
);

CREATE TABLE IF NOT EXISTS team_alias_by_vendor (
    team_id serial PRIMARY KEY,
    team_symbol varchar(3),
    team_name varchar,
    team_name_full varchar,
    sport_id integer REFERENCES sport_alias_by_vendor,
    vendor_id integer REFERENCES vendor,
    UNIQUE (team_symbol, sport_id)
);

CREATE TABLE IF NOT EXISTS line_movement (
  line_id serial PRIMARY KEY,
  sportsbook_id int REFERENCES sportsbook,
  game_id int REFERENCES game_data,
  line_snapshot_time_epoch_ms bigint,
  fav_team_id int REFERENCES team_alias_by_vendor,
  dog_team_id int REFERENCES team_alias_by_vendor,
  money_line_fav_odds float,
  money_line_dog_odds float,
  spread float,
  spread_fav_odds float,
  spread_dog_odds float,
  over_under float,
  over_odds float,
  under_odds float,
  fst_half_odds float,
  snd_half_odds float,
  UNIQUE (sportsbook_id, game_id, line_snapshot_time_epoch_ms)
);
