class Tournoi:
    """
    Représente un tournoi avec ses informations associées.

    Attributs
    ---------
    id_tournoi : int
        Identifiant unique du tournoi.
    nom_tournoi : str
        Nom du tournoi.
    createur : str
        Nom ou identifiant du créateur du tournoi.
    tour : str
        Tour ou phase actuelle du tournoi (par exemple : "quart de finale").
    type_match : str
        Type de match dans le tournoi (par exemple : "simple", "double").
    equipes : list
        Liste des équipes participant au tournoi (initialement vide).
    matchs : list
        Liste des matchs du tournoi (initialement vide).
    """
    def __init__(
        self,
        nom_tournoi,
        createur,
        id_tournoi,
        tour,
        type_match,

    ):
        self.id_tournoi = id_tournoi
        self.nom_tournoi = nom_tournoi
        self.createur = createur
        self.tour = tour
        self.type_match = type_match
        self.equipes = []
        self.matchs = []
