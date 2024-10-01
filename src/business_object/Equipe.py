class Equipe:
     """
    Classe représentant un Joueur

    Attributs
    ----------
    id_joueur : int
        identifiant
    pseudo : str
        pseudo du joueur
    mdp : str
        le mot de passe du joueur
    age : int
        age du joueur
    mail : str
        mail du joueur
    fan_pokemon : bool
        indique si le joueur est un fan de Pokemon
    """

    def __init__(self, match_id, equipe_nom, equipe_image, equipe_score, equipe_winner,
                 shots, goals, saves, assists, score, shooting_percentage, date, ligue,
                  region, stage,):

        self.match_id = match_id                     # ID du match
        self.equipe_nom = equipe_nom                 # Nom de l'équipe
        self.equipe_image = equipe_image             # Image de l'équipe
        self.equipe_score = equipe_score             # Score de l'équipe
        self.equipe_winner = equipe_winner           # Vainqueur (booléen ou indicatif)
        self.shots = shots                           # Nombre de tirs
        self.goals = goals                           # Nombre de buts
        self.saves = saves                           # Sauvegardes
        self.assists = assists                       # Assistances
        self.score = score                           # Score total
        self.shooting_percentage = shooting_percentage  # Pourcentage de tir
        self.date = date                             # Date du match
        self.ligue = ligue                           # Ligue du match
        self.region = region                         # Région du match
        self.stage = stage                           # Étape du tournoi ou du match

    # Méthode pour afficher les informations du match
   def __str__(self):
        """Permet d'afficher les informations de l'equipe"""
        return f"Joueur({self.pseudo}, {self.age} ans)"

    def afficher_statistiques(self) -> list[str]:
        """Retourne les attributs de l'equipe"""
        return [self.pseudo, self.age, self.mail, self.fan_pokemon]
        # pas fait
