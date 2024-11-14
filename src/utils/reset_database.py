import os
import logging


from unittest import mock

from utils.log_decorator import log
from utils.singleton import Singleton
from dao.db_connection import DBConnection
from service.utilisateur_service import UtilisateurService
import dotenv
dotenv.load_dotenv()  # Charger .env avant d'utiliser DBConnection ou ResetDatabase


class ResetDatabase(metaclass=Singleton):
    """
    Classe pour gérer la réinitialisation de la base de données.
    """

    def lancer(self):
        """
        Création de la table Joueur dans la base de données.
        """
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Commande SQL pour supprimer et recréer la table Joueur
                    cursor.execute(
                        """
                        DROP TABLE IF EXISTS Joueur;
                        CREATE TABLE Joueur (
                            joueur_id SERIAL PRIMARY KEY,
                            nom VARCHAR(100) NOT NULL,
                            nationalite VARCHAR(50),
                            rating FLOAT,
                            match_id VARCHAR(50) NOT NULL,
                            equipe_nom VARCHAR(100),
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
                            goal_participation FLOAT,
                            date DATE,                 -- Date du match
                            region VARCHAR(50),        -- Région du match
                            ligue VARCHAR(100),        -- Ligue à laquelle appartient le match
                            stage VARCHAR(100)         -- Étape ou phase du tournoi ou du match
                        );
                        """
                    )
                    connection.commit()  # Confirmer les modifications
                    logging.info("Table Joueur créée avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de la création de la table Joueur: {e}")

if __name__ == "__main__":
    dotenv.load_dotenv()  # Charger les variables d'environnement
    # Créer une instance de ResetDatabase et créer la table Joueur
    reset_db = ResetDatabase()
    reset_db.lancer()
