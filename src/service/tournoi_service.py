from view.session import Session
from dao.tournoi_dao import TournoiDao
from business_object.Tournoi import Tournoi
from dao.utilisateur_dao import UtilisateurDao
from dao.equipe_dao import EquipeDao
from dao.match_dao import MatchDao
from service.equipe_service import EquipeService
from service.match_service import MatchService


class TournoiService:

    def __init__(self):
        self.utilisateur_dao = UtilisateurDao()
        self.equipe_dao = EquipeDao()
        self.match_dao = MatchDao()

    def instancier_tournoi(self, tournois_bdd):
        equipe_service = EquipeService()
        match_service = MatchService()
        matchs = self.match_dao.trouver_par_id_tournoi(tournois_bdd["id_tournoi"])
        equipes = []
        for match in matchs:
            equipe = self.equipe_dao.trouver_par_id_match(match['match_id']) # A coder
            for i in equipe:
                equipes.append(i)
                
        equipe_service.instancier(equipe)
        match_service.instancier(match)
        tournoi = Tournoi(
            nom_tournoi=tournois_bdd["nom_tournoi"],
            createur = tournois_bdd['createur'],
            equipes = equipe,
            matchs = matchs,
            officiel=tournois_bdd["officiel"]
        )
        return tournoi

    def afficher_infos_tournois(self):
        "Affiche les tournois d'un utilisateur"
        nom_utilisateur = Session().utilisateur.nom_utilisateur
        tournois = tournoisDao().afficher_infos_tournois(nom_utilisateur)
        if tournois == []:
            print(f"{nom_utilisateur}, vous n'avez pas fait de tournois")
        else:
            liste_tournois = []
            for tournoi in tournois:
                liste_tournois.append(self.instancier_tournois(tournoi))
            print(liste_tournois)
        return liste_tournois


    def supprimer_paris(pari):
        "Supprime un pari"
        if not isinstance(pari, Pari):
            raise TypeError("Le pari doit être de type Pari")
        ParisDao().supprimer_paris(pari)

    def ajouter_equipes(self, liste_equipes):
        for equipe in liste_equipes:
            self.equipes.append(equipe)
            self.enregistrer_equipe_bdd(equipe)
        print(f"Équipes ajoutées au tournoi {self.nom_tournoi}.")

    def inscrire_equipe(self, equipe):
        if self.officiel:
            print(f"Équipe {equipe.nom} inscrite dans un tournoi officiel.")
            self.enregistrer_tournoi(self.nom_tournoi, True)
        else:
            print(f"Équipe {equipe.nom} inscrite dans un tournoi personnel.")
            self.enregistrer_tournoi(self.nom_tournoi, False)

        self.equipes.append(equipe)

    def enregistrer_tournoi(self, nom_tournoi, officiel):
        print(f"Tournoi {nom_tournoi} enregistré avec officiel={officiel}.")

    def suivre_resultats(self, equipe1, equipe2, score1, score2):
        if equipe1 not in self.equipes or equipe2 not in self.equipes:
            print("Les équipes doivent être inscrites au tournoi.")
            return

        gagnant = equipe1 if score1 > score2 else equipe2
        match = {
            'equipe1': equipe1.nom,
            'score1': score1,
            'equipe2': equipe2.nom,
            'score2': score2,
            'gagnant': gagnant.nom
        }
        self.matchs.append(match)
        print(f"Match joué: {equipe1.nom} {score1} - {equipe2.nom} {score2}. Gagnant: {gagnant.nom}")
        return gagnant

    def afficher_classement(self):
        classement = {equipe.nom: 0 for equipe in self.equipes}
        for match in self.matchs:
            classement[match['gagnant']] += 1

        classement_trie = sorted(classement.items(), key=lambda x: x[1], reverse=True)
        print("\nClassement final :")
        for rang, (equipe_nom, victoires) in enumerate(classement_trie):
            print(f"{rang + 1}. {equipe_nom} - {victoires} victoires")

        return classement_trie

    def gagnant_tournoi(self):
        classement = self.afficher_classement()

        if classement:
            gagnant_final = classement[0][0]
            print(f"\nLe gagnant du tournoi {self.nom_tournoi} est : {gagnant_final}")
            return gagnant_final
        else:
            print("Aucune équipe n'a participé au tournoi.")
            return None
