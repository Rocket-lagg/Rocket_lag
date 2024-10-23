import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.Equipe import Equipe
from business_object.joueur import Joueur

class EquipeDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Joueurs de la base de données"""

    @log
    def creer(self, equipe) -> bool:
        """Creation d'un joueur dans la base de données

        Parameters
        ----------
        equipe : Equipe

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête d'insertion SQL avec RETURNING pour récupérer l'ID
                    cursor.execute(
                        """
                        INSERT INTO Equipe (match_id, equipe_nom, equipe_score, boost_stole,
                                        shots, goals, saves, assists, score, shooting_percentage,
                                         date, ligue, region, stage, time_offensive_third, time_defensive_third,
                                         time_neutral_third, demo_inflige, demo_recu )
                        VALUES (%(match_id)s, %(equipe_nom)s, %(equipe_score)s, %(boost_stole)s,
                                %(shots)s, %(goals)s, %(saves)s, %(assists)s, %(score)s, %(shooting_percentage)s,
                                 %(date)s, %(ligue)s, %(region)s, %(stage)s, %(time_offensive_third)s, %(time_defensive_third)s,
                                %(time_neutral_third)s, %(demo_inflige)s, %(demo_recu)s)
                        RETURNING equipe_nom;

                        """,
                        {
                            "match_id": equipe.match_id,
                            "equipe_nom": equipe.equipe_nom,
                            "equipe_score": equipe.equipe_score,
                            "boost_stole": equipe.boost_stole,
                            "shots": equipe.shots,
                            "goals": equipe.goals,
                            "saves": equipe.saves,
                            "assists": equipe.assists,
                            "score": equipe.score,
                            "shooting_percentage": equipe.shooting_percentage,
                            "date": equipe.date,
                            "ligue": equipe.ligue,
                            "region": equipe.region,
                            "stage": equipe.stage,
                            "time_offensive_third": equipe.time_offensive_third,
                            "time_defensive_third": equipe.time_defensive_third,
                            "time_neutral_third": equipe.time_neutral_third,
                            "demo_inflige": equipe.demo_inflige,
                            "demo_recu": equipe.demo_recu
                         },
                    )
                    # Récupérer l'ID du joueur créé
                    res = cursor.fetchone()
            return res is not None
        except Exception as e:
            logging.error(f"Erreur lors de la création d'equipe : {e}")
            return False


    def creer_table_equipe():
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Commande SQL pour supprimer et recréer la table Equipe
                    cursor.execute("""
                        DROP TABLE IF EXISTS Equipe;
                        CREATE TABLE Equipe (
                            equipe_id SERIAL PRIMARY KEY,
                            match_id VARCHAR(50) NOT NULL,
                            equipe_nom VARCHAR(100) NOT NULL,
                            equipe_score INTEGER,
                            boost_stole INTEGER,
                            shots INTEGER,
                            goals INTEGER,
                            saves INTEGER,
                            assists INTEGER,
                            score INTEGER,
                            shooting_percentage FLOAT,
                            time_offensive_third FLOAT,
                            time_defensive_third FLOAT,
                            time_neutral_third FLOAT,
                            demo_inflige INTEGER,
                            demo_recu INTEGER,
                            date DATE,  -- Le format de la date doit être 'YYYY-MM-DD'
                            ligue VARCHAR(100),
                            region VARCHAR(100),
                            stage VARCHAR(100)
                        );
                    """)
                    connection.commit()  # Confirmer les modifications
                    logging.info("Table Equipe créée avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de la création de la table Equipe: {e}")

    # Appel de la fonction pour créer la table

        @log
        def lister_tous(self) -> list[Joueur]:
            """lister tous les joueurs

            Parameters
            ----------
            None

            Returns
            -------
            liste_joueurs : list[Joueur]
                renvoie la liste de tous les joueurs dans la base de données
            """

            try:
                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT *                              "
                            "  FROM joueur;                        "
                        )
                        res = cursor.fetchall()
            except Exception as e:
                logging.info(e)
                raise

        liste_joueurs = []

        if res:
            for row in res:
                joueur = Joueur(
                    id_joueur=row["id_joueur"],
                    pseudo=row["pseudo"],
                    mdp=row["mdp"],
                    age=row["age"],
                    mail=row["mail"],
                    fan_pokemon=row["fan_pokemon"],
                )

                liste_joueurs.append(joueur)

        return liste_joueurs
