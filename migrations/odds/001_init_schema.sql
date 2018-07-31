CREATE TABLE IF NOT EXISTS vendor (
  vendor_id integer PRIMARY KEY,
  vendor_name varchar(1024) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS venue (
  venue_id integer PRIMARY KEY,
  venue_name varchar(1024) NOT NULL,
  location_name varchar(2048) NOT NULL,
  image_location varchar(2000),
  capacity integer,
  year_opened integer
);

CREATE TABLE IF NOT EXISTS sport (
  sport_id integer PRIMARY KEY,
  sport_name varchar(1024) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS sport_alias (
  sport_alias_id integer PRIMARY KEY,
  sport_id integer REFERENCES sport,
  sport_alias varchar(1024) NOT NULL
);

CREATE TABLE IF NOT EXISTS sport_alias_by_vendor (
  sport_alias_id integer REFERENCES sport_alias,
  vendor_id integer REFERENCES vendor,
  PRIMARY KEY(sport_alias_id, vendor_id)
);

CREATE TABLE IF NOT EXISTS team (
  team_id integer PRIMARY KEY,
  sport_id integer REFERENCES sport,
  venue_id integer REFERENCES venue,
  symbol varchar(4) NOT NULL,
  nickname varchar(1024) NOT NULL,
  UNIQUE(sport_id, symbol)
);

CREATE TABLE IF NOT EXISTS team_alias (
  team_alias_id integer PRIMARY KEY,
  team_id integer REFERENCES team,
  team_alias varchar(1024) NOT NULL
);

CREATE TABLE IF NOT EXISTS team_alias_by_vendor (
  team_alias_id integer REFERENCES team_alias,
  vendor_id integer REFERENCES vendor,
  PRIMARY KEY(team_alias_id, vendor_id)
);

CREATE TABLE IF NOT EXISTS sportsbook (
  sportsbook_id serial PRIMARY KEY,
  sportsbook_name varchar NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS sportsbook_alias (
  sportsbook_alias_id integer PRIMARY KEY,
  sportsbook_id integer REFERENCES sportsbook,
  sportsbook_alias varchar(1024) NOT NULL
);

CREATE TABLE IF NOT EXISTS sportsbook_alias_by_vendor (
  sportsbook_alias_id integer REFERENCES sportsbook_alias,
  vendor_id integer REFERENCES vendor,
  PRIMARY KEY(sportsbook_alias_id, vendor_id)
);

CREATE TABLE IF NOT EXISTS game (
  game_id uuid PRIMARY KEY,
  sport_id integer REFERENCES sport,
  home_team_id integer REFERENCES team,
  away_team_id integer REFERENCES team,
  venue_id integer REFERENCES venue,
  game_time_epoch_ms bigint,
  UNIQUE (sport_id, home_team_id, game_time_epoch_ms)
);

CREATE TABLE IF NOT EXISTS odds_type (
  odds_type_id integer PRIMARY KEY,
  odds_type_name varchar(128) NOT NULL,
  odds_type_abbreviation varchar(8)
);

CREATE TABLE IF NOT EXISTS odds (
  odds_id uuid PRIMARY KEY,
  odds_type_id integer REFERENCES odds_type,
  vendor_id integer REFERENCES vendor,
  sportsbook_id integer REFERENCES sportsbook,
  game_id uuid REFERENCES game,
  offered_time_epoch_ms bigint NOT NULL,
  odds integer NOT NULL,
  period varchar DEFAULT NULL,
  UNIQUE (odds_type_id, vendor_id, sportsbook_id, game_id, period, offered_time_epoch_ms)
);

CREATE TABLE IF NOT EXISTS money_line_odds (
  odds_id uuid references odds ON DELETE CASCADE,
  team_id integer references team,
  PRIMARY KEY (odds_id)
);

CREATE TABLE IF NOT EXISTS spread_odds (
  odds_id uuid references odds ON DELETE CASCADE,
  team_id integer references team,
  spread float NOT NULL,
  PRIMARY KEY (odds_id)
);

CREATE TABLE IF NOT EXISTS total_odds (
  odds_id uuid references odds ON DELETE CASCADE,
  total_score float NOT NULL,
  PRIMARY KEY (odds_id)
);

CREATE TABLE IF NOT EXISTS line_url_scheduling (
  normalized_url varchar(2000) PRIMARY KEY,
  sport_id integer NOT NULL REFERENCES sport,
  vendor_id integer NOT NULL REFERENCES vendor,
  event_time_epoch_ms bigint
);
