from src.utils.singleton import Singleton
from src.dao.equipe_dao import EquipeDao
from src.dao.joueur_dao import JoueurDao
from src.business_object.joueur import Joueur


class ConsulterStats(metaclass=Singleton):
    """Une classe service qui affiche les statistiques par joueur, équipe et match"""

    def stats_joueurs(self, nom_joueur):
        """Une fonction qui permet d'afficher les statistiques par joueur"""
        if not isinstance(nom_joueur, str):
            raise TypeError("nom_joueur doit être une instance de str")
        joueur = JoueurDao(nom_joueur)
        if not joueur:
            raise ValueError("'nom_joueur' ne correspond à aucun joueur de la base de données")
