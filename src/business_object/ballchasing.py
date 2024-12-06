import os
import requests
from dotenv import load_dotenv
from dao.joueur_dao import JoueurDao
from business_object.joueur import Joueur
from dao.equipe_dao import EquipeDao
from business_object.Equipe import Equipe
from business_object.Match import Match
from dao.match_dao import MatchDao

# Load environment variables from .env file
load_dotenv()

# Ballchasing API Class
class BallchasingAPI:
    def __init__(self):
        # Load the API key from environment variables
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Please check your .env file.")

        # Set headers for API requests
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }

        # Base URL for the API
        self.base_url = "https://ballchasing.com/api"
        self.joueur_dao = JoueurDao()
        self.equipe_dao = EquipeDao()
        self.match_dao = MatchDao()

    # Function to fetch data from a URL
    def get_data(self, url):
        """Makes a GET request to the given URL with headers."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raises exception for HTTP errors
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None

    # Function to compile replays from a specific group
    def compile_replays(self, group_id):
        """Fetches and stores replay IDs from a given group."""
        replays_url = f"{self.base_url}/replays?group={group_id}"
        response = self.get_data(replays_url)
        replays = []

        if response and 'list' in response:
            for replay in response['list']:
                replays.append(replay['id'])

        return replays

    # Recursive function to compile groups and sub-groups
    def compile_groups(self, group_id):
        """Recursively fetches group and sub-group replays."""
        groups_url = f"{self.base_url}/groups?group={group_id}"
        response = self.get_data(groups_url)
        all_replays = []

        if response and 'list' in response:
            # Fetch replays of the current group
            replays_in_group = self.compile_replays(group_id)
            all_replays.extend(replays_in_group)

            # Fetch replays in each sub-group
            for group in response['list']:
                sub_group_replays = self.compile_groups(group['id'])
                all_replays.extend(sub_group_replays)

        return all_replays

    # Fetch detailed match data for a given replay ID
    def match_data(self, replay_id):
        """Fetches match data for a specific replay ID."""
        replay_url = f"{self.base_url}/replays/{replay_id}"
        return self.get_data(replay_url)

    def add_major2(self):
        group_id = "lan-nu92kpr2hf"
        ligue="RLCS MAJOR 2"
        stage ="Swiss stage"
        region="INT"
        all_replays = self.compile_groups(group_id)
        if all_replays:
            for i in range(len(all_replays)):
                replay_id = all_replays[i]
                self.match_process(replay_id,ligue,stage,region)

    def add_world(self):
        group_id ="1-swiss-stage-4ws5jld17r"
        all_replays = self.compile_groups(group_id)
        ligue="RLCS 2024 WORLDS"
        stage ="Swiss stage"
        region="INT"
        if all_replays:
            for i in range(len(all_replays)):
                replay_id = all_replays[i]
                self.match_process(replay_id,ligue,stage,region)


    def add_world2(self):
        group_id ="2-playoffs-48kyvcspq9"
        all_replays = self.compile_groups(group_id)
        ligue="RLCS 2024 WORLDS"
        stage ="Play offs"
        region="INT"
        if all_replays:
            for i in range(len(all_replays)):
                replay_id = all_replays[i]
                self.match_process(replay_id,ligue,stage,region)



    def match_process(self,replay,ligue,stage,region):
        match_data = self.match_data(replay)
        team_blue = match_data.get("blue", {}).get("name", "Équipe inconnue")
        team_orange = match_data.get("orange", {}).get("name", "Équipe inconnue")
        date = match_data.get("date", "Date inconnue")
        players_blue = [player.get("name", "Joueur inconnu") for player in match_data.get("blue", {}).get("players", [])]
        players_orange = [player.get("name", "Joueur inconnu") for player in match_data.get("orange", {}).get("players", [])]
        conserver_match=[]

        for couleur in ["blue", "orange"]:  # Parcourir les deux équipes
            conserver_equipe = []

            # Obtenir le nom de l'équipe
            team_name = match_data.get(couleur, {}).get("name", "Équipe inconnue")

            for j, player in enumerate(match_data.get(couleur, {}).get("players", [])):  # Parcourir les joueurs
                joueur_core = player["stats"]["core"]
                joueur_stats = player["stats"]

                # Calculer le pourcentage de tirs réussis
                shooting_percentage = round(
                    (joueur_core['goals'] / joueur_core['shots'] * 100) if joueur_core['shots'] > 0 else 0, 2
                )

                # Construire les données du joueur
                joueur_data = {
                    "match_id": replay,
                    "equipe_nom": team_name,
                    "nom": player.get("name", "Joueur inconnu"),
                    "nationalite": "Inconnue",  # Si disponible, inclure des données plus précises
                    "shots": joueur_core['shots'],
                    "goals": joueur_core['goals'],
                    "saves": joueur_core['saves'],
                    "assists": joueur_core['assists'],
                    "score": joueur_core['score'],
                    "shooting_percentage": shooting_percentage,
                    "demo_inflige": joueur_stats['demo']['inflicted'],
                    "demo_recu": joueur_stats['demo']['taken'],
                    "goal_participation": round(joueur_core.get('goalParticipation', 0), 2),
                    "time_defensive_third": joueur_stats['positioning'].get('time_defensive_third', 0),
                    "time_neutral_third": joueur_stats['positioning'].get('time_neutral_third', 0),
                    "time_offensive_third": joueur_stats['positioning'].get('time_offensive_third', 0),
                    "date": date,
                    "region": region,
                    "stage": stage,
                    "ligue": ligue,
                }

                # Calcul des indices
                joueur = Joueur(**joueur_data)
                joueur.indice_offensif = round(
                    (
                        joueur.goals / 1.05 +
                        joueur.assists / 0.5 +
                        joueur.shots / 3.29 +
                        joueur.demo_inflige / 0.56 +
                        joueur.time_offensive_third / 201.1
                    ), 2
                )
                joueur.indice_performance = round(
                    (
                        joueur.goals * 1 +
                        joueur.assists * 0.75 +
                        joueur.saves * 0.6 +
                        joueur.shots * 0.4 +
                        (joueur.goals / joueur.shots) * 0.5 if joueur.shots > 0 else 0
                    ), 2
                )

                # Enregistrer le joueur dans la base de données
                result = self.joueur_dao.creer(joueur)
                joueur_data['boost_stole']=joueur_stats["boost"]['count_stolen_big']
                conserver_equipe.append(joueur_data)

            # Calcul des statistiques de l'équipe
            stats_equipe = calculer_stats_equipe(conserver_equipe)

            # Construire les données de l'équipe
            equipe_stats = {
                "match_id": replay,
                "equipe_nom": team_name,
                "equipe_score": 0,
                "shots": stats_equipe['shots'],
                "goals": stats_equipe['goals'],
                "saves": stats_equipe['saves'],
                "assists": stats_equipe['assists'],
                "score": stats_equipe['score'],
                "demo_inflige": stats_equipe['demo_inflige'],
                "demo_recu": stats_equipe['demo_recu'],
                "boost_stole": stats_equipe["boost_stole"],
                "shooting_percentage": round(
                    (stats_equipe['goals'] / stats_equipe['shots'] * 100) if stats_equipe['shots'] > 0 else 0, 2
                ),
                "time_defensive_third": stats_equipe['time_defensive_third'],
                "time_neutral_third": stats_equipe['time_offensive_third'],
                "time_offensive_third": stats_equipe['time_offensive_third'],
                "date": date,
                "region": region,
                "stage": stage,
                "ligue": ligue,
            }

            # Calcul des indices de l'équipe
            equipe = Equipe(**equipe_stats)
            equipe.indice_performance = round(
                (
                    equipe.goals * 1 +
                    equipe.assists * 0.75 +
                    equipe.saves * 0.6 +
                    equipe.shots * 0.4 +
                    (equipe.goals / equipe.shots) * 0.5 if equipe.shots > 0 else 0
                ), 2
            )
            equipe.indice_de_pression = round(
                (
                    equipe.boost_stole / 10 +
                    equipe.goals / 1.05 +
                    equipe.shots / 3.29 +
                    equipe.demo_inflige / 0.56 +
                    equipe.time_offensive_third / 201.1
                ), 2
            )

            # Enregistrer l'équipe dans la base de données
            result_equipe = self.equipe_dao.creer(equipe)
            conserver_match.append(equipe)

        # Déterminer le gagnant du match
        if conserver_match[0].goals > conserver_match[1].goals:
            score1 = 1
            score2 = 0
        else:
            score1 = 0
            score2 = 1

        # Construire les données du match
        match_data = {
            "match_id": replay,
            "equipe1": conserver_match[0].equipe_nom,
            "equipe2": conserver_match[1].equipe_nom,
            "date": date,
            "region": region,
            "stage": stage,
            "ligue": ligue,
            "perso": False,
            "score1": score1,
            "score2": score2,
            "cote_equipe1": 2.0,
            "cote_equipe2": 2.0,
        }

        # Enregistrer le match dans la base de données
        match = Match(**match_data)
        result_match = self.match_dao.creer(match)





def calculer_stats_equipe(joueurs):
    """
    Calcule les statistiques totales d'une équipe en additionnant les statistiques de chaque joueur.

    Parameters
    ----------
    joueurs : list[dict]
        Liste des dictionnaires contenant les statistiques individuelles des joueurs.

    Returns
    -------
    dict
        Un dictionnaire contenant les statistiques totales de l'équipe.
    """
    # Initialiser les stats de l'équipe
    stats_equipe = {
        "shots": 0,
        "goals": 0,
        "saves": 0,
        "assists": 0,
        "score": 0,
        "demo_inflige": 0,
        "demo_recu": 0,
        "time_offensive_third": 0,
        "time_defensive_third": 0,
        "time_neutral_third": 0,
        "boost_stole": 0
    }

    # Additionner les statistiques de chaque joueur
    for joueur in joueurs:
        stats_equipe["shots"] += joueur["shots"]
        stats_equipe["goals"] += joueur["goals"]
        stats_equipe["saves"] += joueur["saves"]
        stats_equipe["assists"] += joueur["assists"]
        stats_equipe["score"] += joueur["score"]
        stats_equipe["demo_inflige"] += joueur["demo_inflige"]
        stats_equipe["demo_recu"] += joueur["demo_recu"]
        stats_equipe["time_offensive_third"] += joueur["time_offensive_third"]
        stats_equipe["time_defensive_third"] += joueur["time_defensive_third"]
        stats_equipe["time_neutral_third"] += joueur["time_neutral_third"]
        stats_equipe["boost_stole"] += joueur["boost_stole"]

    return stats_equipe


BallchasingAPI().add_world()
BallchasingAPI().add_major2()

BallchasingAPI().add_world2()
