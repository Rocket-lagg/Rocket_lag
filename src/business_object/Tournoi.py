class Tournoi:
    def __init__(
        self,
        nom_tournoi,
        createur,
        id_tournoi,
        tour,
        type_match,
        officiel=False,
        db_name="tournois.db",
    ):
        self.id_tournoi = id_tournoi
        self.nom_tournoi = nom_tournoi
        self.createur = createur
        self.tour = tour
        self.type_match = type_match
        self.equipes = []
        self.matchs = []
