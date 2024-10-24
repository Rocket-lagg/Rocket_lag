class Match:
    def __init__(self, id_match, equipe1, equipe2, score1, score2, date, ligue, region, perso, cote_match):       
        assert isinstance(id_match, int), "id_match doit être un entier"
        assert isinstance(equipe1, str) and equipe1, "equipe1 doit être une chaîne non vide"
        assert isinstance(equipe2, str) and equipe2, "equipe2 doit être une chaîne non vide"
        assert isinstance(score1, int) and score1 >= 0, "score1 doit être un entier positif"
        assert isinstance(score2, int) and score2 >= 0, "score2 doit être un entier positif"
        assert isinstance(date, str) and date, "date doit être une chaîne non vide" 
        assert isinstance(region, str) and region, "region doit être une chaîne non vide"
        assert isinstance(ligue, str) and ligue, "ligue doit être une chaîne non vide"
        assert isinstance(perso, str) and perso, "perso doit être une chaîne non vide"
        assert isinstance(cote_match, (int, float)) and cote_match > 0, "cote_match doit être un nombre positif"

        self.id_match = id_match
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.score1 = score1
        self.score2 = score2
        self.date = date
        self.region = region
        self.ligue = ligue
        self.perso = perso
        self.cote_match = cote_match
