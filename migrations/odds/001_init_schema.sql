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
  sport_id integer NOT NULL REFERENCES sport,
  vendor_id integer NOT NULL REFERENCES vendor,
  event_time_epoch_ms bigint
);

CREATE TABLE IF NOT EXISTS game_data (
  sport_id integer NOT NULL REFERENCES sport,
  vendor_id integer NOT NULL REFERENCES vendor,
  home_team varchar,
  away_team varchar
);
