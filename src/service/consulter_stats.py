from utils.singleton import Singleton
from dao.equipe_dao import EquipeDao
from dao.joueur_dao import JoueurDao
from dao.match_dao import MatchDao
from business_object.joueur import Joueur
from business_object.Equipe import Equipe


class ConsulterStats(metaclass=Singleton):
    """Une classe service qui affiche les statistiques par joueur, équipe et match"""

    @staticmethod
    def stats_par_match(total, n):
        """
        Calculer la moyenne par match tout en évitant la division par zéro.

        Parameters
        ----------
        total : int or float
            Le total des scores ou autres statistiques à diviser par le nombre de matchs.
        n : int
            Le nombre de matchs sur lequel calculer la moyenne.

        Return
        ------
        float
            La moyenne calculée.
        """
        return total / n if n > 0 else 0

    def stats_joueurs(self, nom_joueur):
        """Une fonction qui permet d'afficher les statistiques par joueur

        Parameters
        ----------
        nom_joueur : str
            Nom du joueur dont on recherche les statistiques

        Return
        ------
        None
            La fonction affiche directement les statistiques de l'équipe dans la console.

        """
        if not isinstance(nom_joueur, str):
            raise TypeError("nom_joueur doit être une instance de str")

        joueurdao = JoueurDao()
        joueur_data = joueurdao.obtenir_par_nom(nom_joueur)

        # Si aucun joueur n'est trouvé
        if not joueur_data:
            raise ValueError(f"Aucun joueur nommé {nom_joueur} n'a été trouvé.")

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
        }

        collonne = [
            "goals",
            "assists",
            "score",
            "shots",
            "shooting_percentage",
            "demo_inflige",
            "demo_recu",
            "goal_participation",
            "saves",
            "indice_offensif",
            "indice_performance",
            "time_offensive_third",
            "time_defensive_third",
            "time_neutral_third",
        ]
        stat_affiché = joueurdao.moyennes_statistiques(nom_joueur, collonne)

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

    def stats_equipe(self, nom_equipe):
        """
        Une fonction qui permet d'afficher les statistiques par équipe.

        Parameters
        ----------
        nom_equipe : str
            Le nom de l'équipe pour laquelle afficher les statistiques.

        Return
        ------
        None
            La fonction affiche directement les statistiques de l'équipe dans la console.
        """

        equipedao = EquipeDao()
        equipe_data = equipedao.obtenir_par_nom(nom_equipe)
        n = equipedao.nombre_match(nom_equipe)
        if n == 0:
            raise ValueError(f"Aucun match n'a été trouvé pour l'équipe {nom_equipe}.")

        collonne = [
            "goals",
            "assists",
            "score",
            "shots",
            "shooting_percentage",
            "demo_inflige",
            "demo_recu",
            "saves",
            "boost_stole",
            "time_offensive_third",
            "time_defensive_third",
            "time_neutral_third",
            "indice_de_pression",
            "indice_performance",
        ]

        stat_affiché = equipedao.moyennes_statistiques(nom_equipe, collonne)

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
            f"Indice de pression moyen : {stat_affiché['indice_de_pression']}\n"
        )

    def choix_match_joueur(self, nom_joueur):
        """
        Récupère les matchs associés à un joueur et retourne un dictionnaire de matchs.

        Parameters
        ----------
        nom_joueur : str
            Le nom du joueur pour lequel récupérer les matchs.

        Return
        ------
        dict
            Un dictionnaire où les clés sont des chaînes de caractères représentant les matchs sous la forme
        """

        if not isinstance(nom_joueur, str):
            raise TypeError("'nom_joueur' doit être une instance de str.")

        matchdao = MatchDao()
        liste = matchdao.trouver_match_id_par_joueur(nom_joueur)

        # Transformer la liste d'objets Match en un dictionnaire avec la forme souhaitée
        match_dict = {}

        for match in liste:
            # Créer la clé sous la forme 'equipe1 vs equipe2 - Stage: stage, Date: date'
            match_key = (
                f"{match.equipe1} vs {match.equipe2} - Stage: {match.stage}, Date: {match.date}"
            )

            # Ajouter l'ID du match dans une liste, si la clé existe déjà, ajoutez l'ID à la liste
            if match_key in match_dict:
                match_dict[match_key].append(match.match_id)
            else:
                match_dict[match_key] = [match.match_id]

        return match_dict

    def choix_match_equipe(self, nom_equipe):
        """
        Récupère les matchs associés à une équipe et retourne un dictionnaire de matchs.

        Parameters
        ----------
        nom_equipe : str
            Le nom de l'équipe pour laquelle récupérer les matchs.

        Return
        ------
        dict
            Un dictionnaire où les clés sont des chaînes de caractères représentant les matchs sous la forme

        """
        if not isinstance(nom_equipe, str):
            raise TypeError("'nom_equipe' doit être une instance de str.")

        matchdao = MatchDao()
        liste = matchdao.trouver_match_id_par_equipe(nom_equipe)

        # Transformer la liste d'objets Match en un dictionnaire avec la forme souhaitée
        match_dict = {}

        for match in liste:
            # Créer la clé sous la forme 'equipe1 vs equipe2 - Stage: stage, Date: date'
            match_key = (
                f"{match.equipe1} vs {match.equipe2} - Stage: {match.stage}, Date: {match.date}"
            )

            # Ajouter l'ID du match dans une liste, si la clé existe déjà, ajoutez l'ID à la liste
            if match_key in match_dict:
                match_dict[match_key].append(match.match_id)
            else:
                match_dict[match_key] = [match.match_id]

        return match_dict

    def stats_completes_match(self, match_id):
        """
        Renvoie toutes les statistiques pour les deux équipes d'un match donné, avec calcul des stats des équipes et des joueurs.

        Parameters
        ----------
        match_id : str
            L'ID unique du match pour lequel les statistiques doivent être récupérées.

        Return
        ------
        dict
            Un dictionnaire contenant toutes les informations sur le match et les statistiques détaillées des joueurs et des équipes.
        """
        if not isinstance(match_id, str):
            raise TypeError("L'ID du match doit être une chaîne de caractères.")

        joueurdao = JoueurDao()
        matchdao = MatchDao()

        # Utiliser la méthode trouver_match_id_et_equipe à la place
        match_data = matchdao.trouver_match_id_et_equipe("Complexity Gaming", match_id)

        if not match_data:
            raise ValueError(f"Aucun détail trouvé pour le match avec l'ID {match_id}.")

        # Préparer les informations du match en utilisant les clés du dictionnaire
        stats_match = {
            "match_id": match_data["match_id"],
            "equipe1": match_data["equipe1"],
            "equipe2": match_data["equipe2"],
            "score1": match_data["score1"],
            "score2": match_data["score2"],
            "date": match_data["date"],
            "stage": match_data["stage"],
            "region": match_data["region"],
            "ligue": match_data["ligue"],
        }

        # Récupérer les joueurs par équipe
        joueurs_par_equipe = joueurdao.obtenir_par_match(match_id)

        if not joueurs_par_equipe:
            raise ValueError(f"Aucun joueur trouvé pour le match avec l'ID {match_id}.")

        # Transformation : Regrouper les joueurs par équipe
        joueurs_par_equipe_dict = {}
        for joueur in joueurs_par_equipe:
            equipe_nom = joueur["equipe_nom"]
            if equipe_nom not in joueurs_par_equipe_dict:
                joueurs_par_equipe_dict[equipe_nom] = []
            joueurs_par_equipe_dict[equipe_nom].append(joueur)

        # Ajouter les joueurs dans chaque équipe avec leurs statistiques
        stats_match["joueurs"] = {}
        equipe1_stats = {
            "score": 0,
            "boost_stole": 0,
            "total_time_offensive": 0,
            "total_time_defensive": 0,
            "total_time_neutral": 0,
            "total_demos_infliges": 0,
            "total_demos_recus": 0,
        }

        equipe2_stats = {
            "score": 0,
            "boost_stole": 0,
            "total_time_offensive": 0,
            "total_time_defensive": 0,
            "total_time_neutral": 0,
            "total_demos_infliges": 0,
            "total_demos_recus": 0,
        }

        # Ajouter les joueurs et calculer les stats des équipes
        for equipe, joueurs in joueurs_par_equipe_dict.items():
            stats_match["joueurs"][equipe] = []
            for joueur in joueurs:
                joueur_stats = matchdao.trouver_match_id_et_joueur(joueur["nom"], match_id)
                if joueur_stats:
                    joueur_detail = {
                        "nom": joueur_stats.get("nom"),
                        "nationalite": joueur_stats.get("nationalite"),
                        "goals": joueur_stats.get("goals"),
                        "assists": joueur_stats.get("assists"),
                        "saves": joueur_stats.get("saves"),
                        "shots": joueur_stats.get("shots"),
                        "score": joueur_stats.get("score"),
                        "shooting_percentage": joueur_stats.get("shooting_percentage"),
                        "time_offensive_third": joueur_stats.get("time_offensive_third"),
                        "time_defensive_third": joueur_stats.get("time_defensive_third"),
                        "time_neutral_third": joueur_stats.get("time_neutral_third"),
                        "demo_inflige": joueur_stats.get("demo_inflige"),
                        "demo_recu": joueur_stats.get("demo_recu"),
                        "goal_participation": joueur_stats.get("goal_participation"),
                        "indice_offensif": joueur_stats.get("indice_offensif"),
                        "indice_performance": joueur_stats.get("indice_performance"),
                    }
                    stats_match["joueurs"][equipe].append(joueur_detail)

                    # Calcul des stats agrégées pour chaque équipe
                    if equipe == match_data["equipe1"]:
                        equipe1_stats["score"] += joueur_stats.get("score", 0)
                        equipe1_stats["boost_stole"] += joueur_stats.get("boost_stole", 0)
                        equipe1_stats["total_time_offensive"] += joueur_stats.get(
                            "time_offensive_third", 0
                        )
                        equipe1_stats["total_time_defensive"] += joueur_stats.get(
                            "time_defensive_third", 0
                        )
                        equipe1_stats["total_time_neutral"] += joueur_stats.get(
                            "time_neutral_third", 0
                        )
                        equipe1_stats["total_demos_infliges"] += joueur_stats.get("demo_inflige", 0)
                        equipe1_stats["total_demos_recus"] += joueur_stats.get("demo_recu", 0)

                    elif equipe == match_data["equipe2"]:
                        equipe2_stats["score"] += joueur_stats.get("score", 0)
                        equipe2_stats["boost_stole"] += joueur_stats.get("boost_stole", 0)
                        equipe2_stats["total_time_offensive"] += joueur_stats.get(
                            "time_offensive_third", 0
                        )
                        equipe2_stats["total_time_defensive"] += joueur_stats.get(
                            "time_defensive_third", 0
                        )
                        equipe2_stats["total_time_neutral"] += joueur_stats.get(
                            "time_neutral_third", 0
                        )
                        equipe2_stats["total_demos_infliges"] += joueur_stats.get("demo_inflige", 0)
                        equipe2_stats["total_demos_recus"] += joueur_stats.get("demo_recu", 0)

        # Ajouter les statistiques agrégées pour les équipes
        stats_match["equipe1_stats"] = {
            "score": equipe1_stats["score"],
            "boost_stole": match_data.get("boost_stole", equipe1_stats["boost_stole"]),
            "total_time_offensive": match_data.get(
                "total_time_offensive", equipe1_stats["total_time_offensive"]
            ),
            "total_time_defensive": match_data.get(
                "total_time_defensive", equipe1_stats["total_time_defensive"]
            ),
            "total_time_neutral": match_data.get(
                "total_time_neutral", equipe1_stats["total_time_neutral"]
            ),
            "total_demos_infliges": match_data.get(
                "total_demos_infliges", equipe1_stats["total_demos_infliges"]
            ),
            "total_demos_recus": match_data.get(
                "total_demos_recus", equipe1_stats["total_demos_recus"]
            ),
        }

        stats_match["equipe2_stats"] = {
            "score": equipe2_stats["score"],
            "boost_stole": match_data.get("boost_stole", equipe2_stats["boost_stole"]),
            "total_time_offensive": match_data.get(
                "total_time_offensive", equipe2_stats["total_time_offensive"]
            ),
            "total_time_defensive": match_data.get(
                "total_time_defensive", equipe2_stats["total_time_defensive"]
            ),
            "total_time_neutral": match_data.get(
                "total_time_neutral", equipe2_stats["total_time_neutral"]
            ),
            "total_demos_infliges": match_data.get(
                "total_demos_infliges", equipe2_stats["total_demos_infliges"]
            ),
            "total_demos_recus": match_data.get(
                "total_demos_recus", equipe2_stats["total_demos_recus"]
            ),
        }

        return stats_match
