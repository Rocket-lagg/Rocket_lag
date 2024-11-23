import uuid
from view.vue_abstraite import VueAbstraite
from dao.match_dao import MatchDao

class AjouterMatchVue(VueAbstraite):
    """Vue pour ajouter un match."""

    def __init__(self, message):
        self.message = message

    def afficher(self):
        print("\n" + "-" * 50 + f"\n{self.message}\n" + "-" * 50 + "\n")

        try:
            # Collecter les informations du match auprès de l'utilisateur

            equipe1 = input("Nom de l'équipe 1 : ")
            equipe2 = input("Nom de l'équipe 2 : ")
            score1 = int(input("Score de l'équipe 1 : "))
            score2 = int(input("Score de l'équipe 2 : "))
            cote_equipe1 = float(input("Cote de l'équipe 1 : "))
            cote_equipe2 = float(input("Cote de l'équipe 2 : "))
            date = input("Date du match (format AAAA-MM-JJ HH:MM:SS) : ")
            perso = bool(input("Match perso True ou false? : "))
            region = input("region :")
            stage = input("stage du tournoi (play-offs ou poules):")
            ligue = input("ligue :")


            match_id = str(uuid.uuid4())  # Génère un UUID et le convertit en chaîne de caractères

            # Construire le dictionnaire du match avec l'ID unique
            match = {
                "match_id": match_id,
                "equipe1": equipe1,
                "equipe2": equipe2,
                "date": date,
                "score1" :score1,
                "score2" :score2,
                "region":region,
                "stage":stage,
                "ligue":ligue,
                "perso":perso,
                "cote_equipe1": cote_equipe1,
                "cote_equipe2": cote_equipe2
            }

            # Appeler la méthode DAO pour ajouter le match
            MatchDao().add_match(match)
            print(f"Le match {equipe1} vs {equipe2} a été ajouté avec succès.")

        except Exception as e:
            print(f"Erreur lors de l'ajout du match : {e}")

        # Retourner à l'accueil ou une autre vue
        from view.accueil.accueil_vue import AccueilVue
        return AccueilVue("Retour à l'accueil")

    def message_info(self):
        """Affiche un message ou reste vide."""
        print("Ajout d'un match : Fournissez les informations demandées.")


    def choisir_menu(self):
        """Retourne à l'accueil après l'opération."""
        from view.accueil.accueil_vue import AccueilVue
        return AccueilVue("Retour à l'accueil")
