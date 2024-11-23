import os
import requests
from dotenv import load_dotenv

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
        all_replays = ballchasing_api.compile_groups(group_id)
        if all_replays:
            for i in range(len(all_replays)):
                replay_id = all_replays[i]
                match_details = ballchasing_api.match_data(replay_id)
                match_process(replay)

    def add_world(self):
        group_id = "2-playoffs-48kyvcspq9"
        all_replays = ballchasing_api.compile_groups(group_id)
        if all_replays:
            for i in range(len(all_replays)):
                replay_id = all_replays[i]
                match_details = ballchasing_api.match_data(replay_id)
                match_process(replay)
        group_id ="1-swiss-stage-4ws5jld17r"
        all_replays = ballchasing_api.compile_groups(group_id)
        ligue="RLCS 2024 WORLDS"
        stage ="Swiss stage"
        region="INT"
        if all_replays:
            for i in range(len(all_replays)):
                replay_id = all_replays[i]
                match_details = ballchasing_api.match_data(replay_id)
                match_process(replay)

    def match_process(self,replay,ligue,stage,region):
            team_blue = match_data.get("blue", {}).get("name", "Équipe inconnue")
            team_orange = match_data.get("orange", {}).get("name", "Équipe inconnue")
            date = match_data.get("date", "Date inconnue")
            players_blue = [player.get("name", "Joueur inconnu") for player in match_data.get("blue", {}).get("players", [])]
            players_orange = [player.get("name", "Joueur inconnu") for player in match_data.get("orange", {}).get("players", [])]


            perso = False

            for j in range(3):  # Assume 3 players per team
                shots = match_data["blue"]["players"][i]["stats"]["core"]["shots"]
                joueur_nom = players_blue[j]
                joueur_nationalite = "inconnu"
                joueur_goals = match_data["blue"]["players"][i]["stats"]["core"]["goals"]
                joueur_core



            match1 = {
                "date": date,
                "stage": stage,
                "ligue": ligue,
                "region": region,
                "score1": equipe_score_blue,
                "score2": equipe_score_orange,
                "equipe1": team_blue,  # Nom de l'équipe
                "equipe2": team_orange,  # Nom de l'équipe
                "perso": perso,
                "cote_equipe1" = 2.0,
                "cote_equipe2" = 2.0
            }

            # Créer l'objet Match et l'enregistrer

            result_match = self.match_dao.add_match(match1)
              shots = match_data["blue"]["players"][i]["stats"]["core"]["shots"]
