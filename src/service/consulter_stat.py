from src.utils.singleton import Singleton
from src.dao.equipe_dao import EquipeDao
from src.dao.joueur_dao import JoueurDao
from src.dao.match_dao import MatchDao
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
        id_matchs = MatchDao.trouver_id_match_par_joueur(nom_joueur)
        n = len(id_matchs)
        # créer un indice régional TODO
        region = joueur.region
        equipe = joueur.equipe
        goals = joueur.goals
        # résultat TODO -> donner le nombre de défaites et de victoires au cours de l'année
        assists = joueur.assists
        shots = joueur.shots
        saves = joueur.saves
        rating = joueur.score
        shooting_percentage = joueur.shooting_percentage
        demolitions = joueur.demo_inflige
        # indice offensif TODO -> besoin de la goal participation, du nombre de buts marqués, du temps passé dans le tiers offensif et du nombre de démolitions
        # indice de performance TODO -> besoin du nombre de buts, du nombre d'assists, du nombre de saves, du nombre de tirs, du nombre de matchs joués
        print(
            f"Statistiques pour le joueur {nom_joueur}, membre de l'équipe "
            f"{equipe}, depuis le début de la saison :\n"
            f"Total de buts : {goals}\n"
            f"Nombre moyen de buts par matchs : {goals/n}\n"
            f"Total de passes décisives : {assists}\n"
            f"Nombre de passes décisives moyen par match : {assists/n}\n"
            f"Total de tirs : {shots}\n"
            f"Nombre moyen de tirs par match : {shots/n}\n"
            f"Total d'arrêts : {saves}\n"
            f"Nombre moyen d'arrêts par match : {saves/n}\n"
            f"Rating moyen par match : {rating/n}\n"
            f"Pourcentage de tirs cadrés moyen par match : {shooting_percentage/n}\n"
            f"Total de démolitions infligées : {demolitions}\n"
            f"Nombre moyen de démolitions infligées par match : {demolitions/n}"
        )

    def stats_equipe(self, nom_equipe):
        if not isinstance(str, nom_equipe):
            raise TypeError("'nom_equipe' doit être une instance de str")
        equipe = EquipeDao.obtenir_par_nom(nom_equipe)
        if not equipe:
            raise ValueError(f"Aucune equipe nommée {nom_equipe} n'a été trouvée.")
        id_matchs = MatchDao.trouver_id_match_par_equipe(nom_equipe)
        joueurs = equipe.joueurs
        n = len(id_matchs)
        goals = equipe.goals
        # résultats TODO
        assists = equipe.assists
        shots = equipe.shots
        saves = equipe.saves
        rating = equipe.score
        shot_percentage = equipe.shot_percentage
        demolitions = equipe.demo_inflige
        # indice de pression TODO -> besoin du nombre de boosts volés, du temps passé dans la partie de terrain adverse, et des démolitions
        print(
            f"Statistiques de l'équipe {nom_equipe}, constituée de {joueurs}, "
            f"depuis le début de la saison :\n"
            f"Total des buts marqués : {goals}\n"
            f"Nombre moyen de buts marqués par match : {goals/n}\n"
            f"Total des passes décisives : {assists}\n"
            f"Nombre moyen de passes décisives par match : {assists/n}\n"
            f"Total des tirs : {shots}\n"
            f"Nombre moyen de tirs par match : {shots/n}\n"
            f"Total d'arrêts : {saves}\n"
            f"Nombre moyen d'arrêts par match : {saves/n}\n"
            f"Rating moyen au cours de la saison : {rating/n}\n"
            f"Pourcentage de tirs cadrés au cours de la saison : {shot_percentage/n}\n"
            f"Total des démolitions infligées : {demolitions}\n"
            f"Nombre moyen de démolitions infligées par match : {demolitions/n}"
        )

    def stats_matchs(self, nom_equipe="Non fourni", nom_joueur="Non fourni"):
        if not isinstance(nom_equipe, str):
            raise TypeError("'nom_equipe' doit être une instance de str.")
        if not isinstance(nom_joueur, str):
            raise TypeError("'nom_joueur' doit être une instance de str.")
        if nom_equipe == "Non fourni" and nom_joueur == "Non fourni":
            raise ValueError("Il faut renseigner au moins un des deux arguments de la fonction.")
        match = MatchDao.trouverparequipejoueur(
            nom_equipe, nom_joueur
        )  # a modifier, but = avoir une ou des fonctions dao qui permettent d'avoir les matchs joués par une éuqipe ou par un joueur
        if not match:
            raise TypeError("Aucun match ne correspond au joueur et/ou à l'équipe sélectionnés.")
        # besoin du résultat du match, des buts, des assists, des arrêts, des ratings, des pourcentages de tirs, du temps passé dans le tiers offensif et des démolitions par équipe et par joueur
        # aussi besoin des boosts volés par équipe
