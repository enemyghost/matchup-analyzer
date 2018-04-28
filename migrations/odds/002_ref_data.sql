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

INSERT INTO team_alias_by_sport (team_abbr, team_name, sport_id) VALUES
('PHI', '76ers', 2),
('MIL', 'Bucks', 2),
('CHI', 'Bulls', 2),
('CLE', 'Cavaliers', 2),
('BOS', 'Celtics', 2),
('LAC', 'Clippers', 2),
('MEM', 'Grizzlies', 2),
('ATL', 'Hawks', 2),
('MIA', 'Heat', 2),
('CHA', 'Hornets', 2),
('UTA', 'Jazz', 2),
('SAC',	'Kings', 2),
('NYK', 'Knicks', 2),
('LAL',	'Lakers', 2),
('ORL',	'Magic', 2),
('DAL',	'Mavericks', 2),
('BKN', 'Nets', 2),
('DEN', 'Nuggets', 2),
('IND', 'Pacers', 2),
('NOP', 'Pelicans', 2),
('DET', 'Pistons', 2),
('TOR', 'Raptors', 2),
('HOU', 'Rockets', 2),
('SAS', 'Spurs', 2),
('PHX', 'Suns', 2),
('OKC', 'Thunder', 2),
('MIN', 'Timberwolves', 2),
('POR', 'Trailblazers', 2),
('GSW', 'Warriors', 2)
('WAS', 'Wizards', 2)
ON CONFLICT DO NOTHING;
