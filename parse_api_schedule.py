import requests
from pprint import pprint

# postgres imports
import os
from urllib import parse
import psycopg2


""" create tables in the PostgreSQL database"""
commands = (
    """
    CREATE TABLE SCHEDULE (
        GAME_ID int(10) NOT NULL DEFAULT '0' PRIMARY KEY,
        HOME_TEAM int(2) NOT NULL,
        AWAY_TEAM int(2) NOT NULL,
        LOCATION VARCHAR(255)
    )
    """,
    """ CREATE TABLE parts (
            part_id SERIAL PRIMARY KEY,
            part_name VARCHAR(255) NOT NULL
            )
    """,
    """
    CREATE TABLE part_drawings (
            part_id INTEGER PRIMARY KEY,
            file_extension VARCHAR(5) NOT NULL,
            drawing_data BYTEA NOT NULL,
            FOREIGN KEY (part_id)
            REFERENCES parts (part_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE vendor_parts (
            vendor_id INTEGER NOT NULL,
            part_id INTEGER NOT NULL,
            PRIMARY KEY (vendor_id , part_id),
            FOREIGN KEY (vendor_id)
                REFERENCES vendors (vendor_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (part_id)
                REFERENCES parts (part_id)
                ON UPDATE CASCADE ON DELETE CASCADE
    )
    """)

# set up postgres connection
parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()
# create table one by one
for command in commands:
    cur.execute(command)

# close communication with the PostgreSQL database server
cur.close()
# commit the changes
conn.commit()

url = 'https://statsapi.web.nhl.com/api/v1/schedule'

# get text and json
r = requests.get(url)
text = r.text
json = r.json()

pprint(json)

for games_date in json['dates']:

	# get current date
	date = games_date['date']
	print('date=' + date)

	for game in games_date['games']:

		# check if game is regular season
		if game['gameType'] is 'R':

			# game id
			game_id = game['gamePk']
			print(game_id)

			# dates
			season = game['season']
			date = game['gameDate']

			# teams
			home_id = game['teams']['home']['team']['id']
			home_name = game['teams']['home']['team']['name']
			away_id = game['teams']['away']['team']['id']
			away_name = game['teams']['away']['team']['name']
			print(away_name + ' (' + str(away_id) + ') @ ' + home_name + ' (' + str(home_id) + ')')




