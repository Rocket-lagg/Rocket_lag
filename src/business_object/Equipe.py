from business_object.EntiteSportive import EntiteSportive


class Equipe(EntiteSportive):
    """
    Classe représentant une équipe dans un match, héritant des statistiques d'une entité sportive.

    Attributs hérités de EntiteSportive:
    ------------------------------------
    match_id : int
        Identifiant unique du match.

    equipe_nom : str
        Nom de l'équipe ou de l'entité sportive.

    shots : int
        Nombre de tirs effectués par l'équipe.

    goals : int
        Nombre de buts marqués par l'équipe.

    saves : int
        Nombre d'arrêts effectués par l'équipe.

    assists : int
        Nombre de passes décisives réalisées par l'équipe.

    score : int
        Score total obtenu par l'équipe dans le match.

    shooting_percentage : float
        Pourcentage de réussite des tirs (nombre de buts par rapport au nombre de tirs).

    time_offensive_third : float
        Temps passé dans le tiers offensif du terrain par l'équipe.

    time_defensive_third : float
        Temps passé dans le tiers défensif du terrain par l'équipe.

    time_neutral_third : float
        Temps passé dans le tiers neutre du terrain par l'équipe.

    demo_inflige : int
        Nombre de démolitions infligées à l'équipe adverse par l'équipe.

    demo_recu : int
        Nombre de démolitions reçues par l'équipe.

    goal_participation : float
        Taux de participation aux buts, calculé comme la somme des buts et des
        passes décisives divisée par le nombre total de buts marqués par
        l'équipe.

    Nouveaux attributs propres à Equipe:
    ------------------------------------
    equipe_score : int
        Score total obtenu par l'équipe dans le match.

    equipe_winner : bool
        Indicateur si l'équipe a gagné le match (True pour gagnante, False pour perdante).

    region : str
        Région géographique à laquelle l'équipe appartient.


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
        equipe_score,
        boost_stole,
        date,
        region,
        ligue,
        stage,
        shots_par_match=1,  # valeur par défaut 1
        goals_par_match=1,  # valeur par défaut 1
        saves_par_match=1,  # valeur par défaut 1
        assists_par_match=1,  # valeur par défaut 1
        score_par_match=1,  # valeur par défaut 1
        demo_inflige_par_match=1,
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

        assert isinstance(region, str), "region doit être une chaîne de caractères"
        assert isinstance(ligue, str), "ligue doit être une chaîne de caractères"
        assert isinstance(stage, str), "stage doit être une chaîne de caractères"

        # Initialisation des nouveaux attributs spécifiques à la classe Equipe
        self.equipe_score = equipe_score
        self.boost_stole = boost_stole

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères des informations de l'équipe.

        Retour:
        -------
        str :
            Représentation de l'équipe avec son nom, son score et sa région.
        """
        return f"Equipe({self.equipe_nom}, Score: {self.equipe_score}, Région: {self.region})"
