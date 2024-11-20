import logging
from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.Tournoi import Tournoi
from tabulate import tabulate


class TournoiDao(metaclass=Singleton):

    def creer_tournoi(
        self, nom_utilisateur, id_tournois, nom_tournois, type_tournoi, tours
    ) -> bool:
        """Création d'un tournoi dans la base de données"""
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête d'insertion SQL avec RETURNING pour récupérer l'ID
                    cursor.execute(
                        """
                        INSERT INTO tournoi (id_tournoi, nom_createur, nom, type_match, tours, officiel)
                        VALUES (%(id_tournoi)s, %(nom_createur)s, %(nom)s, %(type_match)s, %(tours)s, %(officiel)s)
                        RETURNING id_tournoi;
                        """,
                        {
                            "id_tournoi": id_tournois,
                            "nom_createur": nom_utilisateur,
                            "nom": nom_tournois,
                            "type_match": type_tournoi,
                            "tours": tours,
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
                            tournoi = Tournoi(
                                nom_tournoi=element["nom"],
                                createur=element["nom_createur"],
                                id_tournoi=element["id_tournoi"],
                                tour=element["tours"],
                                type_match=element["type_match"],
                                officiel=element["officiel"],
                            )
                            liste_tournois.append(tournoi)
                        return liste_tournois
                    else:
                        tournoi = Tournoi(
                            nom_tournoi=res["nom"],
                            createur=res["nom_createur"],
                            id_tournoi=res["id_tournoi"],
                            tour=res["tours"],
                            type_match=res["type_match"],
                            officiel=res["officiel"],
                        )
                        return [tournoi]

        except Exception as e:
            logging.error(f"Erreur lors de la récupération des tournois : {e}")
            return False

    def recuperer_equipe(self, id_tournoi, tour):
        res = None
        print("cc")
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT nom_equipe
                        FROM equipe_tournoi
                        WHERE id_tournoi = %(id_tournoi)s AND tour = %(tour)s
                        """,
                        {
                            "id_tournoi": id_tournoi,
                            "tour": tour,
                        },
                    )
                    res = cursor.fetchall()
                    if not res:
                        return []
                    liste_equipe = []
                    if isinstance(res, list):
                        for element in res:
                            liste_equipe.append(element["nom_equipe"])
                        return liste_equipe
                    return res["nom_equipe"]

        except Exception as e:
            logging.error(f"Erreur lors de la récupération des équipes : {e}")
            return False

    def ajouter_score_match(self, score1, score2, match_id):
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête d'insertion SQL avec RETURNING pour récupérer l'ID
                    cursor.execute(
                        """
                            UPDATE match_tournoi
                            SET score_equipe1 = %(score_equipe1)s, score_equipe2 = %(score_equipe2)s
                            WHERE id_match = %(id_match)s
                            """,
                        {"score_equipe1": score1, "score_equipe2": score2, "id_match": match_id},
                    )
        except Exception as e:
            print(f"Erreur lors de la création des équipes : {e}")
            return False

    def creer_equipe(self, id_tournoi, nom_equipe, tour):
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête d'insertion SQL avec RETURNING pour récupérer l'ID
                    cursor.execute(
                        """
                            INSERT INTO equipe_tournoi (id_tournoi, nom_equipe, tour)
                            VALUES (%(id_tournoi)s, %(nom_equipe)s, %(tour)s);
                            """,
                        {
                            "id_tournoi": id_tournoi,
                            "nom_equipe": nom_equipe,
                            "tour": tour,
                        },
                    )
        except Exception as e:
            logging.error(f"Erreur lors de la création des équipes : {e}")
            return False

    def creer_match(self, id_tournoi, equipe1, equipe2, tour):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                            INSERT INTO match_tournoi (id_tournoi, equipe1, equipe2, tour)
                            VALUES (%(id_tournoi)s, %(equipe1)s, %(equipe2)s, %(tour)s);
                            """,
                        {
                            "id_tournoi": id_tournoi,
                            "equipe1": equipe1,
                            "equipe2": equipe2,
                            "tour": tour,
                        },
                    )
        except Exception as e:
            logging.error(f"Erreur lors de la création des matchs : {e}")
            return False

    def trouver_matchs_par_tournoi(self, id_tournoi, tour):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                            SELECT id_match, equipe1, equipe2
                            FROM match_tournoi
                            WHERE id_tournoi = %(id_tournoi)s AND tour = %(tour)s
                            """,
                        {
                            "id_tournoi": id_tournoi,
                            "tour": tour,
                        },
                    )
                    res = cursor.fetchall()
                    if res:
                        liste = []
                        for r in res:
                            liste.append([r["id_match"], r["equipe1"], r["equipe2"]])
                        return liste
                    else:
                        return []
        except Exception as e:
            logging.error(f"Erreur lors de la recherche des matchs : {e}")
            return False

    def recuperer_score_match(self, equipe1, equipe2):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                            SELECT score_equipe1, score_equipe2
                            FROM match_tournoi
                            WHERE equipe1 = %(equipe1)s AND equipe2 = %(equipe2)s
                            """,
                        {
                            "equipe1": equipe1,
                            "equipe2": equipe2,
                        },
                    )
                    res = cursor.fetchone()
                    if res:
                        return [res["score_equipe1"], res["score_equipe2"]]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Erreur lors de la recherche des scores : {e}")
            return False

    def modifier_tour_gagnant_equipe(self, equipe):
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                            UPDATE equipe_tournoi
                            SET tour = tour + 1
                            WHERE nom_equipe = %(equipe)s;
                            """,
                        {"equipe": equipe},
                    )
        except Exception as e:
            print(f"Erreur lors de l'incrémentation du tour dans equipe_tournoi : {e}")
            return False

    def recuperer_tour(self):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT MAX(tour) AS max_tour
                        FROM equipe_tournoi;
                        """
                    )
                    res = cursor.fetchone()
                    if res:
                        return res["max_tour"]  # Renvoie uniquement la valeur de max_tour
                    else:
                        return 1
        except Exception as e:
            logging.error(f"Erreur lors de la recherche du tour : {e}")
            return False

    def donner_nombre_equipe(self):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT COUNT(*) AS nombre_lignes
                        FROM equipe_tournoi;
                    """
                    )
                    res = cursor.fetchone()
                    return res["nombre_lignes"]
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du nombre de lignes : {e}")
            return None

    def recuperer_tour_depuis_match(self):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                            SELECT MAX(tour) AS max_tour
                            FROM match_tournoi;
                            """
                    )
                    res = cursor.fetchone()
                    if res:
                        return res["max_tour"]
                    else:
                        return 1
        except Exception as e:
            logging.error(f"Erreur lors de la recherche du tour : {e}")
            return False

    def afficher_pooling_tournoi(self):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT equipe1,
                            score_equipe1,
                            equipe2,
                            score_equipe2,
                            tour
                        FROM match_tournoi
                        ORDER BY tour;
                    """
                    )
                    resultats = cursor.fetchall()

                    # Si des résultats sont disponibles
                    if resultats:
                        # Transformer les résultats en tableau
                        tableau = [
                            [
                                r["equipe1"],
                                r["score_equipe1"],
                                r["equipe2"],
                                r["score_equipe2"],
                                r["tour"],
                            ]
                            for r in resultats
                        ]

                        # Afficher en format tableau
                        print(
                            tabulate(
                                tableau,
                                headers=["Équipe 1", "Score 1", "Équipe 2", "Score 2", "Round"],
                                tablefmt="grid",
                            )
                        )
                    else:
                        print("Aucun match trouvé dans le tournoi.")
        except Exception as e:
            print(f"Erreur lors de l'affichage du pooling : {e}")
