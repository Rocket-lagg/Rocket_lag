from service.calendrier_evenement import CalendrierEvenement
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer
import logging


class EvenementVue(VueAbstraite):
    """Une vue pour afficher les statistiques des matchs"""

    def __init__(self, message=""):
        self.message = message
        self.calendrier_evenement = CalendrierEvenement()

    def message_info(self):
        print("Calendrier des matchs futurs")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")
        try:
            annee = int(input("Quel année?:"))
            mois = int(input("Quel mois (en chiffre)?"))

            # Vérifications des entrées
            if not isinstance(annee, int):
                raise TypeError("L'année doit être un entier.")
            if not isinstance(mois, int) or not (1 <= mois <= 12):
                raise ValueError("Le mois doit être un entier entre 1 et 12.")

            self.calendrier_evenement.afficher_calendrier_annee(annee, mois)

        except ValueError as ve:
            logging.error(f"Entrée invalide : {ve}")
            print("Erreur : Veuillez rentrer des chiffres adéquats en entrée")
        except TypeError as te:
            logging.error(f"Type incorrect : {te}")
            print("Erreur : Veuillez rentrer des chiffres en entrée")
        except Exception as e:
            # Gestion générique des autres erreurs
            logging.error(f"Une erreur s'est produite : {e}")
            print(f"Une erreur inattendue est survenue : {e}")

        choix = inquirer.select(
            message="",
            choices=[
                "Chercher un match spécifique",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Chercher un match spécifique":
                from view.calendrier.recherche_vue import RechercheVue

                return RechercheVue()
