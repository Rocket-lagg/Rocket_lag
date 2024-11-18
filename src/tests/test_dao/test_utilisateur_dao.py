import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.utilisateur_dao import UtilisateurDao

from business_object.Utilisateur import Utilisateur


@pytest.fixture(scope="session", autouse=True)
# def setup_test_environment():
#    """Initialisation des données de test"""
#    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
#        ResetDatabase().lancer(test_dao=True)
#       yield


def test_trouver_par_id_existant():
    """Recherche par id d'un utilisateur existant"""

    # GIVEN
    id_utilisateur = 997

    # WHEN
    utilisateur = UtilisateurDao().trouver_par_id(id_utilisateur)

    # THEN
    assert utilisateur is not None


def test_trouver_par_id_non_existant():
    """Recherche par id d'un utilisateur n'existant pas"""

    # GIVEN
    id_utilisateur = 9999999999999

    # WHEN
    utilisateur = UtilisateurDao().trouver_par_id(id_utilisateur)

    # THEN
    assert utilisateur is None


def test_lister_tous():
    """Vérifie que la méthode renvoie une liste de Utilisateur
    de taille supérieure ou égale à 2
    """

    # GIVEN

    # WHEN
    utilisateurs = UtilisateurDao().lister_tous()

    # THEN
    assert isinstance(utilisateurs, list)
    for j in utilisateurs:
        assert isinstance(j, Utilisateur)
    assert len(utilisateurs) >= 2


def test_creer_ok():
    """Création de Utilisateur réussie"""

    # GIVEN
    utilisateur = Utilisateur(
        nom_utilisateur="test", mot_de_passe="1234", email="test@mail.fr", tournois_crees=[], points=10, paris=[]
    )

    # WHEN
    creation_ok = UtilisateurDao().creer(utilisateur)

    # THEN
    assert creation_ok
    assert utilisateur.id_utilisateur


def test_creer_ko():
    """Création de Utilisateur échouée (mail incorrects)"""

    # GIVEN
    utilisateur = Utilisateur(
        nom_utilisateur="zerty", mot_de_passe="1234", email=12, tournois_crees=[], points=0, paris=[]
    )

    # WHEN
    creation_ok = UtilisateurDao().creer(utilisateur)

    # THEN
    assert not creation_ok


def test_modifier_ok():
    """Modification de Utilisateur réussie"""

    # GIVEN
    new_email = "maurice@mail.com"
    utilisateur = Utilisateur(
        nom_utilisateur="maurice", mot_de_passe="1234", email=new_email, tournois_crees=[], points=666, paris=[]
    )

    # WHEN
    modification_ok = UtilisateurDao().modifier(utilisateur)

    # THEN
    assert modification_ok


def test_modifier_ko():
    """Modification de Utilisateur échouée (id inconnu)"""

    # GIVEN
    utilisateur = Utilisateur(
        nom_utilisateur="test", mot_de_passe="1234", email="test@mail.fr", tournois_crees=[], points=666, paris=[]
    )

    # WHEN
    modification_ok = UtilisateurDao().modifier(utilisateur)

    # THEN
    assert not modification_ok


def test_supprimer_ok():
    """Suppression de Utilisateur réussie"""

    # GIVEN
    utilisateur = Utilisateur(nom_utilisateur="miguel", email="miguel@projet.fr")

    # WHEN
    suppression_ok = UtilisateurDao().supprimer(utilisateur)

    # THEN
    assert suppression_ok


def test_supprimer_ko():
    """Suppression de Utilisateur échouée (id inconnu)"""

    # GIVEN
    utilisateur = Utilisateur(
        nom_utilisateur="id inconnu", mot_de_passe="1234", email="jp@mail.fr", tournois_crees=[], points=0, paris=[]
    )

    # WHEN
    suppression_ok = UtilisateurDao().supprimer(utilisateur)

    # THEN
    assert not suppression_ok


def test_se_connecter_ok():
    """Connexion de Utilisateur réussie"""

    # GIVEN
    nom_utilisateur = "batricia"
    mot_de_passe = "9876"

    # WHEN
    utilisateur = UtilisateurDao().se_connecter(nom_utilisateur, mot_de_passe)  # hash_password(mot_de_passe, nom_utilisateur)

    # THEN
    assert isinstance(utilisateur, Utilisateur)


def test_se_connecter_ko():
    """Connexion de Utilisateur échouée (nom_utilisateur ou mot_de_passe incorrect)"""

    # GIVEN
    nom_utilisateur = "toto"
    mot_de_passe = "poiuytreza"

    # WHEN
    utilisateur = UtilisateurDao().se_connecter(nom_utilisateur, hash_password(mot_de_passe, nom_utilisateur))

    # THEN
    assert not utilisateur


if __name__ == "__main__":
    pytest.main([__file__])
