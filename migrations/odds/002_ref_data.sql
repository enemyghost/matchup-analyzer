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

INSERT INTO team (team_symbol, team_name, team_name_full, sport_id) VALUES
('PHI', '76ers', 'Philadelphia 76ers', 2),
('MIL', 'Bucks', 'Milwaukee Bucks', 2),
('CHI', 'Bulls', 'Chicago Bulls', 2),
('CLE', 'Cavaliers', 'Cleveland Cavaliers', 2),
('BOS', 'Celtics', 'Boston Celtics', 2),
('LAC', 'Clippers', 'LA Clippers', 2),
('MEM', 'Grizzlies', 'Memphis Grizzlies', 2),
('ATL', 'Hawks', 'Atlanta Hawks', 2),
('MIA', 'Heat', 'Miami Heat', 2),
('CHA', 'Hornets', 'Charlotte Hornets', 2),
('UTA', 'Jazz', 'Utah Jazz', 2),
('UTH', 'Jazz', 'Utah Jazz', 2),
('SAC',	'Kings', 'Sacramento Kings', 2),
('NYK', 'Knicks', 'New York Knicks', 2),
('LAL',	'Lakers', 'Los Angeles Lakers', 2),
('ORL',	'Magic', 'Orlando Magic', 2),
('DAL',	'Mavericks', 'Dallas Mavericks', 2),
('BKN', 'Nets', 'Brooklyn Nets', 2),
('DEN', 'Nuggets', 'Denver Nugets', 2),
('IND', 'Pacers', 'Indiana Pacers', 2),
('NOP', 'Pelicans', 'New Orleans Pelicans', 2),
('DET', 'Pistons', 'Detroit Pistons', 2),
('TOR', 'Raptors', 'Toronto Raptors', 2),
('HOU', 'Rockets', 'Houston Rockets', 2),
('SAS', 'Spurs', 'San Antonio Spurs', 2),
('PHX', 'Suns', 'Phoenix Suns', 2),
('OKC', 'Thunder', 'Oklahoma City Thunder', 2),
('OKL', 'Thunder', 'Oklahoma City Thunder', 2),
('MIN', 'Timberwolves', 'Minnesota Timberwolves', 2),
('POR', 'Trailblazers', 'Portland Trail Blazers', 2),
('GSW', 'Warriors', 'Golden State Warriors', 2),
('WAS', 'Wizards', 'Washington Wizards', 2)
ON CONFLICT DO NOTHING;
