from dao.db_connection import DBConnection
from business_object.Utilisateur import Utilisateur
from business_object.Pari import Pari
class ParisDao:
    """Classe contenant les méthodes pour accéder aux paris dans la base de données"""
    def __init__(self):
        self.Pari = Pari


    def get_available_tournaments(self):
        """Récupère les tournois disponibles à partir des paris enregistrés."""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT DISTINCT tournoi
                    FROM match_a_parier;
                """)
                rows = cursor.fetchall()
                return [row['tournoi'] for row in rows]  # Liste des tournois disponibles

    def get_teams_for_tournament(self, tournoi):
        """Récupère les équipes disponibles pour un tournoi donné."""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT equipe1, equipe2,
                        MAX(cote_equipe1) AS cote_equipe1,
                        MAX(cote_equipe2) AS cote_equipe2
                    FROM match_a_parier
                    WHERE tournoi = %s
                    GROUP BY equipe1, equipe2;
                """, (tournoi,))
                rows = cursor.fetchall()
                teams = set()  # Utiliser un set pour éviter les doublons
                for row in rows:
                    teams.add(str(row["cote_equipe1"])+"  "+ row['equipe1']+ " vs "+ row['equipe2']+"  "+str( row["cote_equipe2"]))
                return list(teams)

    def afficher_infos_paris(self):
        """Affiche les paris possibles présents dans la DAO et retourne une liste d'objets Pari."""
        paris = []  # Liste pour stocker les objets Pari
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Exécuter la requête SELECT *
                    cursor.execute("SELECT * FROM match_a_parier;")
                    rows = cursor.fetchall()  # Récupérer tous les résultats

                    # Vérifier si des paris sont disponibles
                    if not rows:
                        print("Aucun pari disponible dans la base de données.")
                        return paris

                    # Parcourir les résultats et créer des objets Pari
                    for row in rows:

                        pari = Pari(
                            id_match=row["id_match"],
                            tournoi=row["tournoi"],
                            equipe1=row["equipe1"],
                            equipe2=row["equipe2"],
                            cote_equipe1=row["cote_equipe1"],
                            cote_equipe2=row["cote_equipe2"],
                            date=row["date"])

                        paris.append(pari)

        except Exception as e:
            print(f"Erreur lors de l'affichage des paris : {e}")

        return paris



    def ajouter_paris(self, tournoi_voulu, equipe_voulue,pseudo):
        """
        Ajoute les paris selon le tournoi et l'équipe spécifiés
        dans la table paris_utilisateur, et retourne les données insérées.

        Parameters
        ----------
        tournoi_voulu : str
            Nom du tournoi

        equipe_voulu : str
            Nom de l'équipe

        Return
        ------
        filtered_results : Tuple
            Liste de tuples (equipe, cote, tournoi) correspondant aux données insérées.
        """
        try:
            # Connexion à la base de données principale
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête pour filtrer selon le tournoi et l'équipe
                    cursor.execute("""
                        SELECT*
                        FROM match_a_parier
                        WHERE tournoi = %s AND (equipe1 = %s OR equipe2 = %s);
                    """, (tournoi_voulu, equipe_voulue, equipe_voulue))

                    rows = cursor.fetchall()  # Récupérer les résultats
            # Transformer les résultats pour renvoyer (equipe, cote, tournoi) uniquement
            filtered_results = []

            for row in rows:
                equipe1 = row['equipe1']
                cote1 = row['cote_equipe1']
                equipe2 = row['equipe2']
                cote2 = row['cote_equipe2']
                tournoi = row['tournoi']
                date = row['date']

                if equipe1 == equipe_voulue:
                    filtered_results.append((tournoi,equipe1, equipe2,date, cote1, pseudo ))
                elif equipe2 == equipe_voulue:
                    filtered_results.append((tournoi,equipe2, equipe1,date, cote2, pseudo ))

            # Insérer les résultats filtrés dans la table paris_utilisateur
            if filtered_results:
                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.executemany("""
                            INSERT INTO paris_utilisateur (tournoi,equipe_parier, equipe_adverse,date, cote, pseudo )
                            VALUES (%s, %s, %s, %s, %s, %s);
                        """, filtered_results)

            return filtered_results

        except Exception as e:
            raise RuntimeError(f"Erreur lors de la gestion des paris : {e}")


    def info_paris(self, pseudo):
        """
        Trouve les paris d'un utilisateur selon son pseudo

        Parameters
        ----------
        pseudo : str
            Pseudo de l'utilisateur

        Return
        ------
        rows : List[Tuple(str)]
            Liste des infos sur les paris de l'utilisateur
        """
        try:
            # Connexion à la base de données principale
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête pour filtrer les paris selon le pseudo
                    cursor.execute("""
                        SELECT *
                        FROM paris
                        WHERE pseudo = %s;
                    """, (pseudo,))  # Ajout de la virgule pour passer un tuple

                    # Récupération des résultats
                    rows = cursor.fetchall()

                    # Affichage des résultats (optionnel)
                    if rows:
                        for row in rows:
                            print(f"Match: {row['tournoi']}, {row['equipe']} , Cote: {row['cote']}, Resultat: {row['win']}")
                    else:
                        print(f"Aucun pari trouvé pour le pseudo {pseudo}.")

                    return rows  # Retourne les résultats pour une utilisation ultérieure

        except Exception as e:
            print(f"Erreur lors de la récupération des paris pour le pseudo {pseudo}: {e}")


    def lister_tous_paris_utilisateur(self,pseudo):
        try:
            # Connexion à la base de données principale
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Première requête : obtenir les paris d'un utilisateur par pseudo
                    cursor.execute("""SELECT * FROM paris_utilisateur WHERE pseudo = %s;""", (pseudo,))
                    rows = cursor.fetchall()

                    if rows:
                        # Liste pour stocker les résultats détaillés
                        results = []

                        # Récupérer les paris et associer les informations des matchs en une seule requête
                        query = """
                            SELECT DISTINCT p.tournoi, p.equipe_parier, p.equipe_adverse, p.date, p.cote, p.pseudo,
                                m.score_equipe1, m.score_equipe2,m.equipe1,m.equipe2
                            FROM paris_utilisateur p
                            JOIN match_result m
                                ON p.tournoi = m.tournoi
                                AND p.date = m.date
                                AND (p.equipe_adverse = m.equipe1 OR p.equipe_adverse = m.equipe2)
                                AND (p.equipe_parier = m.equipe1 OR p.equipe_parier = m.equipe2);
                        """
                        cursor.execute(query)
                        match_results = cursor.fetchall()

                        # Traiter chaque résultat du match
                        for match in match_results:
                            # Créer un dictionnaire pour chaque match
                            if (match['score_equipe1'] > match['score_equipe2'] and match['equipe_parier'] == match['equipe1']) or \
                                (match['score_equipe1'] < match['score_equipe2'] and match['equipe_parier'] == match['equipe2']):
                                win = True
                            else:
                                win = False


                            # Vérifier si un pari pour cet utilisateur et cette équipe existe déjà
                            check_query = """
                                SELECT * FROM paris
                                WHERE pseudo = %s AND equipe_nom = %s;
                            """
                            cursor.execute(check_query, (pseudo, match['equipe_parier']))
                            existing_paris = cursor.fetchone()

                            if existing_paris:
                                # Si le pari existe, mettre à jour les informations
                                update_query = """
                                    UPDATE paris
                                    SET cote = %s, win = %s
                                    WHERE pseudo = %s AND equipe_nom = %s;
                                """
                                cursor.execute(update_query, (
                                    match['cote'],         # Nouvelle cote
                                    win,                   # Résultat calculé (win/lose)
                                    pseudo,                # Utilisateur
                                    match['equipe_parier'] # Équipe pariée
                                ))
                            else:
                                # Sinon, insérer un nouveau pari
                                insert_query = """
                                    INSERT INTO paris (pseudo, equipe_nom, cote, win)
                                    VALUES (%s, %s, %s, %s);
                                """
                                cursor.execute(insert_query, (
                                    pseudo,                # Utilisateur
                                    match['equipe_parier'],# Équipe pariée
                                    match['cote'],         # Cote
                                    win                    # Résultat calculé (win/lose)
                                ))

                            # Ajouter les détails à la liste des résultats
                            ole = {
                                'tournoi': match['tournoi'],
                                'equipe_parier': match['equipe_parier'],
                                'equipe_adverse': match['equipe_adverse'],
                                'date': match['date'],
                                'cote': match['cote'],
                                'pseudo': match['pseudo'],
                                'score_equipe1': match['score_equipe1'],
                                'score_equipe2': match['score_equipe2'],
                                'win': win
                            }
                            results.append(ole)

                        # Confirmer les changements dans la base de données
                        connection.commit()

                        # Retourner la liste des paris insérés ou mis à jour
                        return results

                    # Si aucun pari n'est trouvé
                    return []

        except Exception as e:
            print(f"Une erreur est survenue : {e}")
            return []
