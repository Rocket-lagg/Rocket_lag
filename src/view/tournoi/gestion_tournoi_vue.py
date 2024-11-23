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

    def creer_equipe(self):
        res = input("Nom de l'équipe: ")
        if res and res.strip():
            id_tournoi = Session().tournoi.id_tournoi
            self.tournoi.creer_equipe(id_tournoi, res, tour=1)

    def faire_le_pooling(self, j):
        "Donne les matchs à faire des équipes"

        id_tournoi = Session().tournoi.id_tournoi
        liste_equipe = self.tournoi.recuperer_equipe(id_tournoi, j)

        # Permet de vérifier si les équipes se sont crées
        if liste_equipe == []:
            print("Vous n'avez aucune équipe de créée")
            time.sleep(2)
            return self.creer_equipe()

        if len(liste_equipe) == 1:
            gagnant_tournoi = liste_equipe[0]
            print(f"L'équipe {gagnant_tournoi} remporte le tournoi!")
            self.tournoi.afficher_pooling_tournoi()
            input("Pressez 'entrée' pour retourner vers le menu des tournois")
            return True

        # Fait le pooling (création de paires aléatoires d'équipes)
        random.shuffle(liste_equipe)
        liste_pairs = [
            (liste_equipe[i], liste_equipe[i + 1]) for i in range(0, len(liste_equipe), 2)
        ]
        i = 1

        # Affiche les paires
        for element in liste_pairs:
            print(f"Paire numéro {i}: {element}")
            i += 1

        result = input("Les paires constituées vous conviennent-elles ? (Oui/Non): ")

        if result != "Oui":
            print("Tant pis")

        for element in liste_pairs:
            self.tournoi.ajouter_match(element, j)
            print("Matchs enregistrés")
        return False

    def rentrer_score_match(self, tours, id_utilise: list = []):
        matches = self.tournoi.recuperer_match(tours)

        # Permet de vérifer si les matchs sont crées
        if matches == []:
            print("Vous n'avez pas de matchs prévus dans ce tournoi")
            time.sleep(2)
            return self.faire_le_pooling(tours)

        # Permet de retirer des choix les matchs dont le score est déjà rempli
        if id_utilise != []:
            for i in range(len(id_utilise)):
                for matche in matches:
                    if matche[0] == id_utilise[i]:
                        matches.remove(matche)

        # Menu de choix
        matchs_choix = [{"name": f"{match[1]} vs {match[2]}", "value": match} for match in matches]
        matchs_choix.append({"name": "Retour", "value": "quit"})
        matches_questions = inquirer.select(
            message="Veuillez renseigner le score dans les matchs suivants:",
            choices=matchs_choix,
        ).execute()

        if matches_questions == "quit":
            from view.tournoi.tournoi_vue import TournoiVue

            return TournoiVue()
        else:
            match1 = matches_questions
            print("\n")
            score1 = input(f"Score de l'équipe {match1[1]}: ")

            # Vérification que c'est un entier
            try:
                score1 = int(score1)
            except ValueError:
                print("Le score doit être un entier")
                time.sleep(2)
                return self.rentrer_score_match()

            print("\n")
            score2 = input(f"Score de l'équipe {match1[2]}: ")

            # Vérification que c'est un entier
            try:
                score2 = int(score2)
            except ValueError:
                print("Le score doit être un entier")
                time.sleep(2)
                return self.rentrer_score_match()

            self.tournoi.ajouter_score(score1, score2, match1)
            print("Score ajouté!\n")
            return match1

    def determiner_gagnant_equipe(self, tours, match):
        liste_equipe = match
        equipe1 = liste_equipe[1]
        equipe2 = liste_equipe[2]
        liste_match = self.tournoi.recuperer_score_match(equipe1, equipe2)
        score1 = liste_match[0]
        score2 = liste_match[1]
        if score1 > score2:
            gagnant = equipe1
            print(f"L'équipe gagnante du match est {equipe1}. Félicitation!\n")
        else:
            gagnant = equipe2
            print(f"L'équipe gagnante du match est {equipe2}. Félicitation!\n")
        return gagnant

    def choisir_menu(self):
        """ """
        nom_tournoi = Session().tournoi.nom_tournoi

        print(f"""{"-" * 45} Gestion du tournoi {nom_tournoi}{"-" * 45}""")

        tournoi = Session().tournoi
        nb_tours = tournoi.tour
        nb_equipe = 2**nb_tours
        nb_equipe_crees = self.tournoi.donner_nombre_equipe()
        fin = False

        # Vérification de la création des équipes
        if nb_equipe_crees != nb_equipe:
            print(f"Vous devez créer {nb_equipe} équipes.")
            # Création du nombre d'équipes correspondant au nombre de tours
            for i in range(1, nb_equipe + 1):
                print(f"Création de l'équipe {i}")
                self.creer_equipe()

        # Itération de tous les tours
        for i in range(1, nb_tours + 2):
            print('blip')
            tours = self.tournoi.recuperer_tour()
            print(tours)
            pooling_pour_ce_tour = self.tournoi.pooling_pour_ce_tour(tours)

            # Itération du i-ème tour
            if tours == i:
                print(f"TOUR {i}")

                # Faire le pooling des équipes
                if not pooling_pour_ce_tour:
                    print("POOLING DES EQUIPES")
                    fin = self.faire_le_pooling(i)

                if fin:
                    from view.tournoi.tournoi_vue import TournoiVue

                    return TournoiVue()

                rep = input("Est-ce que vous avez les scores des matchs (Oui/Non)? ")

                if rep == "Oui":
                    print("RENTRER SCORE")
                    liste_gagnant = []
                    liste_match = []
                    nb_match = int(nb_equipe / (2**tours))

                    for i in range(nb_match):
                        match = self.rentrer_score_match(tours, liste_match)
                        liste_match.append(match[0])

                        gagnant = self.determiner_gagnant_equipe(tours, match)
                        if gagnant not in liste_gagnant:
                            liste_gagnant.append(gagnant)
                            self.tournoi.modifier_tour_gagnant(gagnant)

                else:
                    print("Tournoi créé avec succès, retour à la liste des tournois")
                    from view.tournoi.tournoi_vue import TournoiVue

                    return TournoiVue()
