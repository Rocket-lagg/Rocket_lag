from utils.singleton import Singleton
from dao.equipe_dao import EquipeDao
from dao.joueur_dao import JoueurDao
from dao.match_dao import MatchDao
from business_object.joueur import Joueur
from business_object.Equipe import Equipe


class ConsulterStats(metaclass=Singleton):
    """Une classe service qui affiche les statistiques par joueur, équipe et match"""

    def stats_joueurs(self, nom_joueur):
        """Une fonction qui permet d'afficher les statistiques par joueur"""
        if not isinstance(nom_joueur, str):
            raise TypeError("nom_joueur doit être une instance de str")

        joueurdao = JoueurDao()
        joueur_data = joueurdao.obtenir_par_nom(nom_joueur)

        # Si aucun joueur n'est trouvé
        if not joueur_data:
            raise ValueError(f"Aucun joueur nommé {nom_joueur} n'a été trouvé.")

        # Récupérer le nombre de matchs
        n = joueurdao.nombre_match(nom_joueur)

        if n == 0:
            raise ValueError(f"Aucun match trouvé pour le joueur {nom_joueur}.")

        # Dictionnaire pour simplifier l'indice régional
        regional_indices = {
            "EU": 1,
            "NA": 1,
            "SAM": 0.9,
            "MENA": 0.9,
            "OCE": 0.5,
            "APAC": 0.5,
            "SSA": 0.3,
            "INT": 1,
        }
        regional_indice = regional_indices.get(joueur_data.region)
        if regional_indice is None:
            raise ValueError("La région du joueur est inconnue.")

        # Calcul des statistiques par match
        stats_par_match = lambda total: total / n if n > 0 else 0

        joueur_data.goals_par_match = stats_par_match(joueur_data.goals)
        joueur_data.assists_par_match = stats_par_match(joueur_data.assists)
        joueur_data.shots_par_match = stats_par_match(joueur_data.shots)
        joueur_data.saves_par_match = stats_par_match(joueur_data.saves)
        joueur_data.score_par_match = stats_par_match(joueur_data.score)
        joueur_data.demo_inflige_par_match = stats_par_match(joueur_data.demo_inflige)

        # Calcul des indices
        joueur_data.indice_offensif = round(
            (
                joueur_data.goals / 1.05
                + joueur_data.assists / 0.5
                + joueur_data.shots / 3.29
                + joueur_data.demo_inflige / 0.56
                + joueur_data.time_offensive_third / 201.1
            )
            * (1 / n),
            2,
        )

        joueur_data.indice_performance = round(
            (
                joueur_data.goals * 1
                + joueur_data.assists * 0.75
                + joueur_data.saves * 0.6
                + joueur_data.shots * 0.4
                + (joueur_data.goals / joueur_data.shots) * 0.5
                if joueur_data.shots > 0
                else 0
            )
            * (1 / n)
            * regional_indice,
            2,
        )

        return joueur_data

    def stats_equipe(self, nom_equipe):
        """Une fonction qui permet d'afficher les statistiques par équipe"""
        if not isinstance(nom_equipe, str):
            raise TypeError("'nom_equipe' doit être une instance de str")
        equipedao = EquipeDao()
        equipe_data = equipedao.obtenir_par_nom(nom_equipe)
        if not equipe_data:
            raise ValueError(f"Aucune equipe nommée {nom_equipe} n'a été trouvée.")
        matchdao = MatchDao()
        id_matchs = matchdao.trouver_match_id_par_equipe(nom_equipe)
        n = len(id_matchs)
        if n == 0:
            raise ValueError(f"Aucun match n'a été trouvé pour l'équipe {nom_equipe}.")

        def stats_par_match(total):
            return total / n if n > 0 else 0

        equipe_data.goals_par_match = stats_par_match(equipe_data.goals)
        equipe_data.assists_par_match = stats_par_match(equipe_data.assists)
        equipe_data.shots_par_match = stats_par_match(equipe_data.shots)
        equipe_data.score_par_match = stats_par_match(equipe_data.score)
        equipe_data.demo_inflige_par_match = stats_par_match(equipe_data.demo_inflige)

        equipe = Equipe(
            match_id=equipe_data.match_id,
            equipe_nom=equipe_data.equipe_nom,
            joueurs=equipe_data.joueurs,  # ajouter cet argumentà Equipe() et aux méthodes DAO
        )
        joueurs = equipe.joueurs
        goals = equipe.goals
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

    def stats_matchs(self, nom_equipe="Non renseigné", nom_joueur="Non renseigné"):
        if not isinstance(nom_equipe, str):
            raise TypeError("'nom_equipe' doit être une instance de str.")
        if not isinstance(nom_joueur, str):
            raise TypeError("'nom_joueur' doit être une instance de str.")
        if nom_equipe == "Non renseigné" and nom_joueur == "Non renseigné":
            raise ValueError("Il faut renseigner au moins un des deux arguments de la fonction.")
        id_matchs_equipe = None
        id_matchs_joueur = None
        if nom_equipe != "Non renseigné":
            id_matchs_equipe = MatchDao.trouver_match_id_par_equipe(nom_equipe)
        if nom_joueur != "Non renseigné":
            id_matchs_joueur = MatchDao.trouver_match_id_par_joueur(nom_joueur)
        if id_matchs_equipe is not None and id_matchs_joueur is not None:
            if id_matchs_equipe == id_matchs_joueur:
                id_matchs = id_matchs_equipe
            else:
                id_matchs = list(set(id_matchs_equipe + id_matchs_joueur))
        if id_matchs_equipe is None and id_matchs_joueur is None:
            raise TypeError("Aucun match ne correspond au joueur et/ou à l'équipe sélectionnés.")
        # a modifier, but = avoir une ou des fonctions dao qui permettent d'avoir les matchs joués par une éuqipe ou par un joueur

        # besoin du résultat du match, des buts, des assists, des arrêts, des ratings, des pourcentages de tirs, du temps passé dans le tiers offensif et des démolitions par équipe et par joueur
        # aussi besoin des boosts volés par équipe


if __name__ == "__main__":
    consulter_stats = ConsulterStats()  # Création d'une instance de ConsulterStats
    nom_joueur = "itachi"  # Remplacez par le nom du joueur que vous souhaitez
    consulter_stats.stats_joueurs(nom_joueur)  # Appel de la méthode
