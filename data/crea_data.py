


import requests,json # truc à importer
import pandas as pd
import os
from sqlalchemy import create_engine
import dotenv

couleur = ['blue','orange']



# Charger les variables d'environnement
dotenv.load_dotenv()

# Connexion à PostgreSQL
db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(db_url)

# Récupérer les résultats de la requête API
url = "https://api.rlcstatistics.net/matches?page=1&page_size=100000000"
response = requests.get(url)
resp = response.json()
match_list = []
n = len(resp['matches'])

for i in range(0,n):
   match_list.append(resp['matches'][i]['id_match'])

filtered_matches = []
filtered_players = []

match_data_list = []

for l in range(0,len(match_list)) :
    url_match = "https://api.rlcstatistics.net/match/" + match_list[l]
    resp2 = requests.get(url_match)
    match_data = resp2.json()
    match_data_list.append(match_data)

# Parcourir chaque match
for m in range(0,len(match_data_list)):



    match_data = match_data_list[m]
    if match_data == {'detail': 'Match Unknown'}:
        print("Erreur : Match Unknown. Aucun traitement effectué.")
        
    # Détails du match
    ligue = match_data['event']['name']
    region = match_data['event']['region']
    stage = match_data['stage']['name']
    date = match_data['date']

    # Parcourir chaque équipe (bleue et orange)
    for couleur in ['blue', 'orange']:
        equipe_nom = match_data[couleur]['team']['team']['name']
        equipe_image = match_data[couleur]['team']['team']['image']
        equipe_score = match_data[couleur]['score']
        equipe_winner = match_data[couleur]['winner']
        stats_core = match_data[couleur]['team']['stats']['core']

        # Stats équipe
        equipe_stats = {
            "match_id": match_data["_id"],
            "equipe_nom": equipe_nom,
            "equipe_image": equipe_image,
            "equipe_score": equipe_score,
            "equipe_winner": equipe_winner,
            "shots": stats_core['shots'],
            "goals": stats_core['goals'],
            "saves": stats_core['saves'],
            "assists": stats_core['assists'],
            "score": stats_core['score'],
            "shooting_percentage": stats_core['shootingPercentage'],
            "date": date,
            "ligue": ligue,
            "region": region,
            "stage": stage
        }
        filtered_matches.append(equipe_stats)

        # Parcourir les joueurs de l'équipe (3 joueurs par équipe)
        for j in range(3):
            joueur_stats = match_data[couleur]['players'][j]
            joueur_nom = joueur_stats['player']['tag']
            joueur_nationalite = joueur_stats['player']['country']
            joueur_core = joueur_stats['stats']['core']

            # Statistiques du joueur
            joueur_data = {
                "match_id": match_data["_id"],
                "equipe_nom": equipe_nom,
                "joueur_nom": joueur_nom,
                "nationalite": joueur_nationalite,
                "shots": joueur_core['shots'],
                "goals": joueur_core['goals'],
                "saves": joueur_core['saves'],
                "assists": joueur_core['assists'],
                "score": joueur_core['score'],
                "shooting_percentage": joueur_core['shootingPercentage'],
                "demo_infligées": joueur_stats['stats']['demo']['inflicted'],
                "demo_reçues": joueur_stats['stats']['demo']['taken'],
                "goal_participation": joueur_stats['advanced']['goalParticipation'],
                "rating": joueur_stats['advanced']['rating'],
                "time_defensive_third": joueur_stats['stats']['positioning']['timeDefensiveThird'],
                "time_neutral_third": joueur_stats['stats']['positioning']['timeNeutralThird'],
                "time_offensive_third": joueur_stats['stats']['positioning']['timeOffensiveThird']
            }
            filtered_players.append(joueur_data)

# Créer des DataFrames pour les équipes et les joueurs
df_filtered_matches = pd.DataFrame(filtered_matches)
df_filtered_players = pd.DataFrame(filtered_players)

# Sauvegarder le DataFrame des équipes dans la table matches
try:
    df_filtered_matches.to_sql('matches', con=engine, if_exists='append', index=False)
    print("Données des équipes enregistrées avec succès dans la base de données.")
except Exception as e:
    print(f"Erreur lors de l'enregistrement des équipes : {e}")

# Sauvegarder le DataFrame des joueurs dans la table players
try:
    df_filtered_players.to_sql('players', con=engine, if_exists='append', index=False)
    print("Données des joueurs enregistrées avec succès dans la base de données.")
except Exception as e:
    print(f"Erreur lors de l'enregistrement des joueurs : {e}")
