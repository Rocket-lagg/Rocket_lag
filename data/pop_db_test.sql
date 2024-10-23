INSERT INTO utilisateur(id_utilisateur, pseudo, mdp, age, mail, fan_pokemon) VALUES
(999, 'admin',      '0000',     0,       'admin@projet.fr',      null),
(998, 'a',             'a',     20,      'a@ensai.fr',           true),
(997, 'maurice',    '1234',     20,      'maurice@ensai.fr',     true),
(996, 'batricia',   '9876',     25,      'bat@projet.fr',        false),
(995, 'miguel',     'abcd',     23,      'miguel@projet.fr',     true),
(994, 'gilbert',    'toto',     21,      'gilbert@projet.fr',    false),
(993, 'junior',     'aaaa',     15,      'junior@projet.fr',     true);



INSERT INTO match(match_id, equipe1, equipe2, score1, score2, date, region, ligue, perso) VALUES
('admin1','0000','001',1, 2, 2024-10-08T22:00:00Z, 'FRance', 'ligue1', false),
('admin2','0200','001',1, 2, 2024-10-08T22:00:00Z, 'FRance', 'ligue1', false),
('admin3','0300','001',1, 2, 2024-12-08T22:00:00Z, 'FRance', 'ligue1', false);
