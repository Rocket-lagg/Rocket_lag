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
                        "INSERT INTO match(id_match, equipe1, equipe2, score1, score2, date, region, ligue, perso) VALUES        "
                        "(%(id_match)s, %(equipe1)s, %(equipe2)s, %(score1)s, %(score2)s, %(date)s, %(region)s, %(ligue)s, %(perso)s)             "
                        "  RETURNING id_match;                                                ",
                        {
                            "id_match": match.id_match,
                            "equipe1": match.equipe1,
                            "equipe2": match.equipe2,
                            "score1": match.score1,
                            "score2": match.score2,
                            "date": match.date,
                            "region": match.region,
                            "ligue": match.ligue,
                            "perso": match.perso

                        },
                    )

                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            match.id_match = res["id_match"]
            created = True

        return created

    @log
    def trouver_par_id(self, id_match) -> Match:
        """trouver un match grace à son id

        Parameters
        ----------
        id_match : int
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
                        "  FROM match                      "
                        " WHERE id_match = %(id_match)s;  ",
                        {"id_match": id_match},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        match = None
        if res:
            match = Match(
                id_match = res["id_match"],
                equipe1 = res["equipe1"],
                equipe2 = res["equipe2"],
                score1 = res["score1"],
                score2 = res["score2"],
                date = res["date"],
                region = res["region"],
                ligue = res["ligue"],
                perso = res["perso"],
            )

        return match


    @log
    def trouver_par_date(self, id_date) -> Match:
        """trouver un match grace à sa date

        Parameters
        ----------
        date : DATE
            date du match que l'on souhaite trouver

        Returns
        -------
        liste_matchs : list[Match]
            renvoie la liste de tous les matchs à la date donnée
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM match                      "
                        " WHERE date::DATE = %(date)s             "
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
                    id_match = res["id_match"],
                    equipe1 = res["equipe1"],
                    equipe2 = res["equipe2"],
                    score1 = res["score1"],
                    score2 = res["score2"],
                    date = res["date"],
                    region = res["region"],
                    ligue = res["ligue"],
                    perso = res["perso"],
                )

                liste_matchs.append(match)

        return liste_matchs

    @log
    def trouver_id_match_par_equipe(self, equipe) ->List[str]:
        """trouver l'id de match grâce au nom d'une équipe

        Parameters
        ----------
        equipe : str
            nom unique d'une équipe

        Returns
        -------
        list_id_match : List[id_match: str]
            renvoie une liste des id des matchs qu'a fait l'équipe
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_match                           "
                        " FROM equipe                      "
                        " WHERE equipe_nom = %(equipe)s;  ",
                        {"equipe": equipe},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        list_id_match = None
        if res:
            for row in res:
                list_id_match.append(row['id_match'])


        return list_id_match

    @log
    def trouver_id_match_par_joueur(self, joueur) ->List[str]:
        """trouver l'id de match grâce au nom d'un joueur

        Parameters
        ----------
        joueur : str
            nom unique d'une équipe

        Returns
        -------
        list_id_match : List[id_match: str]
            renvoie une liste des id des matchs qu'a fait l'équipe
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_match                           "
                        " FROM joueur                     "
                        " WHERE joueur_nom = %(joueur)s;  ",
                        {"joueur": joueur},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        list_id_match = None
        if res:
            for row in res:
                list_id_match.append(row['id_match'])


        return list_id_match

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
                    id_match = res["id_match"],
                    equipe1 = res["equipe1"],
                    equipe2 = res["equipe2"],
                    score1 = res["score1"],
                    score2 = res["score2"],
                    date = res["date"],
                    region = res["region"],
                    ligue = res["ligue"],
                    perso = res["perso"],
                )

                liste_matchs.append(match)

        return liste_matchs
