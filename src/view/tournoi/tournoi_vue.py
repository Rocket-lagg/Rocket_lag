from service.tournoi_service import TournoiService
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer
from view.session import Session
from view.tournoi.gestion_tournoi_vue import GestionTournoiVue
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

        print("\n" + "-" * 50 + "\n TOURNOIS \n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Souhaitez-vous lancer un nouveau tournoi?",
            choices=[
                "Créer un tournoi",
                "Gérer mes tournois",
                "Rejoindre un tournoi",
                "Afficher mes tournois",
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
                print(tournoi)
                Session().tournoi = tournoi[0]
                from view.tournoi.rejoindre_tournoi_vue import RejoindreTournoiVue

                return RejoindreTournoiVue()

            case "Créer un tournoi":
                from view.tournoi.nouveau_tournoi_vue import NouveauTournoiVue

                return NouveauTournoiVue()

            case "Afficher mes tournois":
                from view.tournoi.info_tournoi_vue import InfoTournoiVue

                return InfoTournoiVue()

            case "Gérer mes tournois":
                tournois = self.tournoi.recuperer_tournois()

                tournois_choix = [{"name": t.nom_tournoi, "value": t} for t in tournois]

                tournois_choix.append({"name": "Retour", "value": "quit"})
                tournois_questions = inquirer.select(
                    message="Quel tournoi voulez-vous modifier?",
                    choices=tournois_choix,
                ).execute()
                if tournois_questions == "quit":
                    return self
                else:
                    print(tournois_questions)
                    Session().tournoi = tournois_questions
                    return GestionTournoiVue()
