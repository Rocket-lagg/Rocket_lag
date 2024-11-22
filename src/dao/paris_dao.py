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
                    FROM paris_utilisateur;
                """)
                rows = cursor.fetchall()
                return [row['tournoi'] for row in rows]  # Liste des tournois disponibles

    def get_teams_for_tournament(self, tournoi):
        """Récupère les équipes disponibles pour un tournoi donné."""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT DISTINCT equipe_parier, equipe_adverse
                    FROM paris_utilisateur
                    WHERE tournoi = %s;
                """, (tournoi,))
                rows = cursor.fetchall()
                teams = set()  # Utiliser un set pour éviter les doublons
                for row in rows:
                    teams.add(row['equipe_parier'])
                    teams.add(row['equipe_adverse'])
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
        Filtre les paris selon le tournoi et l'équipe spécifiés, insère les résultats
        dans la table `paris_utilisateur`, et retourne les données insérées.

        :param tournoi_voulu: Nom du tournoi à filtrer (chaîne).
        :param equipe_voulue: Nom de l'équipe à filtrer (chaîne).
        :return: Liste de tuples (equipe, cote, tournoi) correspondant aux données insérées.
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
                    filtered_results.append((equipe1, equipe2, cote1, pseudo, tournoi, date))
                elif equipe2 == equipe_voulue:
                    filtered_results.append((equipe2, equipe1, cote2, pseudo, tournoi, date))

            # Insérer les résultats filtrés dans la table paris_utilisateur
            if filtered_results:
                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.executemany("""
                            INSERT INTO paris_utilisateur (equipe_parier, equipe_adverse, cote, pseudo, tournoi, date)
                            VALUES (%s, %s, %s, %s, %s, %s);
                        """, filtered_results)

            return filtered_results

        except Exception as e:
            raise RuntimeError(f"Erreur lors de la gestion des paris : {e}")


    def info_paris(self, pseudo):
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



    def supprimer_un_paris(self, paris) -> bool:
        """Suppression d'un pari dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO utilisateur(pseudo, mdp, mail, points)
                        VALUES(%(pseudo)s, %(mdp)s, %(mail)s, 0)
                        RETURNING id_utilisateur;
                        """,
                        {
                            "pseudo": utilisateur.nom_utilisateur,
                            "mdp": utilisateur.mot_de_passe,
                            "mail": utilisateur.email,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            print(e)

        created = False
        if res:
            if isinstance(res["id_utilisateur"], int):
                created = True
        return created
