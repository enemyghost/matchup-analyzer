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

CREATE TABLE IF NOT EXISTS sportsbook (
  sportsbook_id serial PRIMARY KEY,
  sportsbook_name varchar NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS game_data (
  game_id serial PRIMARY KEY,
  sport_id integer,
  vendor_id integer,
  game_time_epoch_ms bigint,
  home_team varchar,
  away_team varchar,
  UNIQUE (sport_id, game_time_epoch_ms, home_team, away_team)
);

CREATE TABLE IF NOT EXISTS team (
    team_id serial PRIMARY KEY,
    sport_id integer,
    team_name varchar NOT NULL UNIQUE,
    team_abbr varchar
);

CREATE TABLE IF NOT EXISTS line_movement (
  line_id serial PRIMARY KEY,
  sportsbook_id int REFERENCES sportsbook,
  game_id int REFERENCES game_data,
  line_snapshot_time_epoch_ms bigint,
  money_line_fav varchar,
  money_line_dog varchar,
  spread_fav varchar,
  spread_dog varchar,
  total_over varchar,
  total_under varchar,
  fst_half_fav varchar,
  fst_half_dog varchar,
  snd_half_fav varchar,
  snd_half_dog varchar,
  UNIQUE (sportsbook_id, game_id, line_snapshot_time_epoch_ms)
);
