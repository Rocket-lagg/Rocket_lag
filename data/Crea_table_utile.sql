CREATE TABLE matches (
    match_id VARCHAR(255),
    equipe_nom VARCHAR(255),
    equipe_image VARCHAR(255),
    equipe_score INT,
    equipe_winner BOOLEAN,
    shots INT,
    goals INT,
    saves INT,
    assists INT,
    score INT,
    shooting_percentage FLOAT,
    date TIMESTAMP,
    ligue VARCHAR(255),
    region VARCHAR(50),
    stage VARCHAR(50)
);

CREATE TABLE players (
    match_id VARCHAR(255),
    equipe_nom VARCHAR(255),
    joueur_nom VARCHAR(255),
    nationalite VARCHAR(50),
    shots INT,
    goals INT,
    saves INT,
    assists INT,
    score INT,
    shooting_percentage FLOAT,
    demo_infligées INT,
    demo_reçues INT,
    goal_participation FLOAT,
    rating FLOAT,
    time_defensive_third FLOAT,
    time_neutral_third FLOAT,
    time_offensive_third FLOAT
);
