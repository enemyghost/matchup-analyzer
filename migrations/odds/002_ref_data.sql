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
