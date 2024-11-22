from view.session import Session
from dao.paris_dao import ParisDao
from business_object.Pari import Pari
from dao.utilisateur_dao import UtilisateurDao
from dao.pari_dao import pariDao
from dao.match_dao import MatchDao
from service.pari_service import pariService
from service.match_service import MatchService


class ParisService:

    def __init__(self):
        self.utilisateur_dao = UtilisateurDao()
        self.pari_dao = pariDao()
        self.match_dao = MatchDao()

    def afficher_infos_paris_possible(self):

        nom_utilisateur = Session().utilisateur.nom_utilisateur
        paris_dao = ParisDao()
        paris = paris_dao.afficher_infos_paris()

        return paris

    def info_paris(self):
        pseudo = Session().utilisateur.nom_utilisateur
        paris_dao = ParisDao()
        info_paris = paris_dao.info_paris(pseudo)
        return info_paris

    def parier(self, tournoi, pari):  # créer un menu dans la view
        "Enregistre le paris de l'utilisateur dans la base de données"
        if not isinstance(tournoi, str):
            raise TypeError("Match doit être une chaîne de charactères")

        pseudo = Session().utilisateur.nom_utilisateur
        ParisDao().ajouter_un_pari(tournoi, pari,pseudo)
        print(f"Vous avez parié sur {pari} dans le tournoi {tournoi}.")

    def terminer_paris(pari, gagnant):
        "Donne le résultat du paris quand le match a été joué"
        if not isinstance(pari, Pari):
            raise TypeError("Le pari doit être de type Pari")
        if pari.pari == gagnant:
            pari.statut = "Remporté"
        else:
            pari.statut = "Perdu"
        ParisDao().changer_statut(pari.statut)

    def supprimer_paris(pari):
        "Supprime un pari"
        if not isinstance(pari, Pari):
            raise TypeError("Le pari doit être de type Pari")
        ParisDao().supprimer_paris(pari)


