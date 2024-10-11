class Pari:
    """
    Définit un pari pour un joueur
    Parameters:
    ---------------
    id_pari: int
     identifiant du pari

    id_match: int
     identifiant du match sur lequel est fait le pari

    id_equipe: Equipe
     identifiant de l'équipe sur laquelle le joueur place son pari

    id_vainqueur: Equipe
     identifiant du joueur qui remporte le pari

    cote_match: Match
     Cote sur le match du pari

    statut: str
     Etat du pari: "Remporté", "En cours"

    montant: int
     Montant mis en jeu dans le pari
    """

    def __init__(self, id_pari, id_match, id_equipe, id_vainqueur, cote_match, status, montant):
        self.id_pari = id_pari
        self.id_match = id_match
        self.id_equipe = id_equipe
        self.id_vainqueur = id_vainqueur
        self.cote_match = cote_match
        self.status = status
        self.montant = montant

    def __str__(self):
        """Affiche les informations du pari"""
        return f"Vous avez parié {self.montant} pour {self.id_equipe} dans le match {self.id_match}"

    def calculer_gains(self):
        """Donne les gains du pari"""
        if self.id_equipe == self.id_vainqueur:
            gain = self.montant * self.cote_match
        else:
            gain = -self.montant
        return gain
