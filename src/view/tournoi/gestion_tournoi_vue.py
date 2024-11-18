from service.tournoi_service import TournoiService
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer
import random
from view.session import Session
import time


class GestionTournoiVue(VueAbstraite):
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

        choix = inquirer.select(
            message="Que souhaitez vous faire?",
            choices=[
                "Créer une équipe",
                "Faire le pooling (minimum 2 équipes)",
                "Rentrer le score d'un match",
                "Donner le gagnant du tournoi",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Créer une équipe":
                res = input("Nom de l'équipe: ")
                if res and res.strip():
                    id_tournoi = Session().tournoi.id_tournoi
                    self.tournoi.creer_equipe(res, id_tournoi)
                return self

            case "Faire le pooling":
                id_tournoi = Session().tournoi.id_tournoi
                liste_equipe = self.tournoi.recuperer_equipe(id_tournoi)
                if liste_equipe == []:
                    print("Vous n'avez aucune équipe de créée")
                if len(liste_equipe) % 2 != 0:
                    raise ValueError(
                        "Le nombre d'équipes doit être pair pour créer des rencontres."
                    )
                random.shuffle(liste_equipe)
                liste_pairs = [
                    (liste_equipe[i], liste_equipe[i + 1]) for i in range(0, len(liste_equipe), 2)
                ]
                for element in liste_pairs:
                    self.tournoi.ajouter_match(element)
                return liste_pairs
                return self

            case "Rentrer le score d'un match":
                matches = self.tournoi.recuperer_match()
                if matches == []:
                    print("Vous n'avez pas de matchs prévus dans ce tournoi")
                    time.sleep(2)
                    return self
                matchs_choix = [
                    {"name": f"{match[1]} vs {match[2]}", "value": match} for match in matches
                ]
                matchs_choix.apen({"name": "Retour", "value": "quit"})
                matches_questions = inquirer.select(
                    message="Que souhaitez vous faire?",
                    choices=matchs_choix,
                ).execute()
                if matches_questions == "quit":
                    return self
                else:
                    match1 = matches_questions
                    print("\\n")
                    score1 = input(f"Score de l'équipe {match1[1]}")
                    try:
                        score1 = int(score1)
                    except ValueError:
                        print("Le score doit être un entier")
                        time.sleep(2)
                        return self
                    print("\\n")
                    score2 = input(f"Score de l'équipe {match1[2]}")
                    try:
                        score2 = int(score2)
                    except ValueError:
                        print("Le score doit être un entier")
                        time.sleep(2)
                        return self
                    self.tournoi.ajouter_score(score1, score2, match1)
                return self
