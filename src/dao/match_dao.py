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
                        "INSERT INTO matchs(match_id, equipe1, equipe2, score1, score2, dates, region, ligue, perso) VALUES        "
                        "(%(match_id)s, %(equipe1)s, %(equipe2)s, %(score1)s, %(score2)s, %(dates)s, %(region)s, %(ligue)s, %(perso)s)             "
                        "  RETURNING match_id;                                                ",
                        {
                            "match_id": match.match_id,
                            "equipe1": match.equipe1,
                            "equipe2": match.equipe2,
                            "score1": match.score1,
                            "score2": match.score2,
                            "dates": match.dates,
                            "region": match.region,
                            "ligue": match.ligue,
                            "perso": match.perso,
                        },
                    )

                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            match.match_id = res["match_id"]
            created = True

        return created

    @log
    def trouver_par_id(self, match_id) -> Match:
        """trouver un match grace à son id

        Parameters
        ----------
        match_id : int
            numéro id du match que l'on souhaite trouver

        Returns
        -------
        match : Match
            renvoie le match que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM matchs                      "
                        " WHERE match_id = %(match_id)s;  ",
                        {"match_id": match_id},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        match = None
        if res:
            match = Match(
                match_id=res["match_id"],
                equipe1=res["equipe1"],
                equipe2=res["equipe2"],
                score1=res["score1"],
                score2=res["score2"],
                dates=res["dates"],
                region=res["region"],
                ligue=res["ligue"],
                perso=res["perso"],
            )

        return match

    @log
    def trouver_par_dates(self, dates) -> Match:
        """trouver un match grace à sa dates

        Parameters
        ----------
        dates : dates
            dates du match que l'on souhaite trouver

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
                        "  FROM matchs                      "
                        " WHERE dates = %(dates)s             "
                        " AND perso = FALSE;  ",
                        {"dates": dates},
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
                    match_id=res["match_id"],
                    equipe1=res["equipe1"],
                    equipe2=res["equipe2"],
                    score1=res["score1"],
                    score2=res["score2"],
                    dates=res["dates"],
                    region=res["region"],
                    ligue=res["ligue"],
                    perso=res["perso"],
                )

                liste_matchs.append(match)

        return liste_matchs

    @log
    def trouver_match_id_par_equipe(self, equipe) -> list[str]:
        """trouver l'id de match grâce au nom d'une équipe

        Parameters
        ----------
        equipe : str
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
                        "SELECT match_id                           "
                        " FROM equipe                      "
                        " WHERE equipe_nom = %(equipe)s;  ",
                        {"equipe": equipe},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        list_match_id = None
        if res:
            for row in res:
                list_match_id.append(row["match_id"])

        return list_match_id

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
                        "SELECT match_id                           "
                        " FROM joueur                     "
                        " WHERE joueur_nom = %(joueur)s;  ",
                        {"joueur": joueur},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        list_match_id = None
        if res:
            for row in res:
                list_match_id.append(row["match_id"])

        return list_match_id

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
                        "  FROM matchs;                        "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_matchs = []

        if res:
            for row in res:
                match = Match(
                    match_id=res["match_id"],
                    equipe1=res["equipe1"],
                    equipe2=res["equipe2"],
                    score1=res["score1"],
                    score2=res["score2"],
                    dates=res["dates"],
                    region=res["region"],
                    ligue=res["ligue"],
                    perso=res["perso"],
                )

                liste_matchs.append(match)

        return liste_matchs
