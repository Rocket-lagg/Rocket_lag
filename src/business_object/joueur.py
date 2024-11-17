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
        shots_par_match=1,
        goals_par_match=1,
        saves_par_match=1,
        assists_par_match=1,
        score_par_match=1,
        demo_inflige_par_match=1,
        # Paramètres additionnels
        indice_offensif=1,
        indice_performance=1,
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

        # Initialisation des nouveaux attributs
        self.nom = nom
        self.nationalite = nationalite
        self.rating = rating
        self.demo_inflige = demo_inflige
        self.goal_participation = goal_participation

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères des informations du joueur.

        Retour:
        -------
        str :
            Représentation du joueur avec son nom et d'autres informations personnelles.
        """
        return (
            f"Joueur({self.nom} \n"
            f"Nationalité: {self.nationalite} \n"
            f"Region: {self.region} \n"
            f"Ligue: {self.ligue} \n"
            f"Stage: {self.stage} \n"
            f"Match ID: {self.match_id} \n"
            f"Equipe: {self.equipe_nom} \n"
            f"Shots: {self.shots} \n"
            f"Goals: {self.goals} \n"
            f"Saves: {self.saves} \n"
            f"Assists: {self.assists} \n"
            f"Score: {self.score} \n"
            f"Shooting Percentage: {self.shooting_percentage} \n"
            f"Time Offensive Third: {self.time_offensive_third} \n"
            f"Time Defensive Third: {self.time_defensive_third} \n"
            f"Time Neutral Third: {self.time_neutral_third} \n"
            f"Demo Infligé: {self.demo_inflige}\n"
            f"Demo Reçu: {self.demo_recu}\n"
            f"Goal Participation: {self.goal_participation}\n"
            f"Rating: {self.rating} \n"
            f"Date: {self.date} \n"
        )
