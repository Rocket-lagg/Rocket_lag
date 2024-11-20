from service.consulter_stats import ConsulterStats
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class MatchVue(VueAbstraite):
    """Une vue pour afficher les statistiques des matchs"""

    def __init__(self, message=""):
        self.message = message
        self.consulter_stats = ConsulterStats()

    def message_info(self):
        print("Consultation des statistiques des matchs")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message="",
            choices=[
                "Rechercher le match par joueur",
                "Rechercher le match par équipe",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Rechercher le match par joueur":

                from view.statistique.match_joueur_vue import MatchJoueurVue

                return MatchJoueurVue()

            case "Rechercher le match par équipe":
                from view.statistique.match_equipe_vue import MatchEquipeVue

                return MatchEquipeVue()
