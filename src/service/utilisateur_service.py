from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.Utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDao


class UtilisateurService:
    """Classe contenant les méthodes de service des utilisateurs"""

    @log
    def creer_utilisateur(
        self, nom_utilisateur, mot_de_passe, email, tournois_crees=None, points=0, paris=None
    ) -> Utilisateur:
        """Création d'un utilisateur à partir de ses attributs"""

        nouveau_utilisateur = Utilisateur(
            nom_utilisateur=nom_utilisateur,
            mot_de_passe=hash_password(mot_de_passe, nom_utilisateur),
            email=email,
            tournois_crees=tournois_crees,
            points=points,
            paris=paris,
        )

        return nouveau_utilisateur if UtilisateurDao().creer(nouveau_utilisateur) else None

    @log
    def lister_tous(self, inclure_mot_de_passe=False) -> list[Utilisateur]:
        """Lister tous les utilisateurs
        Si inclure_mot_de_passe=True, les mots de passe seront inclus
        Par défaut, tous les mot_de_passe des utilisateurs sont à None
        """
        utilisateurs = UtilisateurDao().lister_tous()
        if not inclure_mot_de_passe:
            for j in utilisateurs:
                j.mot_de_passe = None
        return utilisateurs

    @log
    def trouver_par_id(self, id_utilisateur) -> Utilisateur:
        """Trouver un utilisateur à partir de son id"""
        return UtilisateurDao().trouver_par_id(id_utilisateur)

    @log
    def modifier(self, utilisateur) -> Utilisateur:
        """Modification d'un utilisateur"""

        utilisateur.mot_de_passe = hash_password(
            utilisateur.mot_de_passe, utilisateur.nom_utilisateur
        )
        return utilisateur if UtilisateurDao().modifier(utilisateur) else None

    @log
    def supprimer(self, utilisateur) -> bool:
        """Supprimer le compte d'un utilisateur"""
        return UtilisateurDao().supprimer(utilisateur)

    @log
    def afficher_tous(self) -> str:
        """Afficher tous les utilisateurs
        Sortie : Une chaine de caractères mise sous forme de tableau
        """
        entetes = ["nom_utilisateur", "age", "email", "est fan de Pokemon"]

        utilisateurs = UtilisateurDao().lister_tous()

        for j in utilisateurs:
            if j.nom_utilisateur == "admin":
                utilisateurs.remove(j)

        utilisateurs_as_list = [j.as_list() for j in utilisateurs]

        str_utilisateurs = "-" * 100
        str_utilisateurs += "\nListe des utilisateurs \n"
        str_utilisateurs += "-" * 100
        str_utilisateurs += "\n"
        str_utilisateurs += tabulate(
            tabular_data=utilisateurs_as_list,
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f",
        )
        str_utilisateurs += "\n"

        return str_utilisateurs

    @log
    def se_connecter(self, nom_utilisateur, mot_de_passe) -> Utilisateur:
        """Se connecter à partir de nom_utilisateur et mot_de_passe"""
        return UtilisateurDao().se_connecter(
            nom_utilisateur, hash_password(mot_de_passe, nom_utilisateur)
        )

    @log
    def nom_utilisateur_deja_utilise(self, nom_utilisateur) -> bool:
        """Vérifie si le nom_utilisateur est déjà utilisé
        Retourne True si le nom_utilisateur existe déjà en BDD"""
        utilisateurs = UtilisateurDao().lister_tous()
        return nom_utilisateur in [j.nom_utilisateur for j in utilisateurs]
