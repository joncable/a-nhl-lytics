import requests
from pprint import pprint

# postgres imports
import os
from urllib import parse
import psycopg2


""" create tables in the PostgreSQL database"""
commands = (
    """
    CREATE TABLE IF NOT EXISTS SCHEDULE (
        GAME_ID int NOT NULL DEFAULT '0' PRIMARY KEY,
        SEASON int NOT NULL,
        HOME_TEAM int NOT NULL,
        AWAY_TEAM int NOT NULL,
        VENUE VARCHAR(255),
        DATE date DEFAULT NULL,
        TIME VARCHAR(255) DEFAULT NULL,
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS TEAMS (
        TEAM_ID int PRIMARY KEY,
        TEAM_NAME VARCHAR(255) NOT NULL
    )
    """
)

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

url = 'https://statsapi.web.nhl.com/api/v1/schedule'

# get text and json
r = requests.get(url)
text = r.text
json = r.json()

pprint(json)

sql = """INSERT INTO schedule(game_id, home_id, away_id)
         VALUES(%s, %s, %s);"""

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
			time = game['gameDate']

			# teams
			home_id = game['teams']['home']['team']['id']
			home_name = game['teams']['home']['team']['name']
			away_id = game['teams']['away']['team']['id']
			away_name = game['teams']['away']['team']['name']
			print(away_name + ' (' + str(away_id) + ') @ ' + home_name + ' (' + str(home_id) + ')')

			# location
			venue = game['venue']['name']

			# execute the INSERT statement
			cur.execute(sql, (game_id, season, home_id, away_id, venue, date, time))

# close communication with the PostgreSQL database server
cur.close()
# commit the changes
conn.commit()
