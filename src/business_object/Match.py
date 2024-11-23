class Match:
    """
    Représente un match de sport avec toutes ses informations associées.

    Attributs
    ---------
    match_id : int
        Identifiant unique du match.
    equipe1 : str
        Nom de la première équipe.
    equipe2 : str
        Nom de la deuxième équipe.
    score1 : int
        Score de la première équipe.
    score2 : int
        Score de la deuxième équipe.
    date : datetime
        Date et heure du match.
    ligue : str
        Nom de la ligue ou compétition dans laquelle se déroule le match.
    region : str
        Région où le match se joue.
    stage : str
        Phase ou étape du match (par exemple : "quart de finale").
    perso : bool, optionnel
        Indique si le match a été créé de manière personnalisée par l'utilisateur.
        Par défaut, cette valeur est `False`.
    cote_equipe1 : float, optionnel
        Cote associée à la première équipe. Par défaut, elle est de `2`.
    cote_equipe2 : float, optionnel
        Cote associée à la deuxième équipe. Par défaut, elle est de `2`.
    """
    
    def __init__(
        self,
        match_id,
        equipe1,
        equipe2,
        score1,
        score2,
        date,
        ligue,
        region,
        stage,
        perso=False,  # Valeur par défaut pour `perso`
        cote_equipe1=2,
        cote_equipe2=2
    ):
        self.match_id = match_id
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.score1 = score1
        self.score2 = score2
        self.date = date
        self.stage = stage
        self.region = region
        self.ligue = ligue
        self.perso = perso
        self.cote_equipe1 = cote_equipe1
        self.cote_equipe2 = cote_equipe2

        def __str__(self):
            """
            Retourne une représentation sous forme de chaîne de caractères des informations du joueur.

            Retour:
            -------
            str :
                Représentation du joueur avec toutes ses informations personnelles et statistiques.
            """
            return (f"Match({self.match_id}, ")
