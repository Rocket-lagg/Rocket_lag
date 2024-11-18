import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.Tournoi import Tournoi


class TournoiDao(metaclass=Singleton):

    def creer_tournoi(self, nom_utilisateur, id_tournois, nom_tournois, type_tournoi) -> bool:
        """Création d'un tournoi dans la base de données"""
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête d'insertion SQL avec RETURNING pour récupérer l'ID
                    cursor.execute(
                        """
                        INSERT INTO tournoi (id_tournoi, nom_createur, nom, type_match, officiel)
                        VALUES (%(id_tournoi)s, %(nom_createur)s, %(nom)s, %(type_match)s, %(officiel)s)
                        RETURNING id_tournoi;
                        """,
                        {
                            "id_tournoi": id_tournois,
                            "nom_createur": nom_utilisateur,
                            "nom": nom_tournois,
                            "type_match": type_tournoi,
                            "officiel": False,  # Utiliser un booléen natif
                        },
                    )
                    # Récupérer l'ID du tournoi créé
                    res = cursor.fetchone()
                    connection.commit()  # Important pour valider les changements
            return res is not None
        except Exception as e:
            logging.error(f"Erreur lors de la création du tournoi : {e}")
            return False

    def recuperer_tournois_par_utilisateur(self, nom_createur):
        res = None
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM tournoi
                        WHERE nom_createur = %(nom_createur)s
                        """,
                        {
                            "nom_createur": nom_createur,
                        },
                    )
                    res = cursor.fetchall()
                    if not res:
                        return []
                    liste_tournois = []
                    if isinstance(res, list):
                        for element in res:
                            liste_tournois.append(
                                Tournoi(
                                    id_tournoi=element["id_tournoi"],
                                    nom_tournoi=element["nom"],
                                    nom_createur=element["nom_createur"],
                                    officiel=element["officiel"],
                                )
                            )
                        return liste_tournois
                    else:
                        return [
                            Tournoi(
                                id_tournoi=res["id_tournoi"],
                                nom_tournoi=res["nom"],
                                nom_createur=res["nom_createur"],
                                officiel=res["officiel"],
                            )
                        ]

        except Exception as e:
            logging.error(f"Erreur lors de la récupération des équipes : {e}")
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
