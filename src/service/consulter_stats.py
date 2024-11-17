from utils.singleton import Singleton
from dao.equipe_dao import EquipeDao
from dao.joueur_dao import JoueurDao
from dao.match_dao import MatchDao
from business_object.joueur import Joueur
from business_object.equipe import Equipe


class ConsulterStats(metaclass=Singleton):
    """Une classe service qui affiche les statistiques par joueur, équipe et match"""

    @staticmethod
    def stats_par_match(total, n):
        """Calculer la moyenne par match tout en évitant la division par zéro"""
        return total / n if n > 0 else 0

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
        matchdao = MatchDao()
        id_matchs = matchdao.trouver_id_match_par_joueur(nom_joueur)
        n = len(id_matchs)

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
        }

        collonne = ["goals","assists","score","shots","shooting_percentage","demo_inflige","demo_recu","goal_participation","saves",
                     "indice_offensif","indice_performance","time_offensive_third","time_defensive_third","time_neutral_third"]
        stat_affiché = joueurdao.moyennes_statistiques(nom_joueur,collonne)

        print(
            f"Statistiques de {joueur_data.nom}, depuis le début de la saison :\n"
            f"Nombre moyen de buts marqués par match : {stat_affiché['goals']}\n"
            f"Nombre moyen de passes décisives par match : {stat_affiché['assists']}\n"
            f"Score moyen par match : {stat_affiché['score']}\n"
            f"Nombre moyen de tirs par match : {stat_affiché['shots']}\n"
            f"Pourcentage moyen des tirs effectués convertis en buts : {stat_affiché['shooting_percentage']}\n"
            f"Nombre moyen d'arrêts par match : {stat_affiché['saves']}\n"
            f"Performance moyenne : {stat_affiché['indice_performance']}\n"
            f"Participation aux buts au cours de la saison : {stat_affiché['goal_participation']}\n"
            f"Moyennes de démolitions infligées : {stat_affiché['demo_inflige']}\n"
            f"Moyennes de démolitions reçues par match : {stat_affiché['demo_recu']}\n"
            f"Apport offensif moyen : {stat_affiché['indice_offensif']}\n"
            f"Temps moyen passé en attaque : {stat_affiché['time_offensive_third']} secondes\n"
            f"Temps moyen passé en défense : {stat_affiché['time_defensive_third']} secondes"
        )



    # Note pour les vues : Les stats à afficher dans la vue sont : goals, goals par match, assists, assists par match,
    # saves, saves par match, shots, shots par match, score, score par match, demo infligées, demo infligées par match,
    # indice de performance, indice offensif, pourcentage de tirs

    def stats_equipe(self, nom_equipe):
        """Une fonction qui permet d'afficher les statistiques par équipe"""

        equipedao = EquipeDao()
        equipe_data = equipedao.obtenir_par_nom(nom_equipe)
        n = equipedao.nombre_match(nom_equipe)
        if n==0:
            raise ValueError(f"Aucun match n'a été trouvé pour l'équipe {nom_equipe}.")

        # indice de pression TODO -> besoin du nombre de boosts volés, du temps passé dans la partie de terrain adverse, et des démolitions

        collonne = ["goals","assists","score","shots","shooting_percentage","demo_inflige","demo_recu","saves",
                     "boost_stole","time_offensive_third","time_defensive_third","time_neutral_third","indice_de_pression","indice_performance"]

        stat_affiché = equipedao.moyennes_statistiques(nom_equipe,collonne)

        print(
                f"Statistiques de {nom_equipe}, depuis le début de la saison :\n"
                f"Nombre moyen de buts marqués par match : {stat_affiché['goals']}\n"
                f"Nombre moyen de passes décisives par match : {stat_affiché['assists']}\n"
                f"Score moyen par match : {stat_affiché['score']}\n"
                f"Nombre moyen de tirs par match : {stat_affiché['shots']}\n"
                f"Pourcentage moyen des tirs effectués convertis en buts : {stat_affiché['shooting_percentage']}\n"
                f"Nombre moyen d'arrêts par match : {stat_affiché['saves']}\n"
                f"Performance moyenne : {stat_affiché['indice_performance']}\n"
                f"Moyennes de démolitions infligées : {stat_affiché['demo_inflige']}\n"
                f"Moyennes de démolitions reçues par match : {stat_affiché['demo_recu']}\n"
                f"Temps moyen passé en attaque : {stat_affiché['time_offensive_third']} secondes\n"
                f"Temps moyen passé en défense : {stat_affiché['time_defensive_third']} secondes\n"
                f"Temps moyen passé en zone neutre : {stat_affiché['time_neutral_third']} secondes\n"
                f"Indice de pression moyen : {stat_affiché['indice_de_pression']}\n")


    def stats_matchs(self, nom_equipe="Non renseigné", nom_joueur="Non renseigné"):
        match_dao = MatchDao()
        if nom_equipe == "Non renseigné" and nom_joueur == "Non renseigné":
            raise ValueError("Il faut renseigner au moins un des deux arguments de la fonction.")
        id_matchs_equipe = None
        id_matchs_joueur = None
        if nom_equipe != "Non renseigné":
            id_matchs_equipe = match_dao.trouver_match_id_par_equipe(nom_equipe)
        if nom_joueur != "Non renseigné":
            id_matchs_joueur = match_dao.trouver_match_id_par_joueur(nom_joueur)
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
