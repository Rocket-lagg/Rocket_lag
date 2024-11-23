
 _______                       __                   __            __
|       \                     |  \                 |  \          |  \
| $$$$$$$\  ______    _______ | $$   __   ______  _| $$_         | $$       ______    ______
| $$__| $$ /      \  /       \| $$  /  \ /      \|   $$ \        | $$      |      \  /      \
| $$    $$|  $$$$$$\|  $$$$$$$| $$_/  $$|  $$$$$$\\$$$$$$        | $$       \$$$$$$\|  $$$$$$\
| $$$$$$$\| $$  | $$| $$      | $$   $$ | $$    $$ | $$ __       | $$      /      $$| $$  | $$
| $$  | $$| $$__/ $$| $$_____ | $$$$$$\ | $$$$$$$$ | $$|  \      | $$_____|  $$$$$$$| $$__| $$
| $$  | $$ \$$    $$ \$$     \| $$  \$$\ \$$     \  \$$  $$      | $$     \\$$    $$ \$$    $$
 \$$   \$$  \$$$$$$   \$$$$$$$ \$$   \$$  \$$$$$$$   \$$$$        \$$$$$$$$ \$$$$$$$ _\$$$$$$$
                                                                                    |  \__| $$
                                                                                     \$$    $$
                                                                                      \$$$$$$



This project is a console-based application that allows users to looks statistics for Rocket League matchs. Data is sourced via web scraping from Ballchasing and Liquipedia and stored in a PostgreSQL database.
Users can navigate through the application to perform searches by team or player, find statistics on team or player, add or suppress matchs and with an account, bet on matchs and create tournament

## Fonctionalities

First you can:
    -Create an account with your pseudo, password and email
    -See the statistics of a team or player on a specific match
    -See the global statistics of a team or a player
    -See the calendar of the futur match and search a match by date
    -See your logging ifo

But once your connected you can also:
    -Create your own tournament, you can choose the number of matchs and the
    type of match. Then you can invite other user with a code or add team yourself.
    You can complete the result of the match at anytime after.
    -Bet on matchs and see your previous matchs


### Requirements

Install the require library with:

pip install -r requirements.txt

Créer un .env avec :
POSTGRES_HOST=sgbd-eleves.domensai.ecole
POSTGRES_PORT=5432
POSTGRES_DATABASE=idXXXX
POSTGRES_USER=idXXXX
POSTGRES_PASSWORD=idXXXX
POSTGRES_SCHEMA=RocketLag
LIST_ADMIN=[]

## Launching

launch src.__main__.py
