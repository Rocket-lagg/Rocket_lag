from service.tournoi_service import TournoiService
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer
from view.session import Session


class RejoindreTournoiVue(VueAbstraite):
    """Une vue pour afficher les tournois d'un utilisateur"""

    def __init__(self, message=""):
        self.message = message
        self.tournoi = TournoiService()

    def message_info(self):
        print("Tournois de l'utilisateur")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\n REJOINDRE TOURNOIS \n" + "-" * 50 + "\n")

        tournoi = Session().tournoi
        type_tournoi = tournoi.type_match
        liste_equipe = self.tournoi.recuperer_equipe_joueur(tournoi.id_tournoi, type_tournoi)

        liste_equipe.append("Retour")
        equipe_question = inquirer.select(
            message="Quelle équipe voulez-vous rejoindre? ",
            choices=liste_equipe,
        ).execute()

        if equipe_question == "Retour":
            from view.tournoi.tournoi_vue import TournoiVue

            return TournoiVue()
        else:
            equipe = equipe_question
            self.tournoi.ajouter_joueur_equipe(equipe)
            print(f"Vous faites désormais partie de l'équipe {equipe} ")

        choix = inquirer.select(
            message=" ",
            choices=[
                "Afficher le récapitulatif des tournois",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.tournoi.tournoi_vue import TournoiVue

                return TournoiVue()

            case "Afficher le récapitulatif des tournois":
                from view.tournoi.info_tournoi_vue import InfoTournoiVue

                return InfoTournoiVue()
