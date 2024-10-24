import regex
from InquirerPy import prompt
from InquirerPy.validator import PasswordValidator, EmptyInputValidator
from prompt_toolkit.validation import ValidationError, Validator
from view.vue_abstraite import VueAbstraite
from service.utilisateur_service import utilisateur_service


class Inscriptionview(VueAbstraite):
    def __init__(self):
        self.__questions = [
            {
                "type": "input",
                "name": "pseudo",
                "message": "Choisissez un pseudo : ",
            },
            {
                "type": "password",  # permet de cacher le mdp
                "name": "mot_de_passe",
                "message": "Choisissez un mot de passe: ",
            },
            {
                "type": "password",
                "name": "confirmation_mot_de_passe",
                "message": "Confirmez votre mot de passe",
            },
            {
                "type": "input",
                "name": "email",
                "message": "Entrez votre email"
            }
        ]

    def message_info(self):
        print("Bonjour,choisissez votre pseudo et votre mot de passe s'il vous plait")

    def make_choice(self):
        reponse = prompt(self.__questions)

        if reponse["mot_de_passe"] != reponse["confirmation_mot_de_passe"]:
            print("Les mots de passe ne correspondent pas. Veuillez réessayer.")
            return self  # ramène au mot de passe

        pseudo = reponse["pseudo"]
        mot_de_passe = reponse["mot_de_passe"]

        compte = utilisateur_service()

        try:
            result = compte.creer_utilisateur(pseudo, mot_de_passe)
            if result == 0:
                print("Compte créé avec succès ! ")
            elif result == 1:
                print("Mauvaise création")
            else:
                print("Compte déjà existant")

        except Exception as e:
            print(f"Erreur lors de la création du compte : {e}")
            return self

        from view.LogView import LogView

        return LogView()


class MailValidator(Validator):
    """la classe MailValidator verifie si la chaine de caractères
    que l'on entre correspond au format de l'email"""

    def validate(self, document) -> None:
        ok = regex.match(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", document.text)
        if not ok:
            raise ValidationError(
                message="Please enter a valid mail", cursor_position=len(document.text)
            )
