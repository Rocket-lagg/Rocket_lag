from utils.singleton import Singleton
from dao.equipe_dao import EquipeDao
from dao.joueur_dao import JoueurDao
from dao.match_dao import MatchDao
from business_object.joueur import Joueur


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

        # Nous devons maintenant créer un objet Joueur avec les informations récupérées
        matchdao = MatchDao()
        id_matchs = matchdao.trouver_id_match_par_joueur(nom_joueur)
        n = len(id_matchs)

        # Ici on assume que l'objet `joueur_data` contient toutes les informations nécessaires pour créer un Joueur
        joueur = Joueur(
            match_id=joueur_data.match_id,
            equipe_nom=joueur_data.equipe,
            shots=joueur_data.shots,
            shots_par_match=joueur_data.shots_par_match,
            goals=joueur_data.goals,
            goals_par_match=joueur_data.goals_par_match,
            saves=joueur_data.saves,
            saves_par_match=joueur_data.saves_par_match,
            assists=joueur_data.assists,
            assists_par_match=joueur_data.assists_par_match,
            score=joueur_data.score,
            score_par_match=joueur_data.score_par_match,
            shooting_percentage=joueur_data.shooting_percentage,
            time_offensive_third=joueur_data.time_offensive_third,
            time_defensive_third=joueur_data.time_defensive_third,
            time_neutral_third=joueur_data.time_neutral_third,
            demo_inflige=joueur_data.demo_inflige,
            demo_inflige_par_match=joueur_data.demo_inflige_par_match,
            demo_recu=joueur_data.demo_recu,
            goal_participation=joueur_data.goal_participation,
            nom=joueur_data.nom,
            nationalite=joueur_data.nationalite,
            rating=joueur_data.rating,
            date=joueur_data.date,
            region=joueur_data.region,
            ligue=joueur_data.ligue,
            stage=joueur_data.stage,
            indice_offensif=joueur_data.indice_offensif,
            indice_performance=joueur_data.indice_performance,
        )

        # Calcul de l'indice régional selon la région
        region = joueur.region
        if region == "EU":
            regional_indice = 1
        elif region == "NA":
            regional_indice = 1
        elif region == "SAM":
            regional_indice = 0.9
        elif region == "MENA":
            regional_indice = 0.9
        elif region == "OCE":
            regional_indice = 0.5
        elif region == "APAC":
            regional_indice = 0.5
        elif region == "SSA":
            regional_indice = 0.3
        else:
            raise ValueError("La région du joueur est inconnue.")

        # Calcul des statistiques du joueur
        stats = Joueur(  # Ce `Joueur` est temporaire pour assigner les stats
            match_id=joueur.match_id,
            equipe_nom=joueur.equipe_nom,
            shots=joueur.shots,
            shots_par_match=joueur.shots_par_match,
            goals=joueur.goals,
            goals_par_match=joueur.goals_par_match,
            saves=joueur.saves,
            saves_par_match=joueur.saves_par_match,
            assists=joueur.assists,
            assists_par_match=joueur.assists_par_match,
            score=joueur.score,
            score_par_match=joueur.score_par_match,
            shooting_percentage=joueur.shooting_percentage,
            time_offensive_third=joueur.time_offensive_third,
            time_defensive_third=joueur.time_defensive_third,
            time_neutral_third=joueur.time_neutral_third,
            demo_inflige=joueur.demo_inflige,
            demo_inflige_par_match=joueur.demo_inflige_par_match,
            demo_recu=joueur.demo_recu,
            goal_participation=joueur.goal_participation,
            nom=joueur.nom,
            nationalite=joueur.nationalite,
            rating=joueur.rating,
            date=joueur.date,
            region=joueur.region,
            ligue=joueur.ligue,
            stage=joueur.stage,
            indice_offensif=joueur.indice_offensif,
            indice_performance=joueur.indice_performance,
        )

        stats.nom = joueur.nom
        stats.equipe_nom = joueur.equipe_nom
        stats.goals = joueur.goals
        stats.goals_par_match = stats.goals / n
        stats.assists = joueur.assists
        stats.assists_par_match = stats.assists / n
        stats.shots = joueur.shots
        stats.shots_par_match = stats.shots / n
        stats.saves = joueur.saves
        stats.saves_par_match = stats.saves / n
        stats.score = joueur.score
        stats.score_par_match = stats.score / n
        stats.shooting_percentage = joueur.shooting_percentage
        stats.demo_inflige = joueur.demo_inflige
        stats.demo_inflige_par_match = stats.demo_inflige / n
        stats.time_offensive_third = joueur.time_offensive_third
        stats.indice_offensif = round(
            (
                stats.goals / 1.05
                + stats.assists / 0.5
                + stats.shots / 3.29
                + stats.demo_inflige / 0.56
                + stats.time_offensive_third / 201.1
            )
            * (1 / n),
            2,
        )
        stats.indice_performance = round(
            (
                stats.goals * 1
                + stats.assists * 0.75
                + stats.saves * 0.6
                + stats.shots * 0.4
                + (stats.goals / stats.shots) * 0.5
            )
            * (1 / n)
            * regional_indice,
            2,
        )

        return stats

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
    nom_joueur = "Crispy"  # Remplacez par le nom du joueur que vous souhaitez
    consulter_stats.stats_joueurs(nom_joueur)  # Appel de la méthode
