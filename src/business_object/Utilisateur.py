class Utilisateur:
    """
    Classe représentant un Utilisateur

    Attributs
    ----------
    nom_utilisateur : str
        Pseudo de l'utilisateur

    mot_de_passe : str
        Mot de passe de l'utilisateur

    email : str
        Email de l'utilisateur

    tournois_crées: list[Tournoi]
        Liste des tournois créés par l'utilisateur"

    paris: list[Pari]
        Liste des paris fait par l'utilisateur

    points: int
        Nombre de points de l'utilisateur (pour faire des paris)
    """

    def __init__(self, nom_utilisateur, mot_de_passe, email, tournois_crees, paris, points):
        """Constructeur"""
        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe
        self.email = email
        self.tournois_crees = tournois_crees
        self.paris = paris
        self.points = points

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"Joueur({self.nom_utilisateur}"
