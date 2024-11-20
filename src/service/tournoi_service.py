from view.session import Session
from dao.tournoi_dao import TournoiDao
from business_object.Tournoi import Tournoi
from dao.utilisateur_dao import UtilisateurDao
from dao.match_dao import MatchDao
from utils.securite import hash_password


class TournoiService:

    def __init__(self):
        self.utilisateur_dao = UtilisateurDao()
        self.match_dao = MatchDao()
        self.tournoi_dao = TournoiDao()

    def creer_tournois(self, nom_tournoi, type_tournoi, tour):
        nom_utilisateur = Session().utilisateur.nom_utilisateur
        id_tournoi = hash_password(nom_tournoi, sel=nom_utilisateur)
        self.tournoi_dao.creer_tournoi(nom_utilisateur, id_tournoi, nom_tournoi, type_tournoi, tour)
        tournoi = Tournoi(nom_tournoi, Session().utilisateur, id_tournoi, tour, type_tournoi)
        return tournoi

    def recuperer_tournois(self):
        nom_utilisateur = Session().utilisateur.nom_utilisateur
        tournois = self.tournoi_dao.recuperer_tournois_par_utilisateur(nom_utilisateur)
        return tournois

    def creer_equipe(self, id_tournoi, nom_equipe, tour):
        self.tournoi_dao.creer_equipe(id_tournoi, nom_equipe, tour)

    def creer_match(self, equipe1, equipe2, tour=1):
        self.tournoi_dao.creer_equipe(equipe1, equipe2, tour)

    def recuperer_equipe(self, id_tournoi, tour):
        equipes = self.tournoi_dao.recuperer_equipe(id_tournoi, tour)
        return equipes

    def ajouter_match(self, rencontre, tour):
        equipe1 = rencontre[0]
        equipe2 = rencontre[1]
        self.tournoi_dao.creer_match(Session().tournoi.id_tournoi, equipe1, equipe2, tour)

    def recuperer_match(self, tour):
        tournoi = Session().tournoi
        matches = self.tournoi_dao.trouver_matchs_par_tournoi(tournoi.id_tournoi, tour)
        return matches

    def ajouter_score(self, score1, score2, match):
        id_match = match[0]
        self.tournoi_dao.ajouter_score_match(score1, score2, id_match)

    def recuperer_score_match(self, equipe1, equipe2):
        scores = self.tournoi_dao.recuperer_score_match(equipe1, equipe2)
        return scores

    def modifier_tour_gagnant(self, equipe):
        self.tournoi_dao.modifier_tour_gagnant_equipe(equipe)

    def afficher_infos_tournois(self):  # A modifier
        "Affiche les tournois d'un utilisateur"
        nom_utilisateur = Session().utilisateur.nom_utilisateur
        tournois = self.tournoi().afficher_infos_tournois(nom_utilisateur)
        if tournois == []:
            print(f"{nom_utilisateur}, vous n'avez pas fait de tournois")
        else:
            liste_tournois = []
            for tournoi in tournois:
                liste_tournois.append(self.instancier_tournois(tournoi))
            print(liste_tournois)
        return liste_tournois

    def recuperer_tour(self):
        tours = self.tournoi_dao.recuperer_tour()
        return tours

    def donner_nombre_equipe(self):
        nb_equipe = self.tournoi_dao.donner_nombre_equipe()
        return nb_equipe

    def pooling_pour_ce_tour(self, tour):
        tour_dao = self.tournoi_dao.recuperer_tour_depuis_match()
        if tour_dao == tour:
            return True
        else:
            return False

    def afficher_pooling_tournoi(self):
        self.tournoi_dao.afficher_pooling_tournoi()
