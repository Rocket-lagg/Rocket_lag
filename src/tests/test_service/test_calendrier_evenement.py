import os
import pytest
from datetime import datetime
from unittest.mock import patch

from service.calendrier_evenement import CalendrierEvenement


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_rechercher_match_par_date():
    # Cas 1: Date avec un match existant (le 8 octobre 2024)
    date = "2024-10-08T22:00:00Z"
    print(f"Test pour la date avec match : {date}")
    CalendrierEvenement.rechercher_match_par_date(date)

    # Cas 2: Date avec un autre match existant (le 8 décembre 2024)
    date = "2024-12-08T22:00:00Z"
    print(f"\nTest pour une autre date avec match : {date}")
    CalendrierEvenement().rechercher_match_par_date(date)

    # Cas 3: Date sans match
    date = "2024-11-01T22:00:00Z"
    print(f"\nTest pour la date sans match : {date}")
    CalendrierEvenement().rechercher_match_par_date(date)


# Exécution du test
test_rechercher_match_par_date()


if __name__ == "__main__":
    pytest.main([__file__])
