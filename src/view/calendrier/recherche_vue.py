from service.calendrier_evenement import CalendrierEvenement
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer
import datetime


class RechercheVue(VueAbstraite):
    """Une vue pour afficher les statistiques des matchs"""

    def __init__(self, message=""):
        self.message = message
        self.calendrier_evenement = CalendrierEvenement()

    def message_info(self):
        """Affiche un éventuel message informatif"""
        if self.message:
            print(f"Info : {self.message}")

    def valider_date(self):
        """
        Demande une date à l'utilisateur et la valide.

        Returns
        -------
        datetime.date ou None
            La date valide sous forme d'objet datetime.date, ou None si aucune date valide n'est fournie.
        """
        while True:
            date_str = input("À quelle date le match a-t-il eu lieu? (AAAA/MM/JJ) : ")
            try:
                # Convertir l'entrée utilisateur en objet date
                return datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
            except ValueError:
                # Gestion des erreurs pour une date mal formatée
                print("Format invalide. Assurez-vous d'entrer une date au format AAAA/MM/JJ.")
                retry = input("Voulez-vous réessayer ? (o/n) : ").lower()
                if retry != "o":
                    return None

    def choisir_menu(self):
        """
        Choix du menu suivant.

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal.
        """
        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        self.message_info()

        # Recherche du match par date
        date_valide = self.valider_date()
        if date_valide:
            try:
                self.calendrier_evenement.rechercher_match_par_date(date_valide)
            except Exception as e:
                print(f"Une erreur s'est produite lors de la recherche : {e}")
        else:
            print("Aucune date valide fournie, retour au menu principal.")

        # Menu des choix
        choix = inquirer.select(
            message="Que souhaitez-vous faire ?",
            choices=[
                "Afficher le calendrier",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue
                return AccueilVue()

            case "Afficher le calendrier":
                from view.calendrier.calendrier_even_vue import EvenementVue
                return EvenementVue()
