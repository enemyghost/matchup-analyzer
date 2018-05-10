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

-- Sport names for Vegas Insider
INSERT INTO sport_alias_by_vendor (vendor_id, sport_id, sport_alias) VALUES
  (1, 1, 'nfl'),
  (1, 2, 'nba'),
  (1, 3, 'college-basketball'),
  (1, 4, 'college-football'),
  (1, 5, 'mlb'),
  (1, 6, 'nhl')
ON CONFLICT DO NOTHING;

--NBA team alias for Vegas Insider--
INSERT INTO team_alias_by_vendor (team_symbol, team_name, team_name_full, sport_id, vendor_id) VALUES
('PHI', '76ers', 'Philadelphia 76ers', 2, 1),
('MIL', 'Bucks', 'Milwaukee Bucks', 2, 1),
('CHI', 'Bulls', 'Chicago Bulls', 2, 1),
('CLE', 'Cavaliers', 'Cleveland Cavaliers', 2, 1),
('BOS', 'Celtics', 'Boston Celtics', 2, 1),
('LAC', 'Clippers', 'LA Clippers', 2, 1),
('MEM', 'Grizzlies', 'Memphis Grizzlies', 2, 1),
('ATL', 'Hawks', 'Atlanta Hawks', 2, 1),
('MIA', 'Heat', 'Miami Heat', 2, 1),
('CHA', 'Hornets', 'Charlotte Hornets', 2, 1),
('UTH', 'Jazz', 'Utah Jazz', 2, 1),
('SAC',	'Kings', 'Sacramento Kings', 2, 1),
('NYK', 'Knicks', 'New York Knicks', 2, 1),
('LAL',	'Lakers', 'Los Angeles Lakers', 2, 1),
('ORL',	'Magic', 'Orlando Magic', 2, 1),
('DAL',	'Mavericks', 'Dallas Mavericks', 2, 1),
('BKN', 'Nets', 'Brooklyn Nets', 2, 1),
('DEN', 'Nuggets', 'Denver Nugets', 2, 1),
('IND', 'Pacers', 'Indiana Pacers', 2, 1),
('NOP', 'Pelicans', 'New Orleans Pelicans', 2, 1),
('DET', 'Pistons', 'Detroit Pistons', 2, 1),
('TOR', 'Raptors', 'Toronto Raptors', 2, 1),
('HOU', 'Rockets', 'Houston Rockets', 2, 1),
('SAS', 'Spurs', 'San Antonio Spurs', 2, 1),
('PHX', 'Suns', 'Phoenix Suns', 2, 1),
('OKL', 'Thunder', 'Oklahoma City Thunder', 2, 1),
('MIN', 'Timberwolves', 'Minnesota Timberwolves', 2, 1),
('POR', 'Trailblazers', 'Portland Trail Blazers', 2, 1),
('GSW', 'Warriors', 'Golden State Warriors', 2, 1),
('WAS', 'Wizards', 'Washington Wizards', 2, 1)
ON CONFLICT DO NOTHING;
