import pandas as pd
from datetime import datetime
import uuid
from db_engines import DBEngines
from settings import DATABASES
import time
import stdiomask
import re
import random
import smtplib, ssl

from hangman.hangman import Hangman
from rockpaperscissor import Rockpaperscissor
from game_results import GameResults
from multiplayer import MultiPlayer

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login("akshattesting123@gmail.com", "testing@123")


SQL_QUERY_CHECK_USER_EXISTS = r"""
	SELECT * FROM {user_details_table}
	WHERE username = '{username}' 
	AND password = '{password}'
"""

SQL_QUERY_CHECK_USERNAME_EXISTS = r"""
	SELECT * FROM {user_details_table}
	WHERE username = '{username}'
"""

SQL_QUERY_UPDATE_USER_PASSWORD = r"""
	UPDATE {user_details_table}
	SET password = '{password}', modified_on = '{now}'
	WHERE username = '{username}'
"""

SQL_QUERY_ADD_USER = r"""
	INSERT INTO {user_details_table}
	VALUES ('{id_val}', '{username}', '{password}', '{emailid}');
"""


class GamesScoresOptions(GameResults):
	multiplayer_options  = {"1":"Hangman", "2":"Rock, Paper, Scissors", "3":"TicTacToe", "4":"Back"}
	singleplayer_options = {"1":"Hangman", "2":"Rock, Paper, Scissors", "3":"Back"}
	available_games = ["Hangman", "Rock, Paper, Scissors", "TicTacToe"]

	def __init__(self, usertype, username, gametype=''):
		self.gametype = gametype
		self.usertype = usertype
		self.username = username
		self.game = ''

	def score_options(self):
		if self.usertype != 'guest':
			super().display_game_results_options(self.available_games, self.username)
		else:
			print("You are not a user, please select again or signup to keep a track of your records!\n")
	
	def game_options(self):
		while True:
			if self.gametype == 'multi':
				print("Please choose the game you want to play from below:")
				while True:
					for key, value in self.multiplayer_options.items():
						print("{}. {}".format(key, value))

					option = input("Please enter your choice: ")
					if option in self.multiplayer_options:
						break
					else:
						print("Invalid option! Choose again.\n")
			
				self.game = self.multiplayer_options[option]
				if self.game != 'Back':
					self.play_option()
				else:
					return

			elif self.gametype == 'single':
				print("Please choose the game you want to play or if you want to see your scores:")
				while True:
					for key, value in self.singleplayer_options.items():
						print("{}. {}".format(key, value))

					option = input("Please enter your choice: ")
					if option in self.singleplayer_options:
						break
					else:
						print("Invalid option! Choose again.\n")

				self.game = self.singleplayer_options[option]
				if self.game != 'Back':
					self.play_option()
				elif self.game == 'Back':
					return

	def play_option(self):
		play_again = True
		while play_again:
			if self.gametype == "multi":
				play = Hangman(self.usertype, self.gametype)
				multi_instance = MultiPlayer()
				while True:
					players = ['player1', 'player2']
					for player in players:
						if player == "player1":
							name = multi_instance.player1_name()
							print("{} playing first.".format(name))
							if self.game == "Hangman":
								play.word_and_hint(name)
								result, difficulty_level = play.user_game()
						else:
							name = multi_instance.player2_name()
							print("{} playing now.".format(name))							
							if self.game == "Hangman":
								play.word_and_hint(name, difficulty_level)
								result, difficulty_level = play.user_game() # since we want player2 to have the same difficulty as player1

						# elif self.game == "Rock, Paper, Scissors":
						# 	play = Rockpaperscissor(self.usertype, self.gametype, name)
						# elif self.game == "TicTacToe":
						# 	play = Hangman(self.usertype, self.gametype, name)

						multi_instance.updatescores(player, result)

					multi_instance.displayscores()
					if ((input("\nDo you want to play again? (Press y for yes), else enter any key... ")).lower()) != 'y':
						return

			elif self.gametype == "single":
				if self.game == "Hangman":
					play = Hangman(self.usertype, self.gametype)
					play.word_and_hint()
				# elif self.game == "Rock, Paper, Scissors":
				# 	play = Rockpaperscissor(self.usertype, self.gametype, name)
				# elif self.game == "TicTacToe":
				# 	play = Hangman(self.usertype, self.gametype, name)

				result, difficulty_level = play.user_game()

				if self.usertype != 'guest':
					super().base_results(self.username, self.game, difficulty_level, result)
					super().display_user_game_details(self.username, self.game)

				if ((input("\nDo you want to play again? (Press y for yes), else enter any key... ")).lower()) != 'y':
					return

		return

class PlayerStart(MultiPlayer):
				
	def __init__(self):
		self.db_engines = DBEngines.get_instance()
		self.games_db_engine = self.db_engines.get_engine(DATABASES['default'])

	def get_sql_add_user(self, username, emailid, password,id_val):
		sql = SQL_QUERY_ADD_USER.format(
			user_details_table='user_details',
			username=username,
			password=password,
			emailid=emailid,
			id_val=id_val)
		return sql


	def get_sql_username_check(self, username):
		sql = SQL_QUERY_CHECK_USERNAME_EXISTS.format(
						user_details_table='user_details',
						username=username)
		return sql

	def get_sql_user_check(self, username, password):
		sql = SQL_QUERY_CHECK_USER_EXISTS.format(
						user_details_table='user_details',
						username=username,
						password=password)
		return sql

	def get_sql_password_change(self, username, password):
		now = datetime.now()
		sql = SQL_QUERY_UPDATE_USER_PASSWORD.format(
						user_details_table='user_details',
						username=username,
						password=password,
						now=now)
		return sql

	def signup(self):
		username_accepted = False
		while not username_accepted:
			username = input("Please enter username(greater than 5 characters): ")
			if len(username) < 5:
				print("Username less than 5 characters, please choose some other username!\n")
				continue

			sql_query = self.get_sql_username_check(username)  # could have used try except since username is anyway unique in db so would give error
			df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
			
			if df.empty and len(username) >= 5:
				username_accepted = True
			else:
				print("Username already exists, please choose some other username!\n")
				
		regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
		pass_accepted = False
		while not pass_accepted:
			print("Please enter password(should be greater than 5 characters and should contain atleast one special character, one letter and one digit)")
			password = stdiomask.getpass()
			if len(password) > 5 and regex.search(password) != None and bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', password)) == True:
				print("Please enter password again to confirm")
				password2 = stdiomask.getpass()
				if password == password2:
					pass_accepted = True
				else:
					print("Password mismatch!")
			else:
				print("Password is weak, enter again!\n")

		regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
		email_accepted = False
		while not email_accepted:
			emailid = input("Please enter Email id: ")
			if(re.fullmatch(regex, emailid)):
				email_accepted = True
			else:
				print("Invalid email, enter again!\n")

		id_val = uuid.uuid1()
		sql_query = self.get_sql_add_user(username, emailid, password, id_val)

		try:
			with self.games_db_engine.connect() as con:
				con.execution_options(autocommit=True).execute(sql_query)
			print("User creation successful!")
			return username
		except:
			raise Exception("User creation not successful! :(")

	def login(self):
		user_accepted = False
		while not user_accepted:
			username = input("Please enter username: ")
			password = stdiomask.getpass()

			sql_query = self.get_sql_user_check(username, password)
			df = pd.read_sql(sql=sql_query, con=self.games_db_engine)

			if not df.empty:
				user_accepted = True
			else:
				print("Username and/or Password you provided is/are incorrect, please enter again!\n")

		print("Logging in as {}...".format(username))
		time.sleep(1)
		return username

	def forgotpassword(self):
		user_accepted = False
		while not user_accepted:
			username = input("Please enter username: ")
			sql_query = self.get_sql_username_check(username)
			df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
			if not df.empty:
				user_accepted = True
			else:
				print("Username and password you provided are incorrect, please enter again!\n")
		
		emailid = df.iloc[0]['emailid']
		number = random.randint(1111,9999)

		msg = "Subject: OTP for password change.\n\nThe OTP for changing you password is: {}. Please take care of your privacy and never hare such mails or messages with anyone".format(str(number))
		s.sendmail('akshattesting123@gmail.com', emailid, msg)

		otp = input("An OTP has been sent to your email id -  {}, please enter here to reset your password: ".format('*'*(len(emailid)-7)+emailid[-13:]))
		if int(otp) == number:
			regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
			pass_accepted = False
			while not pass_accepted:
				# password = input("Please enter password(greater than 5 characters): ")			
				print("Please enter password(should be greater than 5 characters and should contain atleast one special character, one letter and one digit)")
				password = stdiomask.getpass()
				if len(password) > 5 and regex.search(password) != None and bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', password)) == True:
					print("Please enter password again to confirm")
					password2 = stdiomask.getpass()
					if password == password2:
						pass_accepted = True
					else:
						print("Password mismatch!")
				else:
					print("Password is weak, enter again!\n")

			sql_query = self.get_sql_password_change(username, password)
			with self.games_db_engine.connect() as con:
				con.execution_options(autocommit=True).execute(sql_query)
			print("Password change successful!")

	def startpage(self):
		while True:  # because we need to show the user login page again and again until user exits using option number 4
			entered = False
			username = ''
			while not entered:
				option = input("Please choose an option:\n1. Login (If existing user)\n2. Signup\n3. Play as a guest\n4. Forgot password\n5. Exit\n")
				options = {"1":"login", "2":"signup","3":"guest","4":"forgot password","5":"exit"}
				if option in options:
					if option == '1':
						entered = True
						usertype = 'user'
						username = self.login()
					elif option == '2':
						entered = True
						usertype = 'user'
						username = self.signup()
					elif option == '3':
						entered = True
						usertype = 'guest'
						print("Logging in as a guest...")
						time.sleep(1)
					elif option == '4':
						self.forgotpassword()
					else:
						return
				else:
					print("Invalid option! Choose again.\n")


			while True:
				choice = input("Please choose from below:\n1. Play a game\n2. Check Scores (Only if you are a user)\n3. Back\n")
				if choice == "1":
					gametype = super().checkgametype()  # can be single, multi, or back option
					if gametype == None:  # no response means back option seelcted
						continue
					game = GamesScoresOptions(usertype, username, gametype)
					game.game_options()

				elif choice == "2":
					scores = GamesScoresOptions(usertype, username)
					scores.score_options()

				elif choice == "3":
					break

				else:
					print("Wrong option, please choose again!")

	def __str__(self):
		print("Start Page!")


if __name__ == '__main__':
	user = PlayerStart()
	user.startpage()
