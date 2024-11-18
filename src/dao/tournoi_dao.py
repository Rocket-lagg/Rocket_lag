import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.Tournoi import Tournoi


class TournoiDao(metaclass=Singleton):

    @log
    def creer_tournoi(self, nom_utilisateur, id_tournois, nom_tournois, type_tournoi) -> bool:
        """Creation d'un tournoi dans la base de données"""

        res = None
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête d'insertion SQL avec RETURNING pour récupérer l'ID
                    cursor.execute(
                        """
                        INSERT INTO Tournoi (id_tournoi, nom_createur, nom, officiel, type_tournoi)
                        VALUES (%(id_tournois)s, %(nom_utilisateur)s, %(nom_tournoi)s, %(officiel)s, %(type_tournoi)s);
                        """,
                        {
                            "id_tournoi": id_tournois,
                            "nom_createur": nom_utilisateur,
                            "nom": nom_tournois,
                            "officiel": 0,
                            "type_tournoi": type_tournoi,
                        },
                    )
                    # Récupérer l'ID du joueur créé
                    res = cursor.fetchone()
            return res is not None
        except Exception as e:
            logging.error(f"Erreur lors de la création du tournois : {e}")
            return False

    def recuperer_equipe(self, id_tournoi):
        res = None
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT nom_equipe
                        FROM equipe_tournoi
                        WHERE id_tournoi = %(id_tournoi)s
                        """,
                        {
                            "id_tournoi": id_tournoi,
                        },
                    )
                    res = cursor.fetchall()
                    if not res:
                        return []
                    liste_equipe = []
                    for element in res:
                        liste_equipe.append(element["nom_equipe"])
                    return liste_equipe

        except Exception as e:
            logging.error(f"Erreur lors de la récupération des équipes : {e}")
            return False

    def ajouter_score(self, score1, score2, match_id):
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête d'insertion SQL avec RETURNING pour récupérer l'ID
                    cursor.execute(
                        """
                            INSERT INTO match_tournoi (score1, score2)
                            VALUES (%(score1)s, %(score2)s)
                            WHERE id_match = %(id_match))s;
                            """,
                        {"score1": score1, "score2": score2, "id_match": match_id},
                    )
        except Exception as e:
            logging.error(f"Erreur lors de la création des équipes : {e}")
            return False

    def creer_equipe(self, id_tournoi, nom_equipe):
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête d'insertion SQL avec RETURNING pour récupérer l'ID
                    cursor.execute(
                        """
                            INSERT INTO equipe_tournoi (id_tournoi, nom_equipe)
                            VALUES (%(id_tournoi)s, %(nom_equipe)s);
                            """,
                        {
                            "id_tournoi": id_tournoi,
                            "nom_equipe": nom_equipe,
                        },
                    )
        except Exception as e:
            logging.error(f"Erreur lors de la création des équipes : {e}")
            return False

    def creer_match(self, id_tournoi, equipe1, equipe2):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                            INSERT INTO match_tournoi (id_tournoi, equipe1, equipe2)
                            VALUES (%(id_tournoi)s, %(equipe1)s, %(equipe2)s);
                            """,
                        {
                            "id_tournoi": id_tournoi,
                            "equipe1": equipe1,
                            "equipe2": equipe2,
                        },
                    )
        except Exception as e:
            logging.error(f"Erreur lors de la création des matchs : {e}")
            return False

    def trouver_matchs_par_tournoi(self, id_tournoi):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                            SELECT (id_match, equipe1, equipe2)
                            FROM match_tournoi
                            WHERE id_tournoi = %(id_tournoi)s
                            """,
                        {
                            "id_tournoi": id_tournoi,
                        },
                    )
                    res = cursor.fetchall()
                    if res:
                        if isinstance(res, list):
                            liste = []
                            for r in res:
                                liste.append([r["id_match"], r["equipe1"], r["equipe2"]])
                            return liste
                        else:
                            return [res["id_match"], res["equipe1"], res["equipe2"]]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Erreur lors de la création des matchs : {e}")
            return False
