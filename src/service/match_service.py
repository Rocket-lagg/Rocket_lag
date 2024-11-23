from business_object.Match import Match


class MatchService:

    def instancier(self, match_bdd):
        """
        Crée une instance de l'objet Match à partir des données récupérées de la base de données.

        Parameters
        ----------
        match_bdd : dict
            Un dictionnaire contenant les informations du match à instancier. Les clés du dictionnaire doivent inclure :

        Return
        ------
        match : Match
            Une instance de la classe Match initialisée avec les données fournies dans le dictionnaire match_bdd.
        """
        match = Match(
            match_id=match_bdd["match_id"],
            equipe_bleue=match_bdd["equipe_bleue"],
            equipe_orange=match_bdd["equipe_orange"],
            score_bleu=match_bdd["score_bleu"],
            score_orange=match_bdd["score_orange"],
            date=match_bdd["date"],
            region=match_bdd["region"],
            ligue=match_bdd["ligue"],
            event=match_bdd["event"],
            perso=match_bdd["perso"],
        )
        return match
