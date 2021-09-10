import pandas as pd
from db_engines import DBEngines
from settings import DATABASES

SQL_QUERY_USER_ALL_GAME_DETAILS = r"""
	SELECT * FROM {user_game_details_table}
	WHERE username = '{username}' 
"""

SQL_QUERY_USER_SPECIFIC_GAME_DETAILS = r"""
	SELECT * FROM {user_game_details_table}
	WHERE username = '{username}' 
	AND game = '{game}'
"""

SQL_QUERY_APPEND_USER_GAME_DETAILS = r"""
	INSERT INTO {user_game_details_table} (username, game, difficulty)
	VALUES ('{username}', '{game}', 'easy'), 
	('{username}', '{game}', 'medium'), 
	('{username}', '{game}', 'hard')
"""

SQL_QUERY_UPDATE_USER_GAME_DETAILS = r"""
	UPDATE {user_game_details_table} SET games_{result} = games_{result} + 1
	WHERE username = '{username}'
	AND game = '{game}'
	AND difficulty = '{difficulty}'
"""

class GameResults:
	
	db_engines = DBEngines.get_instance()
	games_db_engine = db_engines.get_engine(DATABASES['default'])
	
	def __init__(self):
		pass

	def base_results(self, username, game, difficulty, result, create_with_difficulties=True):
		sql_query = self.get_sql_user_specific_game_details(username, game)
		df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
		if df.empty:
			self.create_user_game_details(username, game)
		self.update_user_game_details(username, game, difficulty, result)

	def get_sql_user_specific_game_details(self, username, game):
		sql_query = SQL_QUERY_USER_SPECIFIC_GAME_DETAILS.format(
							user_game_details_table='user_game_details',
							username=username,
							game=game)
		return sql_query

	def get_sql_user_all_game_details(self, username):
		sql_query = SQL_QUERY_USER_ALL_GAME_DETAILS.format(
								user_game_details_table='user_game_details',
								username=username)
		return sql_query

	def create_user_game_details(self, username, game, create_with_difficulties=True): #TODO: for rock paper scissors it will be false and use different sql query
		sql_query = SQL_QUERY_APPEND_USER_GAME_DETAILS.format(
							user_game_details_table='user_game_details',
							username=username,
							game=game)
		with self.games_db_engine.connect() as con:
			con.execution_options(autocommit=True).execute(sql_query)

	def update_user_game_details(self, username, game, difficulty, result):
		sql_query = SQL_QUERY_UPDATE_USER_GAME_DETAILS.format(
							user_game_details_table='user_game_details',
							username=username,
							game=game,
							difficulty=difficulty,
							result=result)
		with self.games_db_engine.connect() as con:
			con.execution_options(autocommit=True).execute(sql_query)

	def display_user_game_details(self, username, game):
		sql_query = self.get_sql_user_specific_game_details(username, game)
		df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
		print("\nYour scores for the game {} up till now are: \n".format(game))
		for i in range(len(df)):
			print('{} -  Games Won: {}, Games Lost: {}'.format(df.iloc[i]['difficulty'], df.iloc[i]['games_won'], df.iloc[i]['games_lost']))

	def display_game_results_options(self, avail_games, username):
		while True:
			games_dict = {str(i+1): avail_games[i] for i in range(0, len(avail_games))}

			entered = False
			while not entered:
				print("Choose game you want to see scores of:")
				for idx, game in games_dict.items():
					print(idx, game.capitalize())
				
				print(int(idx)+1, 'All')
				print(int(idx)+2, 'Back')

				option = input()
				if option in games_dict:
					sql_query = self.get_sql_user_specific_game_details(username, games_dict[option])
					entered = True

				elif option == str(int(idx)+1):
					sql_query = self.get_sql_user_all_game_details(username)
					entered = True

				elif option == str(int(idx)+2):
					return

				else:
					print("Incorrect option entered, please choose again!\n")
					continue

			df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
			print("\nYour scores are:")
			games = []
			for i in range(len(df)):
				game = df['game'][0]
				if game not in games:
					print("{}-".format(game))
					games.append(game)
				print('{} -  Games Won: {}, Games Lost: {}'.format(df.iloc[i]['difficulty'].capitalize(), df.iloc[i]['games_won'], df.iloc[i]['games_lost']))
			if df.empty:
				print("Please play a game to have scores!\n")

	def __str__(self):
		print("Game Results!")