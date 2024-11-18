from service.tournoi_service import TournoiService
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer
import time


class TournoiVue(VueAbstraite):
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

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        # self.tournoi.afficher_infos_tournois()

        choix = inquirer.select(
            message="Souhaitez-vous lancer un nouveau tournoi?",
            choices=[
                "Créer un tournoi",
                "Gérer mes tournois",
                "Rejoindre un tournoi",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Rejoindre un tournoi":
                res = input("Entrez la clef du tournoi: ")
                tournoi = self.tournoi.recuperer_tournoi_par_clef(res)
                if not tournoi:
                    print("La clef ne correspond à aucun tournoi")
                    time.sleep(2)
                    return self
                from view.tournoi.gestion_tournoi_vue import GestionTournoiVue
                return GestionTournoiVue

            case "Créer un tournoi":
                from view.tournoi.nouveau_tournoi_vue import NouveauTournoiVue

                return NouveauTournoiVue()
