from dao.match_dao import MatchDao
from view.vue_abstraite import VueAbstraite


class SupprimerMatchVue(VueAbstraite):
    """Vue pour supprimer un match."""

    def __init__(self, message):
        self.message = message

    def afficher(self):
        print("\n" + "-" * 50 + f"\n{self.message}\n" + "-" * 50 + "\n")

        try:
            # Demander à l'utilisateur l'identifiant du match à supprimer
            id_match = input("ID du match à supprimer : ")

            MatchDao().delete_match(id_match)
            print(f"Le match avec l'ID {id_match} a été supprimé avec succès.")

        except Exception as e:
            print(f"Erreur lors de la suppression du match : {e}")

        # Retourner à l'accueil ou une autre vue
        from view.accueil.accueil_vue import AccueilVue
        return AccueilVue("Retour à l'accueil")

    def message_info(self):
        """Affiche un message ou reste vide."""
        print("Suppression d'un match : Fournissez les informations demandées.")

    def choisir_menu(self):
        """Retourne à l'accueil après l'opération."""
        from view.accueil.accueil_vue import AccueilVue
        return AccueilVue("Retour à l'accueil")
