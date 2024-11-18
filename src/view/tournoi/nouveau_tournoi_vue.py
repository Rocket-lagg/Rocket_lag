from service.tournoi_service import TournoiService
from view.vue_abstraite import VueAbstraite
import time
from view.session import Session


class NouveauTournoiVue(VueAbstraite):
    """Une vue pour la création d'un tournoi"""

    def __init__(self, message=""):
        self.message = message
        self.tournoi = TournoiService()

    def message_info(self):
        print("Nouveau Tournoi")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        nom_tournois = input("Quel nom souhaitez-vous donner à votre tournoi? ")
        type_tournois = int(
            input("Quel type de tournois voulez-vous? (tapez 1 pour 1v1, 2 pour 2v2, 3 pour 3v3) ")
        )
        tours = int(input("Nombre de tours pour ce tournoi"))
        if type_tournois != 1 and type_tournois != 2 and type_tournois != 3:
            print("Tapez 1, 2 ou 3")
            time.sleep(2)
            return self

        tournoi = self.tournoi.creer_tournois(nom_tournois, type_tournois, tours)
        clef_tournoi = tournoi.id_tournoi
        Session().tournoi = tournoi
        print(f"La clef pour rejoindre le tounoi est:\n{clef_tournoi}")
        input("Appuyer sur entrée pour passer à la suite")
        from view.tournoi.gestion_tournoi_vue import GestionTournoiVue

        return GestionTournoiVue()
