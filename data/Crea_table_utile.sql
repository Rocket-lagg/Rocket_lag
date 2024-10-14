CREATE TABLE Equipe (
    match_id VARCHAR(255),
    equipe_nom VARCHAR(255),
    joueur_nom VARCHAR(255),
    region VARCHAR(255),
    equipe_winner INT,
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
    time_offensive_third FLOAT,
    ligue VARCHAR(255),
    stage VARCHAR(255)
);

CREATE TABLE Joueur (
    match_id VARCHAR(255),
    equipe_nom VARCHAR(255),
    joueur_nom VARCHAR(255),
    region VARCHAR(255),
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

CREATE TABLE matches (

);
