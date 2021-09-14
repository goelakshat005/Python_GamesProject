import pandas as pd
from db_engines import DBEngines
from settings import DATABASES

SQL_QUERY_USER_SPECIFIC_GAME_DETAILS = r"""
	SELECT * FROM {user_game_details_table}
	WHERE username = '{username}' 
	AND game = '{game}'
"""

SQL_QUERY_APPEND_USER_GAME_DETAILS_WITHDIFFICULTY = r"""
	INSERT INTO {user_game_details_table} (username, game, difficulty)
	VALUES ('{username}', '{game}', 'easy'), 
	('{username}', '{game}', 'medium'), 
	('{username}', '{game}', 'hard')
"""

SQL_QUERY_APPEND_USER_GAME_DETAILS_WITHOUTDIFFICULTY = r"""
	INSERT INTO {user_game_details_table} (username, game, difficulty)
	VALUES ('{username}', '{game}', '')
"""

SQL_QUERY_UPDATE_USER_GAME_DETAILS = r"""
	UPDATE {user_game_details_table} SET games_{result} = games_{result} + 1
	WHERE username = '{username}'
	AND game = '{game}'
	AND difficulty = '{difficulty}'
"""

SQL_QUERY_UPDATE_USER_GAME_SCORE = r"""
	UPDATE {user_game_details_table} SET score = {score}
	WHERE username = '{username}'
	AND game = '{game}'
	AND difficulty = '{difficulty}'
"""

class GameResults:
	
	db_engines = DBEngines.get_instance()
	games_db_engine = db_engines.get_engine(DATABASES['default'])

	def __init__(self):
		pass

	def base_results(self, username, game, difficulty, result, with_difficulties, only_scores=False):
		sql_query = self.get_sql_user_specific_game_details(username, game)
		df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
		if df.empty:
			self.create_user_game_details(username, game, with_difficulties)

		if only_scores == False:
			self.update_user_game_details(username, game, difficulty, result, with_difficulties)
		elif only_scores == True:
			self.update_user_game_details_only_score(username, game, difficulty, result, with_difficulties)
	
	def get_sql_user_specific_game_details(self, username, game):
		sql_query = SQL_QUERY_USER_SPECIFIC_GAME_DETAILS.format(
							user_game_details_table='user_game_details',
							username=username,
							game=game)
		return sql_query

	def create_user_game_details(self, username, game, with_difficulties):
		if with_difficulties == True:
			sql_query = SQL_QUERY_APPEND_USER_GAME_DETAILS_WITHDIFFICULTY.format(
							user_game_details_table='user_game_details',
							username=username,
							game=game)
		else:
			sql_query = SQL_QUERY_APPEND_USER_GAME_DETAILS_WITHOUTDIFFICULTY.format(
							user_game_details_table='user_game_details',
							username=username,
							game=game)

		with self.games_db_engine.connect() as con:
			con.execution_options(autocommit=True).execute(sql_query)

	def update_user_game_details(self, username, game, difficulty, result, with_difficulties):
		sql_query = SQL_QUERY_UPDATE_USER_GAME_DETAILS.format(
							user_game_details_table='user_game_details',
							username=username,
							game=game,
							difficulty=difficulty,
							result=result)
		with self.games_db_engine.connect() as con:
			con.execution_options(autocommit=True).execute(sql_query)

	def update_user_game_details_only_score(self, username, game, difficulty, result, with_difficulties):
		sql_query = SQL_QUERY_USER_SPECIFIC_GAME_DETAILS.format(
							user_game_details_table='user_game_details',
							username=username,
							game=game)
		df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
		if df.iloc[0]['score'] < result:
			sql_query = SQL_QUERY_UPDATE_USER_GAME_SCORE.format(
							user_game_details_table='user_game_details',
							username=username,
							game=game,
							difficulty=difficulty,
							score=result)

			with self.games_db_engine.connect() as con:
				con.execution_options(autocommit=True).execute(sql_query)
			if df.iloc[0]['score'] != 0:
				print("Congratulations you broke your old record!".format(df.iloc[0]['score']))
		else:
			print("Sorry, you couldn't break your old record!")


	def display_game_results_options(self, avail_games, singleplayer_games_with_only_scores, username):
		games_dict = {str(i+1): avail_games[i] for i in range(0, len(avail_games))}
		while True:
			print("\nChoose game you want to see scores of:")
			for idx, game in games_dict.items():
				print(idx, game.capitalize())
			
			print(int(idx)+1, 'Back')

			option = input()

			if option in games_dict:
				if games_dict[option] not in singleplayer_games_with_only_scores:
					self.display_games_scores_with_win_lose(username, games_dict[option])
				else:
					self.display_games_with_only_scores(username, games_dict[option])

			elif option == str(int(idx)+1):
				return

			else:
				print("Incorrect option entered, please choose again!\n")
				continue

	def display_games_scores_with_win_lose(self, username, game):
		sql_query = self.get_sql_user_specific_game_details(username, game)
		df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
		
		if df.empty:
			print("Please play a game to have it's scores!")
			return

		print("\nYour scores for the game {} up till now are: \n".format(game))
		games = []
		for i in range(len(df)):
			if df['difficulty'][i] == '':
				print('Games Won: {}, Games Lost: {}'.format(df.iloc[i]['games_won'], df.iloc[i]['games_lost']))
			else:
				print('{} -  Games Won: {}, Games Lost: {}'.format(df.iloc[i]['difficulty'].capitalize(), df.iloc[i]['games_won'], df.iloc[i]['games_lost']))
		

	def display_games_with_only_scores(self, username, game):
		sql_query = self.get_sql_user_specific_game_details(username, game)
		df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
		
		if df.empty:
			print("Please play a game to have it's scores!")	
			return

		print("Your highest score in {} is: {}".format(df.iloc[0]['game'], df.iloc[0]['score']))

	def __str__(self):
		print("Game Results!")