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

from hangman.hangman import BaseHangman
from rockpaperscissor import BaseRockPaperScissor
from tictactoe import BaseTicTacToe
from flames import BaseFlames
from jumbledwords import BaseJumbledWords 

from gameresults import GameResults
from multiplayer import MultiPlayer
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login("akshattesting123@gmail.com", "testing@123")

# although usertype is passed on to all the classes of games, we don't actually require it

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
	game_objects = {
		"Hangman": BaseHangman,
		"RockPaperScissor": BaseRockPaperScissor,
		"TicTacToe": BaseTicTacToe,
		"Flames": BaseFlames,
		"JumbledWords": BaseJumbledWords
	}

	singleplayer_options = {"1":"Hangman", "2":"RockPaperScissor", "3":"Back"}   # for showing to user
	multiplayer_options  = {"1":"Hangman", "2":"RockPaperScissor", "3":"TicTacToe", "4":"Flames", "5":"Back"}  # for showing to user

	def __init__(self, usertype, username, gametype=''):
		self.gametype = gametype
		self.usertype = usertype
		self.username = username
		self.game = ''


	def score_options(self):
		if self.usertype != 'guest':
			single_players_games_list = list(self.singleplayer_options.values())
			single_players_games_list.pop()
			super().display_game_results_options(single_players_games_list, self.username)
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
					play = self.game_objects[self.game](self.usertype, self.gametype)
					play.handle()
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
					play = self.game_objects[self.game](self.usertype, self.gametype, self.username)
					play.handle()
				elif self.game == 'Back':
					return

	# def multiplayer_type4_play(self):
	# 	print("Which type of game do you wanna play?")
	# 	print("1. Do you want both the players to guess the same word?\n2. Do you want both the players to guess different word given by the other player?")
	# 	while True:
	# 		option = input("Please choose an option: ")
	# 		if option == "1":
	# 			self.multiplayer_type2_play()
	# 			return
	# 		elif option == "2":
	# 			self.multiplayer_type1_play()
	# 			return
	# 		else:
	# 			print("You have not chosen from available options, choose again!")

class PlayerStart(MultiPlayer):
				
	def __init__(self):
		self.db_engines = DBEngines.get_instance()
		self.games_db_engine = self.db_engines.get_engine(DATABASES['default'])

	def apostrophe_balancing(self, word):
		if '\'' in word:
			lis_word = list(word)
			apostrophe_idx = []
			for idx, let in enumerate(lis_word):
				if let == '\'':
					apostrophe_idx.append(idx)
			count = 0
			for idx in apostrophe_idx:
				lis_word.insert(idx+count,"'")
				count += 1
			word = ''.join(lis_word)
		return word

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

			username = self.apostrophe_balancing(username)

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

		password = self.apostrophe_balancing(password)

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
			
			username = self.apostrophe_balancing(username)
			password = self.apostrophe_balancing(password)

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
			username = self.apostrophe_balancing(username)
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

			password = self.apostrophe_balancing(password)
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
