from service.consulter_stats import ConsulterStats
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class MatchJoueurVue(VueAbstraite):
    """Une vue pour afficher les matchs disponibles en fonction d'un joueur et sélectionner un match"""

    def __init__(self, message=""):
        self.message = message
        self.consulter_stats = ConsulterStats()

    def message_info(self):
        print("Sélectionnez un match après avoir fourni un nom de joueur.")

    def choisir_menu(self):
        """Demander un nom de joueur, obtenir les matchs associés et permettre la sélection d'un match"""

        # Demande à l'utilisateur d'entrer un nom de joueur
        joueur = inquirer.text(message="Entrez le nom du joueur :").execute()

        # Vérifie que le nom du joueur est bien une chaîne de caractères
        if not isinstance(joueur, str):
            raise TypeError("'nom_joueur' doit être une instance de str.")

        # Appel à la méthode qui renvoie un dictionnaire des matchs associés au joueur
        matchs = self.consulter_stats.choix_match(joueur)

        # Si aucun match n'est trouvé, afficher un message et quitter
        if not matchs:
            print("Aucun match trouvé pour ce joueur.")
            return None

        # Création de la liste des choix à afficher dans le menu
        choices = []
        for match_key, match_ids in matchs.items():
            for match_id in match_ids:
                # Ajout des matchs au format lisible avec leur ID
                choices.append(f"{match_key} (ID: {match_id})")

        # Affichage du menu interactif pour choisir un match
        print("\n" + "-" * 50 + "\nSélectionner un match\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message="Sélectionnez un match :",
            choices=choices,
        ).execute()

        # Trouver l'ID du match sélectionné
        match_selected = choices[choices.index(choix)]  # Trouve le match choisi
        match_id = match_selected.split("(ID: ")[-1][:-1]  # Récupérer l'ID du match

        # Afficher l'ID du match sélectionné
        print(f"\nVous avez sélectionné le match : {choix}")
        print(f"L'ID du match sélectionné est : {match_id}")

        # Appel à une fonction pour traiter l'ID du match
        self.traiter_match(match_id)

    def traiter_match(self, match_id):
        # Traitement de l'ID du match, exemple : affichage des détails ou autres actions
        print(f"Traitement du match avec l'ID : {match_id}")
        # Ajoutez ici la logique pour traiter cet ID, comme afficher des statistiques détaillées
