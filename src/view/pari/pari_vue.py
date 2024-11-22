from service.paris_service import ParisService
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer
from dao.paris_dao import ParisDao

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
                    tournaments = ParisDao().get_available_tournaments()  # Méthode qui récupère les tournois disponibles

                    choix_tournoi = inquirer.select(
                        message="Quel tournoi voulez-vous choisir ?",
                        choices=tournaments,
                    ).execute()

                    # Récupérer les équipes disponibles pour le tournoi choisi
                    available_teams = ParisDao().get_teams_for_tournament(choix_tournoi)  # Méthode qui récupère les équipes disponibles pour ce tournoi

                    choix_match = inquirer.select(
                        message="Quelle match souhaitez-vous parier ?",
                        choices=available_teams,
                    ).execute()

                    sep= " vs "
                    cleaned_match = choix_match.strip().split(sep)  # Diviser la chaîne par " vs "

                    # Extraire les noms des équipes
                    equipe1 = cleaned_match[0].split()[-1]  # Dernier mot avant "vs"
                    equipe2 = cleaned_match[1].split()[0]
                    choix_equipe = inquirer.select(
                        message="Quelle équipe/joueur souhaitez-vous parier ?",
                        choices=[equipe1,equipe2],
                    ).execute()

                    # Effectuer le pari avec le tournoi et l'équipe choisis

                    self.paris.parier(choix_tournoi, choix_equipe)

                case "Retour":
                    # L'utilisateur a choisi "Retour", on revient à la vue d'accueil
                    from view.accueil.accueil_vue import AccueilVue
                    return AccueilVue()

                case "Voir tous vos paris passées":
                    # L'utilisateur a choisi "Voir tous les paris", on affiche les paris possibles
                    print("TOUS LES PARIS")
                    self.paris.info_paris()

                    self.paris.voir_paris()
