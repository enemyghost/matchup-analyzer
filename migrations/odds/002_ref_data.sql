INSERT INTO vendor (vendor_id, vendor_name) VALUES
  (1, 'vegas insider')
ON CONFLICT DO NOTHING;

INSERT INTO sport (sport_id, sport_name) VALUES
  (1, 'nfl'),
  (2, 'nba'),
  (3, 'ncaam basketball'),
  (4, 'ncaa football'),
  (5, 'mlb'),
  (6, 'nhl')
ON CONFLICT DO NOTHING;

INSERT INTO sport_alias (sport_alias_id, sport_id, sport_alias) VALUES
  (1, 1, 'nfl'),
  (2, 2, 'nba'),
  (3, 3, 'ncaam basketball'),
  (4, 4, 'ncaa football'),
  (5, 5, 'mlb'),
  (6, 6, 'nhl'),
  (7, 3, 'college-basketball'),
  (8, 4, 'college-football')
ON CONFLICT DO NOTHING;

INSERT INTO sport_alias_by_vendor (sport_alias_id, vendor_id) VALUES
  (1, 1),
  (2, 1),
  (5, 1),
  (6, 1),
  (7, 1),
  (8, 1)
ON CONFLICT DO NOTHING;

INSERT INTO sportsbook (sportsbook_id, sportsbook_name) VALUES
  (1, 'VI Consensus'),
  (2, 'Atlantis'),
  (3, 'Caesars'),
  (4, 'CG Technology'),
  (5, 'Coasts Line'),
  (6, 'Golden Nugget'),
  (7, 'Peppermill'),
  (8, 'Southpoint'),
  (9, 'Stations'),
  (10, 'Stratosphere'),
  (11, 'Treasure Island'),
  (12, 'Westgate Superbook'),
  (13, 'William Hill'),
  (14, '5dimes'),
  (15, 'Bet Horizon'),
  (16, 'BETDSI'),
  (17, 'betonline.ag'),
  (18, 'betis.com'),
  (19, 'Bookmaker'),
  (20, 'bovada.lv'),
  (21, 'Carbonsports'),
  (22, 'gtbets.eu'),
  (23, 'Heritage'),
  (24, 'Intertops'),
  (25, 'mybookie.ag'),
  (26, 'PinnacleSports'),
  (27, 'SBG Global'),
  (28, 'sportbet.com'),
  (29, 'sportsbetting.com'),
  (30, 'sportsbook.ag'),
  (31, 'SportsInteraction'),
  (32, 'The Greek'),
  (33, 'topbet.com'),
  (34, 'youwager.eu')
ON CONFLICT DO NOTHING;

INSERT INTO sportsbook_alias (sportsbook_alias_id, sportsbook_id, sportsbook_alias)
  SELECT sportsbook_id, sportsbook_id, UPPER(sportsbook_name)
  FROM sportsbook
ON CONFLICT DO NOTHING;

INSERT INTO sportsbook_alias_by_vendor (sportsbook_alias_id, vendor_id)
  SELECT sportsbook_alias_id, 1
  FROM sportsbook_alias
ON CONFLICT DO NOTHING;

INSERT INTO venue (venue_id, venue_name, location_name, capacity, year_opened) VALUES
  (1, 'Air Canada Centre', 'Toronto, Ontario', 19800, 1999),
  (2, 'American Airlines Arena', 'Miami, Florida', 19600, 1999),
  (3, 'American Airlines Center', 'Dallas, Texas', 19200, 2001),
  (4, 'Amway Center', 'Orlando, Florida', 18846, 2010),
  (5, 'AT&T Center', 'San Antonio, Texas', 18418, 2002),
  (6, 'Bankers Life Fieldhouse', 'Indianapolis, Indiana', 17923, 1999),
  (7, 'Barclays Center', 'Brooklyn, New York', 17732, 2012),
  (8, 'Capital One Arena', 'Washington, D.C.', 20356, 1997),
  (9, 'Chesapeake Energy Arena', 'Oklahoma City, Oklahoma', 18203, 2002),
  (10, 'FedExForum', 'Memphis, Tennessee', 18119, 2004),
  (11, 'Golden 1 Center', 'Sacramento, California', 17608, 2016),
  (12, 'Little Caesars Arena', 'Detroit, Michigan', 20491, 2017),
  (13, 'Madison Square Garden', 'New York, New York', 19812, 1968),
  (14, 'Moda Center', 'Portland, Oregon', 19980, 1995),
  (15, 'Oracle Arena', 'Oakland, California', 19596, 1966),
  (16, 'Pepsi Center', 'Denver, Colorado', 19155, 1999),
  (17, 'Philips Arena', 'Atlanta, Georgia', 18118, 1999),
  (18, 'Quicken Loans Arena', 'Cleveland, Ohio', 20562, 1994),
  (19, 'Smoothie King Center', 'New Orleans, Louisiana', 16867, 1999),
  (20, 'Spectrum Center', 'Charlotte, North Carolina', 19077, 2005),
  (21, 'Staples Center', 'Los Angeles, California', 19060, 1999),
  (22, 'Staples Center', 'Los Angeles, California', 18997, 1999),
  (23, 'Talking Stick Resort Arena', 'Phoenix, Arizona', 18422, 1992),
  (24, 'Target Center', 'Minneapolis, Minnesota', 19356, 1990),
  (25, 'TD Garden', 'Boston, Massachusetts', 18624, 1995),
  (26, 'Toyota Center', 'Houston, Texas', 18055, 2003),
  (27, 'United Center', 'Chicago, Illinois', 20917, 1994),
  (28, 'Vivint Smart Home Arena', 'Salt Lake City, Utah', 18303, 1991),
  (29, 'Wells Fargo Center', 'Philadelphia, Pennsylvania', 20328, 1996),
  (30, 'Wisconsin Entertainment and Sports Center', 'Milwaukee, Wisconsin', 17500, 2018)
ON CONFLICT DO NOTHING;

INSERT INTO team (team_id, sport_id, venue_id, symbol, nickname) VALUES
  (1, 2, 1, 'TOR', 'Toronto Raptors'),
  (2, 2, 2, 'MIA', 'Miami Heat'),
  (3, 2, 3, 'DAL', 'Dallas Mavericks'),
  (4, 2, 4, 'ORL', 'Orlando Magic'),
  (5, 2, 5, 'SAS', 'San Antonio Spurs'),
  (6, 2, 6, 'IND', 'Indiana Pacers'),
  (7, 2, 7, 'BKN', 'Brooklyn Nets'),
  (8, 2, 8, 'WAS', 'Washington Wizards'),
  (9, 2, 9, 'OKL', 'Oklahoma City Thunder'),
  (10, 2, 10, 'MEM', 'Memphis Grizzlies'),
  (11, 2, 11, 'SAC', 'Sacramento Kings'),
  (12, 2, 12, 'DET', 'Detroit Pistons'),
  (13, 2, 13, 'NYK', 'New York Knicks'),
  (14, 2, 14, 'POR', 'Portland Trail Blazers'),
  (15, 2, 15, 'GSW', 'Golden State Warriors'),
  (16, 2, 16, 'DEN', 'Denver Nuggets'),
  (17, 2, 17, 'ATL', 'Atlanta Hawks'),
  (18, 2, 18, 'CLE', 'Cleveland Cavaliers'),
  (19, 2, 19, 'NOP', 'New Orleans Pelicans'),
  (20, 2, 20, 'CHA', 'Charlotte Hornets'),
  (21, 2, 21, 'LAC', 'Los Angeles Clippers'),
  (22, 2, 22, 'LAL', 'Los Angeles Lakers'),
  (23, 2, 23, 'PHX', 'Phoenix Suns'),
  (24, 2, 24, 'MIN', 'Minnesota Timberwolves'),
  (25, 2, 25, 'BOS', 'Boston Celtics'),
  (26, 2, 26, 'HOU', 'Houston Rockets'),
  (27, 2, 27, 'CHI', 'Chicago Bulls'),
  (28, 2, 28, 'UTH', 'Utah Jazz'),
  (29, 2, 29, 'PHI', 'Philadelphia 76ers'),
  (30, 2, 30, 'MIL', 'Milwaukee Bucks')
ON CONFLICT DO NOTHING;

INSERT INTO team_alias (team_alias_id, team_id, team_alias) VALUES
  (1, 1, 'TOR'),
  (2, 1, 'Toronto Raptors'),
  (3, 1, 'Raptors'),
  (4, 2, 'MIA'),
  (5, 2, 'Miami Heat'),
  (6, 2, 'Heat'),
  (7, 3, 'DAL'),
  (8, 3, 'Dallas Mavericks'),
  (9, 3, 'Mavericks'),
  (10, 4, 'ORL'),
  (11, 4, 'Orlando Magic'),
  (12, 4, 'Magic'),
  (13, 5, 'SAS'),
  (14, 5, 'San Antonio Spurs'),
  (15, 5, 'Spurs'),
  (16, 6, 'IND'),
  (17, 6, 'Indiana Pacers'),
  (18, 6, 'Pacers'),
  (19, 7, 'BKN'),
  (20, 7, 'Brooklyn Nets'),
  (21, 7, 'Nets'),
  (22, 8, 'WAS'),
  (23, 8, 'Washington Wizards'),
  (24, 8, 'Wizards'),
  (25, 9, 'OKL'),
  (26, 9, 'Oklahoma City Thunder'),
  (27, 9, 'Thunder'),
  (28, 10, 'MEM'),
  (29, 10, 'Memphis Grizzlies'),
  (30, 10, 'Grizzlies'),
  (31, 11, 'SAC'),
  (32, 11, 'Sacramento Kings'),
  (33, 11, 'Kings'),
  (34, 12, 'DET'),
  (35, 12, 'Detroit Pistons'),
  (36, 12, 'Pistons'),
  (37, 13, 'NYK'),
  (38, 13, 'New York Knicks'),
  (39, 13, 'Knicks'),
  (40, 14, 'POR'),
  (41, 14, 'Portland Trail Blazers'),
  (42, 14, 'Trailblazers'),
  (43, 15, 'GSW'),
  (44, 15, 'Golden State Warriors'),
  (45, 15, 'Warriors'),
  (46, 16, 'DEN'),
  (47, 16, 'Denver Nuggets'),
  (48, 16, 'Nuggets'),
  (49, 17, 'ATL'),
  (50, 17, 'Atlanta Hawks'),
  (51, 17, 'Hawks'),
  (52, 18, 'CLE'),
  (53, 18, 'Cleveland Cavaliers'),
  (54, 18, 'Cavaliers'),
  (55, 19, 'NOP'),
  (56, 19, 'New Orleans Pelicans'),
  (57, 19, 'Pelicans'),
  (58, 20, 'CHA'),
  (59, 20, 'Charlotte Hornets'),
  (60, 20, 'Hornets'),
  (61, 21, 'LAC'),
  (62, 21, 'Los Angeles Clippers'),
  (63, 21, 'Clippers'),
  (64, 22, 'LAL'),
  (65, 22, 'Los Angeles Lakers'),
  (66, 22, 'Lakers'),
  (67, 23, 'PHX'),
  (68, 23, 'Phoenix Suns'),
  (69, 23, 'Suns'),
  (70, 24, 'MIN'),
  (71, 24, 'Minnesota Timberwolves'),
  (72, 24, 'Timberwolves'),
  (73, 25, 'BOS'),
  (74, 25, 'Boston Celtics'),
  (75, 25, 'Celtics'),
  (76, 26, 'HOU'),
  (77, 26, 'Houston Rockets'),
  (78, 26, 'Rockets'),
  (79, 27, 'CHI'),
  (80, 27, 'Chicago Bulls'),
  (81, 27, 'Bulls'),
  (82, 28, 'UTH'),
  (83, 28, 'Utah Jazz'),
  (84, 28, 'Jazz'),
  (85, 29, 'PHI'),
  (86, 29, 'Philadelphia 76ers'),
  (87, 29, '76ers'),
  (88, 30, 'MIL'),
  (89, 30, 'Milwaukee Bucks'),
  (90, 30, 'Bucks')
ON CONFLICT DO NOTHING;

INSERT INTO team_alias_by_vendor (team_alias_id, vendor_id) VALUES
  (1, 1),
  (2, 1),
  (3, 1),
  (4, 1),
  (5, 1),
  (6, 1),
  (7, 1),
  (8, 1),
  (9, 1),
  (10, 1),
  (11, 1),
  (12, 1),
  (13, 1),
  (14, 1),
  (15, 1),
  (16, 1),
  (17, 1),
  (18, 1),
  (19, 1),
  (20, 1),
  (21, 1),
  (22, 1),
  (23, 1),
  (24, 1),
  (25, 1),
  (26, 1),
  (27, 1),
  (28, 1),
  (29, 1),
  (30, 1),
  (31, 1),
  (32, 1),
  (33, 1),
  (34, 1),
  (35, 1),
  (36, 1),
  (37, 1),
  (38, 1),
  (39, 1),
  (40, 1),
  (41, 1),
  (42, 1),
  (43, 1),
  (44, 1),
  (45, 1),
  (46, 1),
  (47, 1),
  (48, 1),
  (49, 1),
  (50, 1),
  (51, 1),
  (52, 1),
  (53, 1),
  (54, 1),
  (55, 1),
  (56, 1),
  (57, 1),
  (58, 1),
  (59, 1),
  (60, 1),
  (61, 1),
  (62, 1),
  (63, 1),
  (64, 1),
  (65, 1),
  (66, 1),
  (67, 1),
  (68, 1),
  (69, 1),
  (70, 1),
  (71, 1),
  (72, 1),
  (73, 1),
  (74, 1),
  (75, 1),
  (76, 1),
  (77, 1),
  (78, 1),
  (79, 1),
  (80, 1),
  (81, 1),
  (82, 1),
  (83, 1),
  (84, 1),
  (85, 1),
  (86, 1),
  (87, 1),
  (88, 1),
  (89, 1),
  (90, 1)
ON CONFLICT DO NOTHING;
