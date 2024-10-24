from InquirerPy import inquirer

from utils.reset_database import ResetDatabase

from view.vue_abstraite import VueAbstraite
from view.session import Session


class AccueilVue(VueAbstraite):
    """Vue d'accueil de l'application"""

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Se connecter",
                "Créer un compte",
                "Consulter les statistiques de match",
                "Consulter les statistiques de joueur/équipe",
                "Consulter le calendrier"
                "Ré-initialiser la base de données",
                "Infos de session",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                exit()

            case "Se connecter":
                from view.accueil.connexion_vue import ConnexionVue

                return ConnexionVue("Connexion à l'application")

            case "Créer un compte":
                from view.accueil.inscription_vue import InscriptionVue

                return InscriptionVue("Création de compte utilisateur")

            case "Consulter les statistiques de match":
                from view.accueil.inscription_vue import InscriptionVue

                return InscriptionVue("Création de compte utilisateur")

            case "Consulter les statistiques de joueur/équipe":
                from view.accueil.inscription_vue import InscriptionVue

                return InscriptionVue("Création de compte utilisateur")

            case "Consulter le calendrier":
                from view.accueil.inscription_vue import InscriptionVue

                return InscriptionVue("Création de compte utilisateur")

            case "Infos de session":
                return AccueilVue(Session().afficher())

            case "Ré-initialiser la base de données":
                succes = ResetDatabase().lancer()
                message = (
                    f"Ré-initilisation de la base de données - {'SUCCES' if succes else 'ECHEC'}"
                )
                return AccueilVue(message)
