from InquirerPy import inquirer
from utils.reset_database import ResetDatabase
from view.vue_abstraite import VueAbstraite
from view.session import Session
import dotenv
import os

class AccueilVue(VueAbstraite):
    """Vue d'accueil de l'application"""

    def message_info(self):
        with open("src/graphical_asset/nom.txt", "r", encoding="utf-8") as asset:
            print(asset.read())

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")
        dotenv.load_dotenv()
        LIST_ADMIN = os.environ["LIST_ADMIN"]  # Exemple de liste des administrateurs

        utilisateur = Session().utilisateur  # Récupérer l'utilisateur actuel
        is_admin = utilisateur and utilisateur.nom_utilisateur in LIST_ADMIN

        if utilisateur:
            # Options de base
            choices = [
                "Consulter les statistiques de match",
                "Consulter les statistiques de joueur/équipe",
                "Consulter le calendrier",
                "Parier",
                "Gestion des tournois",
                "Infos de session",
                "Se déconnecter",
                "Quitter",
            ]

            # Ajouter des options si l'utilisateur est un administrateur
            if is_admin:
                choices.extend(["Ajouter un match", "Supprimer un match"])

        else:
            # Options pour les utilisateurs non connectés
            choices = [
                "Se connecter",
                "Créer un compte",
                "Consulter les statistiques de match",
                "Consulter les statistiques de joueur/équipe",
                "Consulter le calendrier",
                "Infos de session",
                "Quitter",
            ]

        # Afficher le menu avec inquirer
        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=choices,
        ).execute()

        # Gérer le choix
        match choix:
            case "Quitter":
                exit()

            case "Se connecter":
                from view.accueil.connexion_vue import ConnexionVue
                return ConnexionVue("Connexion à l'application")

            case "Créer un compte":
                from view.accueil.inscription_vue import InscriptionVue
                return InscriptionVue("Création de compte utilisateur")

            case "Consulter les statistiques de joueur/équipe":
                from view.statistique.stat_vue import VueConsulterStats
                return VueConsulterStats("Consulter les statistiques de joueur/équipe")

            case "Consulter les statistiques de match":
                from view.statistique.match_vue import MatchVue
                return MatchVue("Consultation des statistiques de match")

            case "Consulter le calendrier":
                from view.calendrier.calendrier_vue import CalendrierVue
                return CalendrierVue("")

            case "Gestion des tournois":
                from view.tournoi.tournoi_vue import TournoiVue
                return TournoiVue("")

            case "Parier":
                from view.pari.pari_vue import PariVue
                return PariVue("")

            case "Ajouter un match":
                from view.admin.ajouter_match_vue import AjouterMatchVue
                return AjouterMatchVue("Ajouter un nouveau match")

            case "Supprimer un match":
                from view.admin.supprimer_match_vue import SupprimerMatchVue
                return SupprimerMatchVue("Supprimer un match")

            case "Infos de session":
                return AccueilVue(Session().afficher())
