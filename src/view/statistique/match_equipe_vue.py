from service.consulter_stats import ConsulterStats
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class MatchEquipeVue(VueAbstraite):
    """Une vue pour afficher les stats d'un match par équipe"""

    def __init__(self, message=""):
        self.message = message

    def message_info(self):
        print("Consultation des statstiques d'un match à partir du nom d'équipe")
