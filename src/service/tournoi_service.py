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

    def creer_tournois(self, nom_tournoi, type_tournoi):
        nom_utilisateur = Session().utilisateur.nom_utilisateur
        id_tournoi = hash_password(nom_tournoi, sel=nom_utilisateur)
        res = self.tournoi_dao.creer_tournoi(nom_utilisateur, id_tournoi, nom_tournoi, type_tournoi)
        tournoi = Tournoi(nom_tournoi, Session().utilisateur, id_tournoi)
        print(res)
        return tournoi

    def recuperer_tournois(self):
        nom_utilisateur = Session().utilisateur.nom_utilisateur
        tournois = self.tournoi_dao.recuperer_tournois_par_utilisateur(nom_utilisateur)
        return tournois

    def creer_equipe(self, id_tournoi, nom_equipe):
        self.tournoi_dao.creer_equipe(id_tournoi, nom_equipe)

    def creer_match(self, equipe1, equipe2, tour=1):
        self.tournoi_dao.creer_equipe(equipe1, equipe2, tour)

    def recuperer_equipe(self, id_tournoi):
        equipes = self.tournoi_dao.recuperer_equipe(id_tournoi)
        return equipes

    def ajouter_match(self, rencontre):
        equipe1 = rencontre[0]
        equipe2 = rencontre[1]
        self.tournoi_dao.creer_match(Session().tournoi.id_tournoi, equipe1, equipe2)

    def recuperer_match(self):
        tournoi = Session().tournoi
        matches = self.tournoi_dao.trouver_matchs_par_tournoi(tournoi.id_tournoi)
        return matches

    def ajouter_score(self, score1, score2, match):
        id_match = match[0]
        self.tournoi_dao.ajouter_score_match(score1, score2, id_match)

    def afficher_infos_tournois(self):
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
