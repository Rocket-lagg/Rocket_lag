import dotenv
dotenv.load_dotenv()
from view.session import Session

def est_admin(pseudo):
    """
    Vérifie si l'utilisateur est dans la liste des administrateurs définie par une variable d'environnement.

    Parameters
    ----------
    pseudo : str
        Pseudo à vérifier.
    Returns
    ------
    bool : Bool
        True si l'utilisateur est un administrateur, sinon False.
    """
    nom_utilisateur = Session().utilisateur.nom_utilisateur
    return nom_utilisateur in os.environ['LIST_ADMIN']

print(est_admin('momo'))
