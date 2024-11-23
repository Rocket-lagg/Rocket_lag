from unittest.mock import MagicMock
from datetime import datetime
import pytest
from service.calendrier_evenement import CalendrierEvenement
from dao.match_dao import MatchDao
from dao.paris_dao import ParisDao

# Données de test
liste_matchs = [
    MagicMock(date=datetime(2025, 1, 15, 20, 30), ligue="Ligue 1", equipe1="Equipe A", equipe2="Equipe B"),
    MagicMock(date=datetime(2025, 1, 20, 18, 0), ligue="Ligue 2", equipe1="Equipe C", equipe2="Equipe D"),
]

liste_paris = [
    MagicMock(date=datetime(2025, 1, 10, 15, 45), tournoi="Tournoi X", equipe1="Equipe E", equipe2="Equipe F"),
    MagicMock(date=datetime(2025, 1, 20, 17, 0), tournoi="Tournoi Y", equipe1="Equipe G", equipe2="Equipe H"),
]





def test_rechercher_match_par_date_match_trouve(capsys):
    """Test de rechercher_match_par_date avec un match trouvé"""
    # GIVEN
    date_test = datetime(2025, 1, 15).date()
    MatchDao().trouver_par_dates = MagicMock(return_value=[liste_matchs[0]])
    calendrier = CalendrierEvenement()

    # WHEN
    calendrier.rechercher_match_par_date(date_test)

    # THEN
    captured = capsys.readouterr()
    output = captured.out
    assert "Match du 2025-01-15" in output
    assert "Ligue 1: Equipe A vs Equipe B" in output


def test_rechercher_match_par_date_aucun_match(capsys):
    """Test de rechercher_match_par_date avec aucun match trouvé"""
    # GIVEN
    date_test = datetime(2025, 1, 14).date()
    MatchDao().trouver_par_dates = MagicMock(return_value=[])
    calendrier = CalendrierEvenement()

    # WHEN
    calendrier.rechercher_match_par_date(date_test)

    # THEN
    captured = capsys.readouterr()
    output = captured.out
    assert f"Il n'y a aucun match le {date_test}" in output


if __name__ == "__main__":
    pytest.main([__file__])
