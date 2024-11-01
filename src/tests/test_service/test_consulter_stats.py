import pytest
from unittest.mock import patch, MagicMock
from service.consulter_stats import ConsulterStats


@pytest.fixture
def consulter_stats():
    return ConsulterStats()


class TestStatsJoueurs:

    @patch("dao.joueur_dao.JoueurDao")
    @patch("dao.match_dao.MatchDao")
    def test_stats_joueurs_nom_valide(self, MockMatchDao, MockJoueurDao, consulter_stats):
        nom_joueur = "Crispy"
        # Simule un joueur avec des statistiques fictives
        joueur_fictif = MagicMock(
            region="EU",
            equipe="RocketLag",
            goals=5,
            assists=3,
            shots=12,
            saves=4,
            score=1500,
            shooting_percentage=40,
            demo_inflige=3,
            time_offensive_third=60,
        )

        # Mock des méthodes de DAO pour obtenir les statistiques
        MockJoueurDao.return_value.obtenir_par_nom.return_value = joueur_fictif
        MockMatchDao.return_value.trouver_id_match_par_joueur.return_value = [1, 2, 3]

        # Capture l'affichage des statistiques
        with patch("sys.stdout", new_callable=MagicMock()) as mock_stdout:
            consulter_stats.stats_joueurs(nom_joueur)
            output = mock_stdout.write.call_args[0][0]

            assert "Statistiques pour le joueur Crispy" in output
            assert "RocketLag" in output
            assert "Total de buts : 5" in output
            assert "Nombre moyen de buts par matchs : 1.67" in output  # 5 / 3 matchs
            assert "Son indice de performance au cours de la saison est égal à :" in output
            assert "Son indice offensif au cours de la saison est égal à :" in output

    @patch("dao.joueur_dao.JoueurDao")
    def test_stats_joueurs_joueur_non_trouve(self, MockJoueurDao, consulter_stats):
        nom_joueur = "Inconnu"
        # Mock pour simuler qu'aucun joueur n'a été trouvé
        MockJoueurDao.return_value.obtenir_par_nom.return_value = None

        with pytest.raises(ValueError, match="Aucun joueur nommé Inconnu n'a été trouvé."):
            consulter_stats.stats_joueurs(nom_joueur)

    def test_stats_joueurs_type_erreur(self, consulter_stats):
        # Vérifie qu'un TypeError est levé pour un type de nom incorrect
        with pytest.raises(TypeError, match="nom_joueur doit être une instance de str"):
            consulter_stats.stats_joueurs(123)

    @patch("dao.joueur_dao.JoueurDao")
    @patch("dao.match_dao.MatchDao")
    def test_stats_joueurs_region_inconnue(self, MockMatchDao, MockJoueurDao, consulter_stats):
        nom_joueur = "Crispy"
        # Simule un joueur avec une région inconnue
        joueur_fictif = MagicMock(
            region="UNKNOWN",
            equipe="RocketLag",
            goals=3,
            assists=2,
            shots=8,
            saves=1,
            score=1000,
            shooting_percentage=33,
            demo_inflige=1,
            time_offensive_third=30,
        )

        MockJoueurDao.return_value.obtenir_par_nom.return_value = joueur_fictif
        MockMatchDao.return_value.trouver_id_match_par_joueur.return_value = [1]

        # Vérifie qu'une ValueError est levée pour une région inconnue
        with pytest.raises(ValueError, match="La région du joueur est inconnue."):
            consulter_stats.stats_joueurs(nom_joueur)
