import logging
import dotenv

from utils.log_init import initialiser_logs

from view.accueil.accueil_vue import AccueilVue


if __name__ == "__main__":
    # On charge les variables d'environnement
    dotenv.load_dotenv(override=True)
    # Configuration du logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Créer une instance de ResetDatabase et créer les tables
    reset_db = ResetDatabase()
    reset_db.lancer()


    initialiser_logs("Application")


    vue_courante = AccueilVue("Bienvenue dans")
    nb_erreurs = 0


    while vue_courante:
        """
        if nb_erreurs > 100:
            print("Le programme recense trop d'erreurs et va s'arrêter")
            break
        """
        # Affichage du menu
        vue_courante.afficher()
        vue_courante.message_info()
        # Affichage des choix possibles
        vue_courante = vue_courante.choisir_menu()
        """
        except Exception as e:
            logging.info(e)
            nb_erreurs += 1
            vue_courante = AccueilVue("Une erreur est survenue, retour au menu principal")
        """
    # Lorsque l on quitte l application
    print("----------------------------------")
    print("Au revoir")

    logging.info("Fin de l'application")
