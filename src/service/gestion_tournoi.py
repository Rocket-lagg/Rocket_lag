import sqlite3

############### on va définir ici la classe tornoi avec ses 3 fonctiuonnalitées et qui va me permettre de gérer
############### des tournois qui seront crées par mes utilisateurs viusiteurs ( uniquement). il est à noter que pour les matchs offiels,
################ cela se fezra directement via Api.


class Tournoi:
    def __init__(self, nom_tournoi, createur, officiel=False, db_name="tournois.db"):
        self.nom_tournoi = nom_tournoi
        self.createur = createur
        self.officiel = officiel
        self.equipes = []
        self.matchs = []
        self.conn = sqlite3.connect(db_name)
