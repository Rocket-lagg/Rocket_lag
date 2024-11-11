from business_object.Pari import Pari
from business_object.Tournoi import Tournoi


class Utilisateur:
    """
    Classe représentant un Utilisateur

    Attributs
    ----------
    pseudo : str
        Pseudo de l'utilisateur

    mdp : str
        Mot de passe de l'utilisateur

    mail : str
        mail de l'utilisateur

    tournois_crées: list[Tournoi]
        Liste des tournois créés par l'utilisateur"

    paris: list[Pari]
        Liste des paris fait par l'utilisateur

    points: int
        Nombre de points de l'utilisateur (pour faire des paris)
    """

    def __init__(
        self, pseudo, mail, tournois_crees=[], paris=[], points=10, id_utilisateur=None, mdp=None
    ):
        """Constructeur"""
        if not isinstance(pseudo, str):
            raise TypeError("pseudo doit être de type str")
        if not isinstance(tournois_crees, list):
            raise TypeError("tournois_crees doit être de type list")
        if not isinstance(paris, list):
        if not isinstance(paris, list(Pari)):
            raise TypeError("paris doit être de type Pari")
        if not isinstance(points, int):
            raise TypeError("points doit être de type int")

        self.id_utilisateur = id_utilisateur
        self.pseudo = pseudo
        self.mdp = mdp
        self.mail = mail
        self.tournois_crees = tournois_crees
        self.paris = paris  # regarder pour prendre les logs
        self.points = points

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        tournois_str = ", ".join([tournoi.nom_tournoi for tournoi in self.tournois_crees])
        paris_str = ", ".join([f"{pari.id_pari}" for pari in self.paris])
        return (
            f"identifiant:{self.nom_utilisateur}, "
            f"mdp:{self.mot_de_passe}, "
            f"email:{self.email}, "
            f"tournois:[{tournois_str}], "
            f"paris:[{paris_str}], "
            f"points:{self.points}"
        )
        return f"identifiant:{self.pseudo}, mdp:{self.mdp}, mail:{self.mail}"
        f"tournois:{self.tournois_crees}, paris:{self.paris}, points:{self.points})"
