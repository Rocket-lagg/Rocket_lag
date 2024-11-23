from datetime import datetime
from dao.match_dao import MatchDao
from dao.paris_dao import ParisDao
import calendar
import logging


class CalendrierEvenement:

    def __init__(self):
        self.match_dao = MatchDao()
        self.pari_dao = ParisDao()

    def dictionnaire_evenement(self, annee, mois):
        """
        Récupère les événements de paris et de matchs pour une année et un mois donnés.

        Parameters
        ----------
        annee : int
            L'année pour laquelle les événements sont récupérés.
        mois : int
            Le mois pour lequel les événements sont récupérés (compris entre 1 et 12).

        Return
        ------
        evenements : dict
            Un dictionnaire des événements, où la clé est un tuple `(mois, jour)` et la valeur est une liste d'événements.
            Chaque événement est une chaîne de caractères décrivant le match ou le pari.
        """
        # Dictionnaire des événements par jour (clé = (mois, jour), valeur = liste d'événements)
        all_matchs = ParisDao().afficher_infos_paris()
        evenements = {}
        for match in all_matchs:
            date = match.date
            if date.year == annee and date.month == mois:
                # Construire la chaîne de l'événement
                evenement = (
                    f"{match.tournoi}: {match.equipe1} vs {match.equipe2} à {date.hour}h{date.minute}"
                )

                # Ajouter à la clé correspondante dans le dictionnaire
                if (date.month, date.day) not in evenements:
                    evenements[(date.month, date.day)] = (
                        []
                    )  # Initialiser une liste si la clé n'existe pas

                evenements[(date.month, date.day)].append(
                    evenement
                )  # Ajouter l'événement à la liste existante
        all_matchs_passes = self.match_dao.lister_tous()
        for match in all_matchs_passes:
            date = match.date
            if date.year == annee and date.month == mois:
                # Construire la chaîne de l'événement
                evenement = (
                    f"{match.ligue}: {match.equipe1} vs {match.equipe2} à {date.hour}h{date.minute}"
                )

                # Ajouter à la clé correspondante dans le dictionnaire
                if (date.month, date.day) not in evenements:
                    evenements[(date.month, date.day)] = (
                        []
                    )  # Initialiser une liste si la clé n'existe pas

                evenements[(date.month, date.day)].append(
                    evenement
                )  # Ajouter l'événement à la liste existante

        return evenements

    # Fonction pour afficher un calendrier d'une année complète avec des événements

    def afficher_calendrier_annee(self, annee, mois):
        """
        Affiche le calendrier d'un mois avec les événements associés.

        Parameters
        ----------
        annee : int
            L'année du calendrier à afficher.
        mois : int
            Le mois du calendrier à afficher (compris entre 1 et 12).

        Return
        ------
        evenements : dict
            Un dictionnaire des événements associés aux jours du mois, où la
            clé est un tuple (mois, jour) et la valeur est une liste d'événements.
            Cette valeur est retournée en cas d'erreur pour assurer la gestion des erreurs.
        """
        try:
            # Vérifications des entrées
            if not isinstance(annee, int):
                raise TypeError("L'année doit être un entier.")
            if not isinstance(mois, int) or not (1 <= mois <= 12):
                raise ValueError("Le mois doit être un entier entre 1 et 12.")

            # Récupération des événements
            evenements = CalendrierEvenement().dictionnaire_evenement(annee, mois)

            # Affichage du titre
            print(f"Calendrier pour {calendar.month_name[mois]} {annee} :\n")

            # En-tête des jours de la semaine
            print("Lu Ma Me Je Ve Sa Di")

            # Obtenir le calendrier du mois sous forme de tableau
            tableau_mois = calendar.monthcalendar(annee, mois)

            # Affichage du calendrier avec les événements
            for semaine in tableau_mois:
                ligne = []
                for jour in semaine:
                    if jour == 0:
                        ligne.append("  ")  # Jours en dehors du mois
                    else:
                        # Ajouter un astérisque s'il y a un événement pour ce jour
                        if (mois, jour) in evenements:
                            ligne.append(f"{jour:2}*")
                        else:
                            ligne.append(f"{jour:2}")
                print(" ".join(ligne))  # Afficher la semaine

            print()  # Ligne vide après le calendrier

            # Liste des événements
            print("Événements du mois :")
            for (mois_evt, jour), liste_evenements in evenements.items():
                print(f"{calendar.month_name[mois_evt]} {jour} :")
                for evenement in liste_evenements:
                    print(f"  - {evenement}")

        except Exception as e:
            # Gestion des erreurs
            logging.error(
                f"Une erreur s'est produite dans afficher_calendrier_annee: {e}"
            )
            print(f"Une erreur est survenue : {e}")
            return {}

    def rechercher_match_par_date(self, dates):
        """
        Recherche et affiche les matchs d'une date donnée.

        Cette méthode recherche les matchs programmés pour une date spécifique et les affiche.
        Si aucun match n'est trouvé pour cette date, un message indiquant l'absence de matchs est affiché.

        Parameters
        ----------
        dates : str
            La date sous forme de chaîne de caractères à rechercher (format : "YYYY-MM-DD").

        Return
        ------
        None
            Cette fonction n'a pas de valeur de retour. Elle se charge uniquement d'afficher les matchs ou l'absence de matchs.
        """
        match_dao = MatchDao()
        liste_match = match_dao.trouver_par_dates(dates)

        if liste_match == []:
            print(f"Il n'y a aucun match le {dates}")
        else:

            print(f"Match du {dates}")
            for match in liste_match:

                print(f"{match.ligue}: {match.equipe1} vs {match.equipe2} le {dates} ")


r = CalendrierEvenement()

print(r.dictionnaire_evenement(2025, 1))
