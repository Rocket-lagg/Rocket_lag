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

    def recuperer_tournois(self, nom_utilisateur=None):
        if not nom_utilisateur:
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

    def recuperer_tournoi_par_clef(self, clef):
        tournoi = self.tournoi_dao.recuperer_tournoi_par_clef(clef)
        return tournoi

    def recuperer_joueur_par_equipe(self, nom):
        joueurs = self.tournoi_dao.recuperer_joueur_par_equipe(nom)
        return joueurs

    def recuperer_equipe_joueur(self, id_tournoi, type_tournoi):
        noms_equipes = self.tournoi_dao.recuperer_equipe(id_tournoi, 1)
        for noms in noms_equipes:
            joueur = self.tournoi_dao.recuperer_joueur_par_equipe(noms)
            if len(joueur) == type_tournoi:
                noms_equipes.remove(noms)
        return noms_equipes

    def ajouter_joueur_equipe(self, equipe):
        joueur = Session().utilisateur.nom_utilisateur
        tournoi = Session().tournoi.id_tournoi
        self.tournoi_dao.ajouter_joueur_equipe(joueur, equipe)
        self.tournoi_dao.ajouter_joueur_tournoi(joueur, tournoi)

    def recuperer_tournoi_info(self, id_tournoi):
        tournoi_info = self.tournoi_dao.recuperer_tournoi_info(id_tournoi)
        equipes = self.tournoi_dao.recuperer_equipes_tournoi(id_tournoi)
        matchs = self.tournoi_dao.recuperer_matchs_tournoi(id_tournoi)

        if not tournoi_info:
            raise ValueError(f"Aucun tournoi trouvé avec l'ID {id_tournoi}")

        return {
            "tournoi_info": tournoi_info,
            "equipes": equipes,
            "matchs": matchs,
        }

