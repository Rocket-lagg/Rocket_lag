import logging
from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.Tournoi import Tournoi
from tabulate import tabulate


class TournoiDao(metaclass=Singleton):

    def creer_tournoi(
        self, nom_utilisateur, id_tournois, nom_tournois, type_tournoi, tours
        ) -> bool:
        """
        Crée un tournoi dans la base de données.

        Parameters
        ----------
        nom_utilisateur : str
            Le nom de l'utilisateur qui crée le tournoi.
        id_tournois : str
            L'identifiant unique du tournoi.
        nom_tournois : str
            Le nom du tournoi à créer.
        type_tournoi : int
            Le type de tournoi ("1vs1", "2vs2", "3vs3").
        tours : int
            Le nombre de tours ou phases dans le tournoi.

        Return
        -------
        bool : Bool
            True si le tournoi a été créé avec succès, False sinon.
        """
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
        """
        Récupère la liste des tournois d'un utilisateur

        Parameters
        ----------
        nom_createur : str
            Le nom de l'utilisateur qui crée le tournoi.

        Return
        -------
        liste_tournois : List[Tournoi]
            Liste des tournois créés par l'utilisateur
        """
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
                        )
                        return [tournoi]

        except Exception as e:
            logging.error(f"Erreur lors de la récupération des tournois : {e}")
            return []

    def recuperer_equipe(self, id_tournoi, tour):
        """
        Récupère les équipes d'un tournoi pour un tour donné.

        Parameters
        ----------
        id_tournoi : int
            L'identifiant unique du tournoi.
        tour : int
            Le numéro du tour pour lequel les équipes doivent être récupérées.

        Return
        ------
        liste_equipe : List[str]
            Une liste contenant les noms des équipes participant au tour spécifié dans le tournoi.
            Retourne une liste vide si aucune équipe n'est trouvée.
        False : bool
            Retourne False en cas d'erreur lors de l'exécution de la requête.
        """
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
                    print(res)
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
        """
        Met à jour les scores d'un match spécifique dans la base de données.

        Parameters
        ----------
        score1 : int
            Le score de l'équipe 1.
        score2 : int
            Le score de l'équipe 2.
        match_id : int
            L'identifiant unique du match à mettre à jour.

        Return
        ------
        success : bool
            Retourne False en cas d'erreur lors de la mise à jour des scores.
            Aucun retour explicite (None) si l'opération est réussie.
        """
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
        """
        Ajoute une équipe dans un tournoi spécifique pour un tour donné.

        Parameters
        ----------
        id_tournoi : int
            L'identifiant unique du tournoi auquel l'équipe est associée.
        nom_equipe : str
            Le nom de l'équipe à ajouter.
        tour : int
            Le numéro du tour auquel l'équipe participe.

        Return
        ------
        success : bool
            Retourne False en cas d'erreur lors de l'insertion de l'équipe dans la base de données.
            Aucun retour explicite (None) si l'opération est réussie.
        """
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
        """
        Ajoute un match entre deux équipes dans un tournoi spécifique pour un tour donné.

        Parameters
        ----------
        id_tournoi : int
            L'identifiant unique du tournoi auquel le match est associé.
        equipe1 : str
            Le nom de la première équipe participant au match.
        equipe2 : str
            Le nom de la deuxième équipe participant au match.
        tour : int
            Le numéro du tour auquel le match appartient.

        Return
        ------
        success : bool
            Retourne False en cas d'erreur lors de l'insertion du match dans la base de données.
            Aucun retour explicite (None) si l'opération est réussie.
        """
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
        """
        Récupère la liste des matchs d'un tournoi spécifique pour un tour donné.

        Parameters
        ----------
        id_tournoi : int
            L'identifiant unique du tournoi pour lequel les matchs sont recherchés.
        tour : int
            Le numéro du tour auquel les matchs appartiennent.

        Return
        ------
        liste_matchs : List[List[Any]]
            Une liste contenant les informations des matchs (id_match, equipe1, equipe2) pour le tour spécifié.
            Retourne une liste vide si aucun match n'est trouvé.
        success : bool
            Retourne False en cas d'erreur lors de la récupération des données depuis la base de données.
        """
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
        """
        Récupère les scores d'un match entre deux équipes spécifiques.

        Parameters
        ----------
        equipe1 : str
            Le nom de la première équipe.
        equipe2 : str
            Le nom de la deuxième équipe.

        Return
        ------
        scores : List[int]
            Une liste contenant les scores des deux équipes. Si le match n'est pas trouvé, retourne une liste vide.
        success : bool
            Retourne False en cas d'erreur lors de la récupération des données depuis la base de données.
        """
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
        """
        Modifie le tour d'une équipe gagnante en incrémentant le tour dans la base de données.

        Parameters
        ----------
        equipe : str
            Le nom de l'équipe dont le tour doit être incrémenté.

        Return
        ------
        success : bool
            Retourne `True` si la mise à jour a réussi, `False` en cas d'erreur lors de l'incrémentation du tour dans la base de données.
        """
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
        """
        Récupère le numéro du tour le plus élevé dans la table equipe_tournoi.

        Cette fonction exécute une requête pour récupérer le tour maximal auquel une équipe a participé,
        en fonction des données présentes dans la base de données. Si aucune donnée n'est trouvée,
        le tour est considéré comme étant le tour 1 par défaut.

        Return
        ------
        max_tour : int
            Le numéro du tour le plus élevé. Si aucune donnée n'est disponible, renvoie 1.
        """
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
                    print(res)
                    if res:
                        return res["max_tour"]  # Renvoie uniquement la valeur de max_tour
                    else:
                        return 1
        except Exception as e:
            logging.error(f"Erreur lors de la recherche du tour : {e}")
            return False

    def donner_nombre_equipe(self):
        """
        Récupère le nombre total d'équipes présentes dans la table equipe_tournoi.

        Return
        ------
        nombre_lignes : int
            Le nombre d'équipes présentes dans la table equipe_tournoi.
            Si une erreur survient, la fonction retourne None.
        """
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
        """
        Récupère le numéro du tour le plus élevé des matchs dans la table match_tournoi.

        Return
        ------
        max_tour : int
            Le numéro du tour le plus élevé. Si aucune donnée n'est disponible, renvoie 1.
            En cas d'erreur, retourne False.
        """
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
        """
        Affiche un tableau des matchs d'un tournoi, incluant les scores et les informations sur les équipes.

        Return
        ------
        None
            Cette fonction n'a pas de valeur de retour. Elle se charge uniquement de l'affichage des résultats.
        """
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

    def recuperer_tournoi_par_clef(self, clef):
        res = None
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM tournoi
                        WHERE id_tournoi = %(id_tournoi)s
                        """,
                        {
                            "id_tournoi": clef,
                        },
                    )
                    res = cursor.fetchone()
                    print(res)
                    if not res:
                        return []
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

    def recuperer_joueur_par_equipe(self, nom):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                            SELECT joueur1, joueur2, joueur3
                            FROM equipe_tournoi
                            WHERE nom_equipe = %(nom)s
                            """,
                        {
                            "nom": nom,
                        },
                    )
                    res = cursor.fetchone()
                    if res:
                        return [res["joueur1"], res["joueur2"], res["joueur3"]]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Erreur lors de la recherche des joueurs : {e}")
            return False

    def ajouter_joueur_equipe(self, joueur, equipe):
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                            UPDATE equipe_tournoi
                            SET
                                joueur1 = CASE WHEN joueur1 IS NULL THEN %(joueur)s ELSE joueur1 END,
                                joueur2 = CASE WHEN joueur1 IS NOT NULL AND joueur2 IS NULL THEN %(joueur)s ELSE joueur2 END,
                                joueur3 = CASE WHEN joueur1 IS NOT NULL AND joueur2 IS NOT NULL AND joueur3 IS NULL THEN %(joueur)s ELSE joueur3 END
                            WHERE nom_equipe = %(equipe)s
                            AND (
                                joueur1 IS NULL
                                OR joueur2 IS NULL
                                OR joueur3 IS NULL
                                );
                            """,
                        {"joueur": joueur, "equipe": equipe},
                    )
        except Exception as e:
            print(f"Erreur lors de la création des joueurs : {e}")
            return False

    def ajouter_joueur_tournoi(self, nom_utilisateur, id_tournoi):
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                            INSERT INTO tournois_utilisateur (nom_utilisateur, id_tournoi)
                            VALUES (%(nom_utilisateur)s, %(id_tournoi)s);
                            """,
                        {"nom_utilisateur": nom_utilisateur, "id_tournoi": id_tournoi},
                    )
        except Exception as e:
            print(f"Erreur lors de l'inscription des utilisateurs et des tournois : {e}")
            return False

    def recuperer_tournoi_utilisateur(utilisateur):
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_tournoi
                        FROM utilisateur_tournoi
                        WHERE nom_utilisateur = %(utilisateur)s;
                        """,
                        {"utilisateur": utilisateur},
                    )
                    tournois = cursor.fetchall()
                    return [tournoi["id_tournoi"] for tournoi in tournois]
        except Exception as e:
            print(
                f"Erreur lors de la récupération des tournois pour l'utilisateur {utilisateur} : {e}"
            )
            return None

    def recuperer_tournoi_info(self, id_tournoi):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT nom, nom_createur, type_match, tours, officiel
                        FROM tournoi
                        WHERE id_tournoi = %(id_tournoi)s;
                        """,
                        {"id_tournoi": id_tournoi},
                    )
                    # Récupérer le résultat AVANT la fermeture du curseur
                    result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Erreur lors de la récupération des informations du tournoi {id_tournoi} : {e}")
            return None

    def recuperer_equipes_tournoi(self, id_tournoi):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT nom_equipe, tour, joueur1, joueur2, joueur3
                        FROM equipe_tournoi
                        WHERE id_tournoi = %(id_tournoi)s
                        ORDER BY tour, nom_equipe;
                        """,
                        {"id_tournoi": id_tournoi},
                    )
                    result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Erreur lors de la récupération des équipes du tournoi {id_tournoi} : {e}")
            return None

    def recuperer_matchs_tournoi(self, id_tournoi):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_match, equipe1, equipe2, score_equipe1, score_equipe2, tour
                        FROM match_tournoi
                        WHERE id_tournoi = %(id_tournoi)s
                        ORDER BY tour, id_match;
                        """,
                        {"id_tournoi": id_tournoi},
                    )
                    result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Erreur lors de la récupération des matchs du tournoi {id_tournoi} : {e}")
            return None


