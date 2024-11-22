from service.paris_service import ParisService
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class PariVue(VueAbstraite):
    """Une vue pour afficher les paris d'un utilisateur"""

    def __init__(self, message=""):
        self.message = message
        self.paris = ParisService()

    def message_info(self):
        print("Paris de l'utilisateur")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        while True:


            choix = inquirer.select(
            message="Souhaitez-vous faire un nouveau pari ?",
            choices=[
                "Parier sur un nouveau match",
                "Retour",
                "Voir tous les paris",

            ],
        ).execute()

            match choix:
                case "Parier sur un nouveau match":
                    # Demander à l'utilisateur de choisir un tournoi parmi les disponibles
                    tournaments = self.get_available_tournaments()  # Méthode qui récupère les tournois disponibles

                    choix_tournoi = inquirer.select(
                        message="Quel tournoi voulez-vous choisir ?",
                        choices=tournaments,
                    ).execute()

                    # Récupérer les équipes disponibles pour le tournoi choisi
                    available_teams = self.get_teams_for_tournament(choix_tournoi)  # Méthode qui récupère les équipes disponibles pour ce tournoi

                    choix_equipe = inquirer.select(
                        message="Quelle équipe souhaitez-vous parier ?",
                        choices=available_teams,
                    ).execute()

                    # Effectuer le pari avec le tournoi et l'équipe choisis
                    self.parier(choix_tournoi, choix_equipe)

                case "Retour":
                    # L'utilisateur a choisi "Retour", on revient à la vue d'accueil
                    from view.accueil.accueil_vue import AccueilVue
                    return AccueilVue()

                case "Voir tous vos paris passées":
                    # L'utilisateur a choisi "Voir tous les paris", on affiche les paris possibles
                    self.paris.info_paris()
