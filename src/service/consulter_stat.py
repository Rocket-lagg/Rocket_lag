from src.utils.singleton import Singleton
from src.dao.equipe_dao import EquipeDao
from src.dao.joueur_dao import JoueurDao


class ConsulterStats(metaclass=Singleton):

    def stats_joueurs(self, nom_joueur):
        if not isinstance(nom_joueur, str):
            raise TypeError("nom_joueur doit être une instance de str")
