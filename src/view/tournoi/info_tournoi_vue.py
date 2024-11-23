from service.tournoi_service import TournoiService
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer
from view.session import Session
from prettytable import PrettyTable


class InfoTournoiVue(VueAbstraite):
    """Une vue pour afficher les tournois d'un utilisateur"""

    def __init__(self, message=""):
        self.message = message
        self.tournoi = TournoiService()

    def message_info(self):
        print("Tournois de l'utilisateur")

    def afficher_tournoi(self, info):
        print("\n=== Informations du Tournoi ===")
        tournoi_info = info["tournoi_info"]
        print(f"Nom : {tournoi_info['nom']}")
        print(f"Créateur : {tournoi_info['nom_createur']}")
        print(f"Type de match : {tournoi_info['type_match']}")
        print(f"Nombre de tours : {tournoi_info['tours']}")
        print(f"Officiel : {'Oui' if tournoi_info['officiel'] else 'Non'}")

        print("\n=== Équipes du Tournoi ===")
        table_equipes = PrettyTable(["Nom de l'équipe", "Tour", "Joueur 1", "Joueur 2", "Joueur 3"])
        for equipe in info["equipes"]:
            table_equipes.add_row(
                [
                    equipe["nom_equipe"],
                    equipe["tour"],
                    equipe["joueur1"],
                    equipe["joueur2"],
                    equipe["joueur3"],
                ]
            )
        print(table_equipes)

        print("\n=== Matchs du Tournoi ===")
        table_matchs = PrettyTable(
            ["ID Match", "Équipe 1", "Équipe 2", "Score Équipe 1", "Score Équipe 2", "Tour"]
        )
        for match in info["matchs"]:
            table_matchs.add_row(
                [
                    match["id_match"],
                    match["equipe1"],
                    match["equipe2"],
                    match["score_equipe1"],
                    match["score_equipe2"],
                    match["tour"],
                ]
            )
        print(table_matchs)

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\n INFORMATION TOURNOIS DE L'UTILISATEUR \n" + "-" * 50 + "\n")

        utilisateur = Session().utilisateur.nom_utilisateur
        liste_tournoi = self.tournoi.recuperer_tournois(utilisateur)

        for tournoi in liste_tournoi:
            info = self.tournoi.recuperer_tournoi_info(tournoi.id_tournoi)
            self.afficher_tournoi(info)

        choix = inquirer.select(
            message=" ",
            choices=[
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.tournoi.tournoi_vue import TournoiVue

                return TournoiVue()
