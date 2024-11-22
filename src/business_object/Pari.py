
class Pari:
    def __init__(self, id_match, tournoi, equipe1, equipe2, cote_equipe1, cote_equipe2, date):
        self.id_match = id_match
        self.tournoi = tournoi
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.cote_equipe1 = cote_equipe1
        self.cote_equipe2 = cote_equipe2
        self.date = date

    def __str__(self):
        return (f"Pari(id_match={self.id_match}, tournoi={self.tournoi}, "
                f"equipe1={self.equipe1}, equipe2={self.equipe2}, "
                f"cote_equipe1={self.cote_equipe1}, cote_equipe2={self.cote_equipe2}, date={self.date})")
