import pandas as pd

SQL_QUERY_CHECK_USER_ALL_GAME_DETAILS = r"""
	SELECT * FROM {user_game_details_table}
	WHERE username = '{username}' 
"""

SQL_QUERY_CHECK_USER_IN_GAME_DETAILS = r"""
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

class Gameresult:
	
	def __init__(self):
		pass

	def update_results(self, username, game, difficulty, result):
		exists = self.check_user_game_details(username, game)
		if not exists:
			self.create_user_game_details(username, game)
		self.update_user_game_details(username, game, difficulty, result)

	def check_user_game_details(self,username, game):
		sql_query = SQL_QUERY_CHECK_USER_IN_GAME_DETAILS.format(
							user_game_details_table='user_game_details',
							username=username,
							game=game)
		df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
		if df.empty:
			return False
		else:
			return True

	def create_user_game_details(self, username, game):
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
		sql_query = SQL_QUERY_CHECK_USER_IN_GAME_DETAILS.format(
							user_game_details_table='user_game_details',
							username=username,
							game=game)
		df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
		print("\nYour scores for the game {} up till now are: \n".format(game))
		for i in range(len(df)):
			print('{} -  Games Won: {}, Games Lost: {}'.format(df.iloc[i]['difficulty'], df.iloc[i]['games_won'], df.iloc[i]['games_lost']))

	def display_game_results_options(self, games, username):
		while True:
			games_dict = {str(i+1): games[i] for i in range(0, len(games))}

			entered = False
			while not entered:
				print("Choose game you want to see scores of:")
				
				for idx, game in games_dict.items():
					print(idx, game.capitalize())
				
				print(int(idx)+1, 'All')
				print(int(idx)+2, 'Back')

				option = input()
				print(option)
				if option in games_dict:
					sql_query = SQL_QUERY_CHECK_USER_IN_GAME_DETAILS.format(
								user_game_details_table='user_game_details',
								username=username,
								game=games_dict[option])
					entered = True

				elif option == str(int(idx)+1):
					sql_query = SQL_QUERY_CHECK_USER_ALL_GAME_DETAILS.format(
								user_game_details_table='user_game_details',
								username=username)
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
					print("{}-".format(game.capitalize()))
					games.append(game)
				print('{} -  Games Won: {}, Games Lost: {}'.format(df.iloc[i]['difficulty'].capitalize(), df.iloc[i]['games_won'], df.iloc[i]['games_lost']))
			print("\n")
	def __str__(self):
		print("Game Results!")