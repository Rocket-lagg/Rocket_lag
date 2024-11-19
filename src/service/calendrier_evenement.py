from datetime import datetime
from dao.match_dao import MatchDao
import calendar


class CalendrierEvenement:

    def __init__(self):
        self.match_dao = MatchDao()

    def dictionnaire_evenement(self, annee):
        # Dictionnaire des événements par jour (clé = (mois, jour), valeur = événement)
        all_matchs = self.match_dao.lister_tous()
        evenements = {}
        for match in all_matchs:
            print(match.date)
            date = match.date
            if date.year == annee:
                evenements[(date.month, date.day)] = (
                    f"{match.ligue}: {match.equipe1} vs {match.equipe2} à {date.hour}h{date.minute} "
                )
        return evenements

    # Fonction pour afficher un calendrier d'une année complète avec des événements
    def afficher_calendrier_annee(self, annee):
        evenements = CalendrierEvenement().dictionnaire_evenement(annee)
        print(f"Calendrier pour l'année {annee} :\n")
        # Pour chaque mois de l'année
        for mois in range(1, 13):
            print(calendar.month_name[mois], annee)
            print("Lu Ma Me Je Ve Sa Di")  # En-tête des jours de la semaine

            # Obtenir le calendrier du mois sous forme de tableau
            tableau_mois = calendar.monthcalendar(annee, mois)

            # Afficher les jours du mois et ajouter des événements s'il y en a
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
                print(" ".join(ligne))

            print()  # Saut de ligne entre les mois

        # Liste des événements
        print("Événements de l'année :")
        for (mois, jour), evenement in evenements.items():
            print(f"{calendar.month_name[mois]} {jour} : {evenement}")

    def rechercher_match_par_date(self, dates):
        match_dao = MatchDao()
        liste_match = match_dao.trouver_par_dates(dates)

        if liste_match == []:
            print(f"Il n'y a aucun match le {dates}")
        else:

            print(f"Match du {dates}")
            for match in liste_match:

                print(f"{match.ligue}: {match.equipe1} vs {match.equipe2} le {dates} ")


r = CalendrierEvenement()

r.afficher_calendrier_annee(2024)
