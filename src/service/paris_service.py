from view.session import Session
from dao.paris_dao import ParisDao
from business_object.Pari import Pari
from dao.utilisateur_dao import UtilisateurDao
from dao.paris_dao import ParisDao
from dao.match_dao import MatchDao
from service.match_service import MatchService


class ParisService:

    def __init__(self):
        self.utilisateur_dao = UtilisateurDao()
        self.paris_dao = ParisDao()
        self.match_dao = MatchDao()

    def afficher_infos_paris_possible(self):
        """
        Récupère et retourne les informations sur les paris possibles pour l'utilisateur.

        Return
        ------
        paris : list
            Liste des paris disponibles récupérés via ParisDao. Chaque entrée de la liste représente un pari possible.
        """
        nom_utilisateur = Session().utilisateur.nom_utilisateur
        paris_dao = ParisDao()
        paris = paris_dao.afficher_infos_paris()

        return paris

    def info_paris(self):
        """
        Récupère les informations des paris effectués par l'utilisateur.

        Return
        ------
        info_paris : list
            Liste des paris déjà effectués par l'utilisateur, récupérée via ParisDao.
        """
        pseudo = Session().utilisateur.nom_utilisateur
        paris_dao = ParisDao()
        info_paris = paris_dao.info_paris(pseudo)
        return info_paris

    def parier(self, tournoi, equipe):  # créer un menu dans la view
        """
        Enregistre un pari effectué par l'utilisateur dans la base de données.

        Parameters
        ----------
        tournoi : str
            Le nom du tournoi sur lequel l'utilisateur parie.
        equipe : str
            Le nom de l'équipe sur laquelle l'utilisateur parie.

        """

        pseudo = Session().utilisateur.nom_utilisateur
        t=ParisDao().ajouter_paris(tournoi, equipe,pseudo)
        print(f"Vous avez parié sur {equipe} dans le tournoi {tournoi}.")

    def terminer_paris(pari, gagnant):
        """
        Détermine le résultat d'un pari après la fin du match. Met à jour le statut du pari en fonction du gagnant.

        Parameters
        ----------
        pari : Pari
            Le pari à évaluer, de type Pari.
        gagnant : str
            Le nom de l'équipe gagnante du match.
        """
        if not isinstance(pari, Pari):
            raise TypeError("Le pari doit être de type Pari")
        if pari.pari == gagnant:
            pari.statut = "Remporté"
        else:
            pari.statut = "Perdu"
        ParisDao().changer_statut(pari.statut)

    def supprimer_paris(pari):
        """
        Supprime un pari de l'utilisateur dans la base de données.

        Parameters
        ----------
        pari : Pari
            Le pari à supprimer, de type Pari.
        """
        if not isinstance(pari, Pari):
            raise TypeError("Le pari doit être de type Pari")
        ParisDao().supprimer_paris(pari)


    def voir_paris(self):
        """
        Récupère et affiche les paris effectués par l'utilisateur.

        Return
        ------
        p : list
            Liste des paris effectués par l'utilisateur
        """
        pseudo = Session().utilisateur.nom_utilisateur
        p=ParisDao().lister_tous_paris_utilisateur(pseudo)
        return p
