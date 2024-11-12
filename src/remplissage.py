import requests
import pandas as pd
import os
import dotenv
from dao.db_connection import DBConnection  # Importation de DBConnection

# Chargement des variables d'environnement
dotenv.load_dotenv()


class API:
    def __init__(self, base_url):
        self.base_url = base_url

    def recuperer_page(self, endpoint, params=None):
        """Récupère les données depuis un endpoint API spécifié."""
        url = self.base_url + endpoint
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur : Impossible de récupérer les données depuis {url}")
            return None


class MatchProcessor:
    def __init__(self, api):
        self.api = api
        self.liste_matchs = []
        self.donnees_matchs = []
        self.matchs_filtrés = []
        self.joueurs_filtrés = []

    def recuperer_matchs(self, page, taille_page):
        """Récupère toutes les données des matchs depuis l'API et les stocke."""
        endpoint = f"/matches?page={page}&page_size={taille_page}"
        data = self.api.recuperer_page(endpoint)

        print("Données récupérées pour les matchs :", data)

        if data and "matches" in data:
            self.donnees_matchs = data["matches"]
            self.liste_matchs = [match["id_match"] for match in data["matches"]]
            return self.liste_matchs
        else:
            print("Erreur : Impossible de récupérer les matchs.")
            return None

    def traiter_matchs(self):
        """Traite les données des matchs et des joueurs."""
        with DBConnection().connection as conn:
            with conn.cursor() as cursor:
                for donnees_match in self.donnees_matchs:
                    if donnees_match == {"detail": "Match Unknown"}:
                        print("Erreur : Match inconnu. Aucun traitement effectué.")
                        continue

                    # Insertion dans info_match
                    cursor.execute(
                        """
                        INSERT INTO "RocketLag".info_match (match_id, event, date)
                        VALUES (%s, %s, %s)
                        ;
                        """,
                        (donnees_match["id_match"], donnees_match["event"], donnees_match["date"]),
                    )

                    ligue = donnees_match["event"]
                    region = "Inconnue"
                    date = donnees_match["date"]

                    for couleur in ["blue", "orange"]:
                        self.traiter_equipe(donnees_match, couleur, ligue, region, date, cursor)
                conn.commit()

    def traiter_equipe(self, donnees_match, couleur, ligue, region, date, cursor):
        """Traite les données d'une équipe pour un match et une couleur donnés."""
        donnees_equipe = donnees_match.get(couleur, {})

        nom_equipe = donnees_equipe.get("team", "NomInconnu")
        score_equipe = donnees_equipe.get("score")
        stats_base = donnees_equipe.get("stats", {}).get("core", {})

        stats_equipe = {
            "equipe_nom": nom_equipe,
            "equipe_score": score_equipe,
            "shots": stats_base.get("shots", 0),
            "goals": stats_base.get("goals", 0),
            "saves": stats_base.get("saves", 0),
            "assists": stats_base.get("assists", 0),
            "score": stats_base.get("score", 0),
            "demo_inflige": donnees_equipe.get("stats", {}).get("demo", {}).get("inflicted", 0),
            "demo_recu": donnees_equipe.get("stats", {}).get("demo", {}).get("taken", 0),
            "shooting_percentage": stats_base.get("shootingPercentage", 0.0),
            "time_defensive_third": donnees_equipe.get("stats", {})
            .get("positioning", {})
            .get("timeDefensiveThird", 0.0),
            "time_neutral_third": donnees_equipe.get("stats", {})
            .get("positioning", {})
            .get("timeNeutralThird", 0.0),
            "time_offensive_third": donnees_equipe.get("stats", {})
            .get("positioning", {})
            .get("timeOffensiveThird", 0.0),
            "date": date,
            "region": region,
            "ligue": ligue,
        }

        # Vérification de l'existence de l'équipe
        cursor.execute(
            'SELECT id_equipe FROM "RocketLag".Equipe WHERE equipe_nom = %s', (nom_equipe,)
        )
        result = cursor.fetchone()

        if result:
            id_equipe = result["id_equipe"]
        else:
            # Insertion de l'équipe
            cursor.execute(
                """
                INSERT INTO "RocketLag".Equipe (
                    equipe_nom, equipe_score, shots, goals, saves, assists, score,
                    demo_infligees, demo_recues, shooting_percentage,
                    time_defensive_third, time_neutral_third, time_offensive_third,
                    region, ligue
                )
                VALUES (%(equipe_nom)s, %(equipe_score)s, %(shots)s, %(goals)s, %(saves)s,
                        %(assists)s, %(score)s, %(demo_inflige)s, %(demo_recu)s,
                        %(shooting_percentage)s, %(time_defensive_third)s, %(time_neutral_third)s,
                        %(time_offensive_third)s, %(region)s, %(ligue)s)
                RETURNING id_equipe;
                """,
                stats_equipe,
            )
            id_equipe = cursor.fetchone()["id_equipe"]

        # Insertion de la relation match-équipe
        cursor.execute(
            """
            INSERT INTO "RocketLag".matchs_equipe (id_match, id_equipe)
            VALUES (%s, %s);
            """,
            (donnees_match["id_match"], id_equipe),
        )

    def creer_dataframes(self):
        """Crée des DataFrames pandas à partir des données filtrées des matchs et des joueurs."""
        df_matchs_filtrés = pd.DataFrame(self.matchs_filtrés)
        df_joueurs_filtrés = pd.DataFrame(self.joueurs_filtrés)
        return df_matchs_filtrés, df_joueurs_filtrés


# Utilisation
api = API(base_url="https://api.rlcstatistics.net")
processeur_matchs = MatchProcessor(api)

# Étapes de traitement
processeur_matchs.recuperer_matchs(page=226, taille_page=2)
processeur_matchs.traiter_matchs()

# Création des DataFrames
df_matchs, df_joueurs = processeur_matchs.creer_dataframes()
print(df_matchs)
print(df_joueurs)
