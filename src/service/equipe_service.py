from business_object.Equipe import Equipe


class EquipeService:

    def instancier(self, equipe_bdd):
        """
        Crée une instance de l'objet Equipe à partir des données récupérées de la base de données.

        Parameters
        ----------
        equipe_bdd : dict
            Un dictionnaire contenant les informations de l'équipe à instancier. Les clés du dictionnaire doivent inclure :

        Return
        ------
        equipe : Equipe
            Une instance de la classe Equipe initialisée avec les données fournies dans le dictionnaire equipe_bdd.
        """
        equipe = Equipe(
            nom_equipe=equipe_bdd["nom_equipe"],
            shots=equipe_bdd["shots"],
            goals=equipe_bdd["goals"],
            saves=equipe_bdd["saves"],
            assists=equipe_bdd["assists"],
            score=equipe_bdd["scores"],
            shooting_percentage=equipe_bdd["shooting_percentage"],
        )
        return equipe
