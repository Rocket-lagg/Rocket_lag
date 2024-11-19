from service.consulter_stats import ConsulterStats
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class MatchEquipeVue(VueAbstraite):
    """Une vue pour afficher les stats d'un match par équipe"""

    def __init__(self, message=""):
        self.message = message
        self.consulter_stats = ConsulterStats()

    def message_info(self):
        print("Consultation des statstiques d'un match à partir du nom d'équipe")

    def choisir_menu(self):
        """Demander un nom d'équpe, obtenir les matchs associés et permettre la sélection d'un match"""

        equipe = inquirer.text(message="Entrez le nom de l'équipe :").execute()

        if not isinstance(equipe, str):
            raise TypeError("'nom_equipe' doit être une instance de str.")

        matchs = self.consulter_stats.choix_match_equipe(equipe)

        if not matchs:
            print("Aucun match trouvé pour cette équipe.")
            return None

        choices = []
        for match_key, match_ids in matchs.items():
            for match_id in match_ids:
                choices.append(f"{match_key} (ID: {match_id})")

        print("\n" + "-" * 50 + "\nSélectionner un match\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message="Sélectionnez un match :",
            choices=choices,
        ).execute()

        # Trouver l'ID du match sélectionné
        match_selected = choices[choices.index(choix)]
        match_id = match_selected.split("(ID: ")[-1][:-1]

        print(f"\nVous avez sélectionné le match : {choix}")

        # Appel à la fonction pour afficher toutes les statistiques du match
        self.traiter_match(match_id)

    def traiter_match(self, match_id):
        try:
            # Essayer de récupérer les détails du match
            match_details = self.consulter_stats.stats_completes_match(match_id)

            if not match_details:
                print(f"Aucune statistique trouvée pour le match avec l'ID {match_id}.")
                return

            # Si les détails du match sont trouvés, afficher les informations
            print("\n--- Détails du Match ---")
            # Utilisation de la notation dictionnaire pour accéder aux valeurs
            print(f"Match: {match_details['equipe1']} vs {match_details['equipe2']}")
            print(f"Score: {match_details['score1']} - {match_details['score2']}")
            print(f"Date: {match_details['date']}")
            print(f"Stage: {match_details['stage']}")
            print(f"Ligue: {match_details['ligue']}")
            print(f"Région: {match_details['region']}")
            print(
                "\n" + "-" * 50
            )  # Ligne de séparation entre les détails du match et les stats des équipes
            print("--- Statistiques des Équipes ---")

            # Afficher les statistiques agrégées des équipes
            for equipe, equipe_stats in zip(
                [match_details["equipe1"], match_details["equipe2"]],
                [match_details["equipe1_stats"], match_details["equipe2_stats"]],
            ):
                print(f"\nÉquipe: {equipe}")
                print(f"Score: {equipe_stats['score']}")
                print(f"Boost volé: {equipe_stats['boost_stole']}")
                print(f"Temps en Zone Offensive: {equipe_stats['total_time_offensive']}")
                print(f"Temps en Zone Défensive: {equipe_stats['total_time_defensive']}")
                print(f"Temps en Zone Neutre: {equipe_stats['total_time_neutral']}")
                print(f"Démolitions infligées: {equipe_stats['total_demos_infliges']}")
                print(f"Démolitions reçues: {equipe_stats['total_demos_recus']}")
                print(f"{'-'*50}")  # Ligne de séparation après les statistiques de l'équipe

            print("\n" + "-" * 50)  # Ligne de séparation avant les statistiques des joueurs
            print("--- Statistiques des Joueurs ---")

            # Afficher les statistiques des joueurs par équipe
            for equipe, joueurs in match_details["joueurs"].items():
                print(f"\n{'-'*50}")  # Ligne de séparation avant chaque équipe
                print(f"Équipe: {equipe}")
                print(
                    f"Score: {match_details['score1'] if equipe == match_details['equipe1'] else match_details['score2']}"
                )
                print(f"Région: {match_details['region']}")
                print(f"Ligue: {match_details['ligue']}")
                print(f"Stage: {match_details['stage']}")
                print(f"{'-'*50}")  # Ligne de séparation après les informations de l'équipe

                # Liste des joueurs et leurs statistiques
                for joueur in joueurs:
                    print(f"\nJoueur: {joueur['nom']} ({joueur['nationalite']})")
                    print(f"Rating: {joueur['rating']}")
                    print(f"Goals: {joueur['goals']}, Assists: {joueur['assists']}")
                    print(f"Saves: {joueur['saves']}, Shots: {joueur['shots']}")
                    print(f"Score: {joueur['score']}")
                    print(f"Shooting %: {joueur['shooting_percentage']}")
                    print(f"Temps en Zone Offensive: {joueur['time_offensive_third']}")
                    print(f"Temps en Zone Défensive: {joueur['time_defensive_third']}")
                    print(f"Temps en Zone Neutre: {joueur['time_neutral_third']}")
                    print(
                        f"Démolitions infligées: {joueur['demo_inflige']}, Reçues: {joueur['demo_recu']}"
                    )
                    print(f"Participation aux Buts: {joueur['goal_participation']}")
                    print(f"Indice Offensif: {joueur['indice_offensif']}")
                    print(f"Indice de Performance: {joueur['indice_performance']}")
                    print(f"{'-'*50}")  # Ligne de séparation après chaque joueur

        except Exception as e:
            print(f"Une erreur inattendue s'est produite : {e}")

        choix = inquirer.select(
            message="Que voulez-vous faire maintenant?",
            choices=[
                "Chercher un autre match avec un nom de joueur",
                "Chercher un autre match avec un nom d'équipe",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":

                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Chercher un autre match avec un nom de joueur":

                from view.statistique.match_joueur_vue import MatchJoueurVue

                return MatchJoueurVue()

            case "Chercher un autre match avec un nom d'équipe":

                return self
