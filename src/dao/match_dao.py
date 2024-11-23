import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.Match import Match


class MatchDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux matchs de la base de données"""

    @log
    def creer(self, match) -> bool:
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO match(
                            match_id, equipe1, equipe2, score1, score2, date, region, stage, ligue, perso, cote_equipe1, cote_equipe2
                        )
                        VALUES (
                            %(match_id)s, %(equipe1)s, %(equipe2)s, %(score1)s, %(score2)s, %(date)s, %(region)s, %(stage)s, %(ligue)s, %(perso)s, %(cote_equipe1)s, %(cote_equipe2)s
                        )
                        RETURNING match_id;
                        """,
                        {
                            "match_id": match.match_id,
                            "equipe1": match.equipe1,
                            "equipe2": match.equipe2,
                            "score1": match.score1,
                            "score2": match.score2,
                            "date": match.date,
                            "region": match.region,
                            "stage": match.stage,
                            "ligue": match.ligue,
                            "perso": bool(match.perso),  # Forcer le type bool
                            "cote_equipe1": match.cote_equipe1,
                            "cote_equipe2": match.cote_equipe2,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la création du match : {e}")

        created = False
        if res:
            match.match_id = res["match_id"]
            created = True

        return created

    @log
    def trouver_par_match_id(self, match_id):
        """Trouver un match par son match_id"""
        res_match = None  # Initialiser la variable avant l'exécution
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:  # Le curseur est automatiquement fermé après le bloc
                    cursor.execute(
                        """
                        SELECT *
                        FROM Match
                        WHERE match_id = %(match_id)s;
                        """,
                        {"match_id": match_id},
                    )
                    res_match = cursor.fetchone()  # Assurez-vous de récupérer la donnée ici
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du match : {e}")
            raise

        # Assurez-vous que res_match est défini avant de l'utiliser
        match = None
        if res_match:
            match = Match(
                match_id=res_match["match_id"],
                equipe1=res_match["equipe1"],
                equipe2=res_match["equipe2"],
                score1=res_match["score1"],
                score2=res_match["score2"],
                date=res_match["date"],
                region=res_match["region"],
                ligue=res_match["ligue"],
                perso=res_match["perso"],
                stage=res_match["stage"],
            )

        return match

    def trouver_par_dates(self, date) -> Match:
        """trouver un match grace à sa dates

        Parameters
        ----------
        date : datetime
            date du match que l'on souhaite trouver

        Returns
        -------
        liste_matchs : list[Match]
            renvoie la liste de tous les matchs à la dates donnée
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM match                      "
                        " WHERE date::date = %(date)s             "
                        " AND perso = FALSE;  ",
                        {"date": date},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        match = None
        liste_matchs = []

        if res:
            for row in res:
                match = Match(
                    match_id=row["match_id"],
                    equipe1=row["equipe1"],
                    equipe2=row["equipe2"],
                    score1=row["score1"],
                    score2=row["score2"],
                    date=row["date"],
                    region=row["region"],
                    ligue=row["ligue"],
                    perso=row["perso"],
                    stage=row["stage"],
                )

                liste_matchs.append(match)

        return liste_matchs

    @log
    def trouver_match_id_par_equipe(self, equipe) -> list[str]:
        """Trouver l'ID des matchs grâce au nom d'une équipe.

        Parameters
        ----------
        equipe : str
            Nom unique d'une équipe.

        Returns
        -------
        list_match_id : List[str]
            Renvoie une liste des IDs des matchs qu'a faits l'équipe.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT*
                        FROM match
                        WHERE equipe1 = %(equipe)s OR equipe2 = %(equipe)s;
                        """,
                        {"equipe": equipe},  # Utilisation d'un dictionnaire de paramètres
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_matchs = []

        if res:
            for row in res:
                match = Match(
                    match_id=row["match_id"],
                    equipe1=row["equipe1"],
                    equipe2=row["equipe2"],
                    score1=row["score1"],
                    score2=row["score2"],
                    date=row["date"],
                    region=row["region"],
                    ligue=row["ligue"],
                    perso=row["perso"],
                    stage=row["stage"],
                )

                liste_matchs.append(match)

        return liste_matchs

    @log
    def trouver_match_id_par_joueur(self, joueur) -> list[str]:
        """trouver l'id de match grâce au nom d'un joueur

        Parameters
        ----------
        joueur : str
            nom unique d'une équipe

        Returns
        -------
        list_match_id : List[match_id: str]
            renvoie une liste des id des matchs qu'a fait l'équipe
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT*
                        FROM match JOIN Joueur ON Joueur.match_id = match.match_id
                        WHERE Joueur.nom =  %(joueur)s;
                        """,
                        {"joueur": joueur},  # Utilisation d'un dictionnaire de paramètres
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_matchs = []

        if res:
            for row in res:
                match = Match(
                    match_id=row["match_id"],
                    equipe1=row["equipe1"],
                    equipe2=row["equipe2"],
                    score1=row["score1"],
                    score2=row["score2"],
                    date=row["date"],
                    region=row["region"],
                    ligue=row["ligue"],
                    perso=row["perso"],
                    stage=row["stage"],
                )

                liste_matchs.append(match)

        return liste_matchs

    @log
    def lister_tous(self) -> list[Match]:
        """lister tous les matchs

        Parameters
        ----------
        None

        Returns
        -------
        liste_matchs : list[Match]
            renvoie la liste de tous les matchs dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM match;                        "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_matchs = []

        if res:
            for row in res:
                match = Match(
                    match_id=row["match_id"],
                    equipe1=row["equipe1"],
                    equipe2=row["equipe2"],
                    score1=row["score1"],
                    score2=row["score2"],
                    date=row["date"],
                    region=row["region"],
                    ligue=row["ligue"],
                    stage=row["stage"],
                    perso=row["perso"],
                )

                liste_matchs.append(match)

        return liste_matchs

    def trouver_match_id_et_joueur(self, joueur, match_id) -> Match:
        """Trouver un match grâce au nom d'un joueur et à l'ID du match.

        Parameters
        ----------
        joueur : str
            Nom unique du joueur.
        match_id : str
            L'ID du match.

        Returns
        -------
        Match :
            Objet Match correspondant au joueur et au match.
            Retourne None si aucun résultat n'est trouvé.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM match
                        JOIN Joueur ON Joueur.match_id = match.match_id
                        WHERE Joueur.nom = %(joueur)s AND Joueur.match_id = %(match_id)s;
                        """,
                        {
                            "joueur": joueur,
                            "match_id": match_id,
                        },
                    )
                    row = cursor.fetchone()  # Récupérer un seul résultat
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du match pour le joueur {joueur}: {e}")
            raise

        if row:
            # Construire le dictionnaire Match à partir des données de la ligne
            match = {
                "match_id": row["match_id"],
                "equipe1": row["equipe1"],
                "equipe2": row["equipe2"],
                "score1": row["score1"],
                "score2": row["score2"],
                "cote_equipe2": row["cote_equipe2"],
                "cote_equipe1": row["cote_equipe1"],
                "date": row["date"],
                "region": row["region"],
                "ligue": row["ligue"],
                "perso": row["perso"],
                "stage": row["stage"],
                "nom": row["nom"],
                "nationalite": row["nationalite"],
                "rating": row["rating"],
                "shots": row["shots"],
                "goals": row["goals"],
                "saves": row["saves"],
                "assists": row["assists"],
                "score": row["score"],
                "shooting_percentage": row["shooting_percentage"],
                "time_offensive_third": row["time_offensive_third"],
                "time_defensive_third": row["time_defensive_third"],
                "time_neutral_third": row["time_neutral_third"],
                "demo_inflige": row["demo_inflige"],
                "demo_recu": row["demo_recu"],
                "goal_participation": row["goal_participation"],
                "indice_offensif": row["indice_offensif"],
                "indice_performance": row["indice_performance"],
            }
            return match
        else:
            return None

    def trouver_match_id_et_equipe(self, equipe, match_id) -> Match:
        """Trouver un match grâce au nom d'un joueur et à l'ID du match.

        Parameters
        ----------
        equipe : str
            Nom unique de l'équipe.
        match_id : str
            L'ID du match.

        Returns
        -------
        Match :
            Objet Match correspondant à l'équipe et au match.
            Retourne None si aucun résultat n'est trouvé.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM match
                        JOIN Equipe ON Equipe.match_id = match.match_id
                        WHERE equipe1 = %(equipe)s OR equipe2 = %(equipe)s
						AND Equipe.match_id = %(match_id)s
						AND Equipe.equipe_nom = %(equipe)s;
                        """,
                        {
                            "equipe": equipe,
                            "match_id": match_id,
                        },
                    )
                    row = cursor.fetchone()  # Récupérer un seul résultat
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du match pour le joueur {joueur}: {e}")
            raise

        if row:
            # Construire le dictionnaire Match à partir des données de la ligne
            match = {
                "match_id": row["match_id"],
                "equipe1": row["equipe1"],
                "equipe2": row["equipe2"],
                "score1": row["score1"],
                "score2": row["score2"],
                "cote_equipe2": row["cote_equipe2"],
                "cote_equipe1": row["cote_equipe1"],
                "date": row["date"],
                "region": row["region"],
                "ligue": row["ligue"],
                "perso": row["perso"],
                "stage": row["stage"],
                "equipe_nom": row["equipe_nom"],
                "equipe_score": row["equipe_score"],
                "boost_stole": row["boost_stole"],
                "shots": row["shots"],
                "goals": row["goals"],
                "saves": row["saves"],
                "assists": row["assists"],
                "score": row["score"],
                "shooting_percentage": row["shooting_percentage"],
                "time_offensive_third": row["time_offensive_third"],
                "time_defensive_third": row["time_defensive_third"],
                "time_neutral_third": row["time_neutral_third"],
                "demo_inflige": row["demo_inflige"],
                "demo_recu": row["demo_recu"],
                "indice_de_pression": row["indice_de_pression"],
                "indice_performance": row["indice_performance"],
            }
            return match
        else:
            return None


    def delete_match(match_id):
        """
        Supprimer un match dans la table `Match` en fonction de son match_id.

        Parameters
        ----------
        match_id : str
            L'ID du match à supprimer.

        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM Match
                        WHERE match_id = %(match_id)s;
                        """,
                        {"match_id": match_id},
                    )
                    connection.commit()
                    logging.info(f"Match avec match_id={match_id} supprimé avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du match : {e}")
            raise



    def add_match(match_details):
        """
        Ajouter un match dans la table Match.

        Parameters
        ----------
        match_details : Dictionnaire
            Un dictionnaire contenant les informations du match à insérer.

        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO Match (tournoi, equipe1, equipe2, date, cote_equipe1, cote_equipe2)
                        VALUES (%(tournoi)s, %(equipe1)s, %(equipe2)s, %(date)s, %(cote_equipe1)s, %(cote_equipe2)s);
                        """,
                        match_details
                    )
                    connection.commit()
                    logging.info("Match ajouté avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout d'un match : {e}")
            raise
