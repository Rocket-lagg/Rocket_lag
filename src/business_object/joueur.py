from business_object.EntiteSportive import EntiteSportive


class Joueur(EntiteSportive):
    """
    Classe représentant un joueur, héritant des statistiques d'une entité sportive.

    Attributs hérité de EntiteSportive:
    -----------------------------------
    match_id : int
        Identifiant unique du match.

    equipe_nom : str
        Nom de l'équipe à laquelle le joueur appartient.

    shots : int
        Nombre de tirs effectués par le joueur.

    goals : int
        Nombre de buts marqués par le joueur.

    saves : int
        Nombre d'arrêts effectués par le joueur.

    assists : int
        Nombre de passes décisives réalisées par le joueur.

    score : int
        Score total obtenu par l'équipe dans le match.

    shooting_percentage : float
        Pourcentage de réussite des tirs (nombre de buts par rapport au nombre de tirs).

    time_offensive_third : float
        Temps passé dans le tiers offensif du terrain par le joueur.

    time_defensive_third : float
        Temps passé dans le tiers défensif du terrain par le joueur.

    time_neutral_third : float
        Temps passé dans le tiers neutre du terrain par le joueur.

    demo_inflige : int
        Nombre de démolitions infligées à l'équipe adverse par le joueur.

    demo_recu : int
        Nombre de démolitions reçues par le joueur.

    goal_participation : float
        Taux de participation aux buts, calculé comme la somme des buts et des
        passes décisives divisée par le nombre total de buts marqués par
        l'équipe.

    Nouveaux Attributs propres à Joueur:
    ------------------------------------
    nom : str
        Nom du joueur.

    nationalite : str
        Nationalité du joueur.

    rating : float
        Note ou évaluation de la performance du joueur.
    """

    def __init__(
        self,
        match_id,
        equipe_nom,
        shots,
        goals,
        saves,
        assists,
        score,
        shooting_percentage,
        time_offensive_third,
        time_defensive_third,
        time_neutral_third,
        demo_inflige,
        demo_recu,
        goal_participation,
        nom,
        nationalite,
        rating,
        date,
        region,
        ligue,
        stage,
        # Paramètres avec valeurs par défaut pour les statistiques moyennes par match
        shots_par_match=1,  # valeur par défaut 1
        goals_par_match=1,  # valeur par défaut 1
        saves_par_match=1,  # valeur par défaut 1
        assists_par_match=1,  # valeur par défaut 1
        score_par_match=1,  # valeur par défaut 1
        demo_inflige_par_match=1,  # valeur par défaut 1
        # Paramètres additionnels
        indice_offensif=1,
        indice_performance=1
    ):
        # Appel du constructeur parent (EntiteSportive)
        super().__init__(
            match_id,
            equipe_nom,
            shots,
            goals,
            saves,
            assists,
            score,
            shooting_percentage,
            time_offensive_third,
            time_defensive_third,
            time_neutral_third,
            demo_inflige,
            demo_recu,
            date,
            region,
            ligue,
            stage,
        )

        # Vérifications des types pour les nouveaux attributs spécifiques à Joueur
        assert isinstance(nom, str), "nom doit être une chaîne de caractères"
        assert isinstance(nationalite, str), "nationalite doit être une chaîne de caractères"
        assert isinstance(rating, float), "rating doit être un flottant"

        # Initialisation des nouveaux attributs spécifiques à Joueur
        self.nom = nom
        self.nationalite = nationalite
        self.rating = rating
        self.demo_inflige = demo_inflige
        self.goal_participation = goal_participation
        self.shots_par_match = shots_par_match
        self.goals_par_match = goals_par_match
        self.saves_par_match = saves_par_match
        self.assists_par_match = assists_par_match
        self.score_par_match = score_par_match
        self.demo_inflige_par_match = demo_inflige_par_match
        self.indice_offensif = indice_offensif
        self.indice_performance = indice_performance

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères des informations du joueur.

        Retour:
        -------
        str :
            Représentation du joueur avec toutes ses informations personnelles et statistiques.
        """
        return (f"Joueur({self.nom}, "
                f"Nationalité: {self.nationalite}, "
                f"Region: {self.region}, "
                f"Ligue: {self.ligue}, "
                f"Stage: {self.stage}, "
                f"Match ID: {self.match_id}, "
                f"Equipe: {self.equipe_nom}, "
                f"Shots: {self.shots}, "
                f"Goals: {self.goals}, "
                f"Saves: {self.saves}, "
                f"Assists: {self.assists}, "
                f"Score: {self.score}, "
                f"Shooting Percentage: {self.shooting_percentage}, "
                f"Time Offensive Third: {self.time_offensive_third}, "
                f"Time Defensive Third: {self.time_defensive_third}, "
                f"Time Neutral Third: {self.time_neutral_third}, "
                f"Demo Infligé: {self.demo_inflige}, "
                f"Demo Reçu: {self.demo_recu}, "
                f"Goal Participation: {self.goal_participation}, "
                f"Rating: {self.rating}, "
                f"Date: {self.date}, "
                f"Shots per Match: {self.shots_par_match}, "
                f"Goals per Match: {self.goals_par_match}, "
                f"Saves per Match: {self.saves_par_match}, "
                f"Assists per Match: {self.assists_par_match}, "
                f"Score per Match: {self.score_par_match}, "
                f"Demo Infligé per Match: {self.demo_inflige_par_match}, "
                f"Indice Offensif: {self.indice_offensif}, "
                f"Indice Performance: {self.indice_performance})")




