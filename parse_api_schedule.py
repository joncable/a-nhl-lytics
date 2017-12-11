import requests
from pprint import pprint

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




