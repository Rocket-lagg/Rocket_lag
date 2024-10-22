from src.utils.singleton import Singleton
from src.dao.equipe_dao import EquipeDao
from src.dao.joueur_dao import JoueurDao
from sklearn.preprocessing import StandardScaler
from src.business_object.joueur import Joueur


class ConsulterStats(metaclass=Singleton):
    """Une classe service qui affiche les statistiques par joueur, équipe et match"""

    def stats_joueurs(self, nom_joueur):
        """Une fonction qui permet d'afficher les statistiques par joueur"""
        if not isinstance(nom_joueur, str):
            raise TypeError("nom_joueur doit être une instance de str")
        joueur = JoueurDao.obtenir_par_nom(nom_joueur)
        if not joueur:
            raise ValueError(f"Aucun joueur nommé {nom_joueur} n'a été trouvé.")
        goals = joueur.goals
        # résultat TODO
        assists = joueur.assists
        shots = joueur.shots
        saves = joueur.saves
        rating = joueur.score
        shooting_percentage = joueur.shooting_percentage
        demolitions = joueur.demo_inflige
        # indice offensif TODO
        # indice de performance TODO
        print(
            f"Statistiques pour le joueur {nom_joueur} depuis le début de la saison :\n"
            f"Buts : {goals}\n"
            f"Passes décisives : {assists}\n"
            f"Tirs : {shots}\n"
            f"Arrêts : {saves}\n"
            f"Rating : {rating}\n"
            f"Pourcentage de tirs cadrés : {shooting_percentage}\n"
            f"Démolitions : {demolitions}"
        )

    def stats_equipe(self, nom_equipe):
        if not isinstance(str, nom_equipe):
            raise TypeError("'nom_equipe' doit être une instance de str")
        equipe = EquipeDao.obtenir_par_nom(nom_equipe)
        if not equipe:
            raise ValueError(f"Aucune equipe nommée {nom_equipe} n'a été trouvée.")
        goals = equipe.goals
        # résultats TODO
        assists = equipe.assists
        shots = equipe.shots
        saves = equipe.saves
        rating = equipe.score
        shot_percentage = equipe.shot_percentage
        demolitions = equipe.demo_inflige
        # indice de pression TODO
        print(
            f"Statistiques de l'équipe {nom_equipe} depuis le début de la saison :\n"
            f"Nombre de buts marqués : {goals}\n"
            f"Nombre de passes décisives : {assists}\n"
            f"Nombre de tirs : {shots}\n"
            f"Nombre d'arrêts : {saves}\n"
            f"Rating moyen au cours de la saison : {rating}\n"
            f"Pourcentage de tirs cadrés au cours de la saison : {shot_percentage}\n"
            f"Nombre de démolitions depuis le début de la saison : {demolitions}"
        )

    def stats_matchs(self, nom_equipe="Non fourni", nom_joueur="Non fourni"):
        if not isinstance(nom_equipe, str):
            raise TypeError("'nom_equipe' doit être une instance de str.")
        if not isinstance(nom_joueur, str):
            raise TypeError("'nom_joueur' doit être une instance de str.")
        if nom_equipe == "Non fourni" and nom_joueur == "Non fourni":
            raise ValueError("Il faut renseigner au moins un des deux arguments de la fonction.")
