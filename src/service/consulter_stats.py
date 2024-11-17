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
        regional_indice = regional_indices.get(joueur_data.region)
        if regional_indice is None:
            raise ValueError("La région du joueur est inconnue.")

        # Calcul des statistiques par match
        joueur_data.goals_par_match = self.stats_par_match(joueur_data.goals, n)
        joueur_data.assists_par_match = self.stats_par_match(joueur_data.assists, n)
        joueur_data.shots_par_match = self.stats_par_match(joueur_data.shots, n)
        joueur_data.saves_par_match = self.stats_par_match(joueur_data.saves, n)
        joueur_data.score_par_match = self.stats_par_match(joueur_data.score, n)
        joueur_data.demo_inflige_par_match = self.stats_par_match(joueur_data.demo_inflige, n)

        # Calcul des indices
        joueur_data.indice_offensif = round(
            (
                joueur_data.goals / 1.05
                + joueur_data.assists / 0.5
                + joueur_data.shots / 3.29
                + joueur_data.demo_inflige / 0.56
                + joueur_data.time_offensive_third / 201.1
            )
            / n,
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
            / n
            * regional_indice,
            2,
        )

        return joueur_data

    # Note pour les vues : Les stats à afficher dans la vue sont : goals, goals par match, assists, assists par match,
    # saves, saves par match, shots, shots par match, score, score par match, demo infligées, demo infligées par match,
    # indice de performance, indice offensif, pourcentage de tirs

    def stats_equipe(self, nom_equipe):
        """Une fonction qui permet d'afficher les statistiques par équipe"""
        if not isinstance(nom_equipe, str):
            raise TypeError("'nom_equipe' doit être une instance de str")

        equipedao = EquipeDao()
        equipe_data = equipedao.obtenir_par_nom(nom_equipe)

        if not equipe_data:
            raise ValueError(f"Aucune équipe nommée {nom_equipe} n'a été trouvée.")

        matchdao = MatchDao()
        id_matchs = matchdao.trouver_id_match_par_equipe(nom_equipe)
        n = len(id_matchs)

        if n == 0:
            raise ValueError(f"Aucun match n'a été trouvé pour l'équipe {nom_equipe}.")

        # Calcul des statistiques par match
        equipe_data.goals_par_match = self.stats_par_match(equipe_data.goals, n)
        equipe_data.assists_par_match = self.stats_par_match(equipe_data.assists, n)
        equipe_data.shots_par_match = self.stats_par_match(equipe_data.shots, n)
        equipe_data.score_par_match = self.stats_par_match(equipe_data.score, n)
        equipe_data.demo_inflige_par_match = self.stats_par_match(equipe_data.demo_inflige, n)

        # Calcul de l'indice de pression
        equipe_data.indice_de_pression = round(
            (
                equipe_data.demo_inflige / 1.68
                + equipe_data.time_offensive_third / 603.3
                + equipe_data.boost_stole / 1500
            )
            / n,
            2,
        )

        return equipe_data

        # Note pour les vues : Les statistiques à afficher sont : les joueurs (equipe_data.joueurs),
        # shots, shots par match, goals, goals par match, assists, assists par match, saves, saves par match,
        # pourcentage de tir, rating, rating par match, demo infligées, demo infligées par match, indice de pression

        # Note pour les fonctions DAO : penser à ajouter un argument "joueurs" dans Equipe() qui contienne les
        # noms des joueurs qui constituent l'équipe, et penser à implémenter ça dans les fonctions DAO.

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
