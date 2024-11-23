from service.paris_service import ParisService
from InquirerPy import inquirer
from dao.paris_dao import ParisDao
from prettytable import PrettyTable
from view.vue_abstraite import VueAbstraite

class PariVue(VueAbstraite):
    """Une vue pour afficher les paris d'un utilisateur"""

    def __init__(self, message=""):
        self.message = message
        self.paris = ParisService()

    def message_info(self):
        print("Paris de l'utilisateur")

    def choisir_menu(self):
        """Choix du menu suivant"""
        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        while True:
            choix = inquirer.select(
                message="Souhaitez-vous faire un nouveau pari ?",
                choices=[
                    "Parier sur un nouveau match",
                    "Retour",
                    "Voir tous les paris",
                ],
            ).execute()

            match choix:
                case "Parier sur un nouveau match":
                    # Demander à l'utilisateur de choisir un tournoi parmi les disponibles
                    tournaments = ParisDao().get_available_tournaments()  # Méthode qui récupère les tournois disponibles

                    choix_tournoi = inquirer.select(
                        message="Quel tournoi voulez-vous choisir ?",
                        choices=tournaments,
                    ).execute()

                    # Récupérer les équipes disponibles pour le tournoi choisi
                    available_teams = ParisDao().get_teams_for_tournament(choix_tournoi)  # Méthode qui récupère les équipes disponibles pour ce tournoi

                    choix_match = inquirer.select(
                        message="Quel match souhaitez-vous parier ?",
                        choices=available_teams,
                    ).execute()

                    sep = " vs "
                    cleaned_match = choix_match.strip().split(sep)  # Diviser la chaîne par " vs "

                    # Extraire les noms des équipes
                    equipe1 = cleaned_match[0].split()[-1]  # Dernier mot avant "vs"
                    equipe2 = cleaned_match[1].split()[0]
                    choix_equipe = inquirer.select(
                        message="Quelle équipe/joueur souhaitez-vous parier ?",
                        choices=[equipe1, equipe2],
                    ).execute()

                    # Effectuer le pari avec le tournoi et l'équipe choisis
                    self.paris.parier(choix_tournoi, choix_equipe)

                case "Retour":
                    # L'utilisateur a choisi "Retour", on revient à la vue d'accueil
                    from view.accueil.accueil_vue import AccueilVue
                    return AccueilVue()

                case "Voir tous les paris":
                    # L'utilisateur a choisi "Voir tous les paris", on affiche les paris possibles
                    print("Tentative d'affichage des paris...")  # Message avant le try pour confirmer l'exécution du code

                    try:
                        # Récupération des paris effectués
                        paris_effectué = self.paris.voir_paris()
                        # Si aucune donnée n'est récupérée
                        if not paris_effectué:
                            print("Aucun pari trouvé.")  # Ajout d'un message pour le cas où aucun pari n'est trouvé

                        else:
                            # Créer une table PrettyTable pour afficher les paris
                            table = PrettyTable()
                            table.field_names = ["Tournoi", "Équipe Pariée", "Équipe Adverse", "Cote","Resultat"]

                            # Ajouter les données de chaque pari dans la table
                            for pari in paris_effectué:

                                tournoi = pari.get("tournoi", "Inconnu")
                                equipe_parier = pari.get("equipe_parier", "Inconnue")
                                equipe_adverse = pari.get("equipe_adverse", "Inconnue")
                                cote = pari.get("cote", "Non définie")
                                win = pari.get("win","Inconnu")
                                if win: res= "Gagnée"
                                else: res= "Perdue"

                                table.add_row([tournoi, equipe_parier, equipe_adverse, cote,res])

                            # Afficher la table
                            print("Paris effectué")
                            print(table)




                        # Retour à l'accueil
                        from view.accueil.accueil_vue import AccueilVue
                        return AccueilVue("Retour à l'accueil")

                    except Exception as e:
                        print(f"Erreur lors de l'affichage des paris : {e}")  # Message en cas d'erreur

        # Retourner à l'accueil ou une autre vue
        from view.accueil.accueil_vue import AccueilVue
        return AccueilVue("Retour à l'accueil")

 