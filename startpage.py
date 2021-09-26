import pandas as pd
from datetime import datetime
import uuid
import time
import stdiomask
import re
import random
import smtplib, ssl

from common.db_engines import DBEngines
from common.settings import DATABASES
from common.gameresults import GameResults

from hangman.hangman import BaseHangman
from rockpaperscissor import BaseRockPaperScissor
from tictactoe import BaseTicTacToe
from flames import BaseFlames
from jumbledwords import BaseJumbledWords 
from memorytest import BaseMemoryTest
from moneygamespackage.moneygames import BaseMoneyGames
from cowsandbulls import BaseCowsAndBulls

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login("akshattesting123@gmail.com", "testing@123")

# although usertype is passed on to all the classes of games, we don't actually require it

SQL_QUERY_TO_CHECK_IF_USER_EXISTS = r"""
	SELECT * FROM {user_details_table}
	WHERE username = '{username}' 
	AND password = '{password}'
"""

SQL_QUERY_TO_CHECK_IF_USERNAME_EXISTS = r"""
	SELECT * FROM {user_details_table}
	WHERE username = '{username}'
"""

SQL_QUERY_TO_CHECK_IF_EMAILID_EXISTS = r"""
	SELECT * FROM {user_details_table}
	WHERE emailid = '{emailid}'
"""

SQL_QUERY_TO_UPDATE_PASSWORD = r"""
	UPDATE {user_details_table}
	SET password = '{password}', modified_on = '{now}'
	WHERE username = '{username}'
"""

SQL_QUERY_TO_ADD_NEW_USER = r"""
	INSERT INTO {user_details_table}
	VALUES ('{id_val}', '{username}', '{password}', '{emailid}');
"""


class GamesScoresOptions(GameResults):
	game_objects = {
		"Hangman": BaseHangman,
		"RockPaperScissor": BaseRockPaperScissor,
		"TicTacToe": BaseTicTacToe,
		"Flames": BaseFlames,
		"JumbledWords": BaseJumbledWords,
		"MemoryTest": BaseMemoryTest,
		"MoneyGames": BaseMoneyGames,
		"CowsAndBulls": BaseCowsAndBulls
	}

	singleplayer_options = {"1":"Hangman", "2":"RockPaperScissor", "3":"JumbledWords", "4":"MemoryTest", "5":"CowsAndBulls", "6":"Back"}   # for showing to user
	multiplayer_options  = {"1":"Hangman", "2":"RockPaperScissor", "3":"TicTacToe", "4":"Flames", "5":"JumbledWords", "6":"MemoryTest", "7":"CowsAndBulls", "8":"MoneyGames", "9":"Back"}  # for showing to user

	singleplayer_games_with_only_scores = ["MemoryTest", "CowsAndBulls"]

	def __init__(self, usertype, username, gametype=''):
		self.gametype = gametype
		self.usertype = usertype
		self.username = username
		self.game = ''

	def score_options(self):
		if self.usertype != 'guest':
			single_players_games_list = list(self.singleplayer_options.values())
			single_players_games_list.pop()    # to remove back option from it
			super().display_game_results_options(single_players_games_list, self.singleplayer_games_with_only_scores, self.username)
		else:
			print("You are not a user, please select again or signup to keep a track of your records!")
			
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
					play = self.game_objects[self.game](self.usertype, self.gametype)       # a new object is created everytime
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

	def __str__(self):
		print("Second page, after user successfully logins!")

class Start():
				
	gametypes = {"1": "single", "2": "multi"}
	
	def __init__(self):
		self.db_engines = DBEngines.get_instance()
		self.games_db_engine = self.db_engines.get_engine(DATABASES['default'])

		self.username = ''
		self.usertype = ''

	def get_sql_query_to_add_new_user(self, emailid, password,id_val):
		sql = SQL_QUERY_TO_ADD_NEW_USER.format(
						user_details_table='user_details',
						username=self.username,
						password=password,
						emailid=emailid,
						id_val=id_val)
		return sql


	def get_sql_query_check_username_exists(self):
		sql = SQL_QUERY_TO_CHECK_IF_USERNAME_EXISTS.format(
						user_details_table='user_details',
						username=self.username)
		return sql

	def get_sql_query_to_check_user_exists(self, password):
		sql = SQL_QUERY_TO_CHECK_IF_USER_EXISTS.format(
						user_details_table='user_details',
						username=self.username,
						password=password)
		return sql

	def get_sql_query_check_emailid_exists(self, emailid):
		sql = SQL_QUERY_TO_CHECK_IF_EMAILID_EXISTS.format(
						user_details_table='user_details',
						emailid=emailid)
		return sql


	def get_sql_query_to_change_password(self, password):
		now = datetime.now()
		sql = SQL_QUERY_TO_UPDATE_PASSWORD.format(
						user_details_table='user_details',
						username=self.username,
						password=password,
						now=now)
		return sql

	# apostrophe_balancing function because when we write sql queries when user has written apostrophes(') either one or multiple in username/password creates issues 
	# when executing those sql queries so we need to balance/correct those apostrophies
	def apostrophe_balancing(self, word):
		if '\'' in word:
			lis_word = list(word)
			apostrophe_idx = []
			for idx, char in enumerate(lis_word):
				if char == '\'':
					apostrophe_idx.append(idx)
			count = 0
			for idx in apostrophe_idx:
				lis_word.insert(idx+count,"'")
				count += 1
			word = ''.join(lis_word)
		return word

	def signup(self):
		username_accepted = False
		while not username_accepted:
			self.username = input("Please enter username(greater than 5 characters): ")
			if len(self.username) < 5:
				print("Username less than 5 characters, please choose some other username!\n")
				continue

			self.username = self.apostrophe_balancing(self.username)

			sql_query = self.get_sql_query_check_username_exists()  # could have used try except since username has unique constraint in db so would give error
			df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
			
			if df.empty and len(self.username) >= 5:
				username_accepted = True
			else:
				print("Username already exists, please choose some other username!\n")
				
		regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
		pass_accepted = False
		while not pass_accepted:
			print("Please enter password(should be greater than 5 characters and should contain atleast one special character, one letter and one digit)")
			password = stdiomask.getpass()
			if len(password) > 5 and regex.search(password) != None and bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', password)) == True:
				print("Please enter password again to confirm!")
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

			if (re.fullmatch(regex, emailid)):
				sql_query = self.get_sql_query_check_emailid_exists(emailid)
				df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
				if df.empty:
					email_accepted = True
				else:
					print("Email-id already exists, please choose some other email-id!\n")
					continue
			else:
				print()
				print("Invalid email, enter again!\n")

		id_val = uuid.uuid1()
		sql_query = self.get_sql_query_to_add_new_user(emailid, password, id_val)

		try:
			with self.games_db_engine.connect() as con:
				con.execution_options(autocommit=True).execute(sql_query)
			print("\nUser creation successful!")
		except:
			raise Exception("\nUser creation not successful! :(")

	def login(self):
		user_accepted = False
		while not user_accepted:
			self.username = input("Please enter username: ")
			password = stdiomask.getpass()
			
			self.username = self.apostrophe_balancing(self.username)
			password = self.apostrophe_balancing(password)

			sql_query = self.get_sql_query_to_check_user_exists(password)
			df = pd.read_sql(sql=sql_query, con=self.games_db_engine)

			if not df.empty:
				user_accepted = True
			else:
				print("Username and/or Password you provided is/are incorrect, please enter again!\n")

		print("Logging in as {}...".format(self.username))
		time.sleep(1)

	def forgotpassword(self):
		username_accepted = False
		while not username_accepted:
			self.username = input("Please enter username: ")
			self.username = self.apostrophe_balancing(self.username)
			sql_query = self.get_sql_query_check_username_exists()
			df = pd.read_sql(sql=sql_query, con=self.games_db_engine)
			if not df.empty:
				username_accepted = True
			else:
				print("Username you provided is not incorrect, please enter again!")
		
		while True:
			emailid = df.iloc[0]['emailid']
			code = random.randint(1111,9999)

			msg = "Subject: OTP for password change.\n\nThe OTP for changing you password is: {}. Please take care of your privacy and never hare such mails or messages with anyone".format(str(code))
			s.sendmail('akshattesting123@gmail.com', emailid, msg)

			otp = input("An OTP has been sent to your email id -  {}, please enter here to reset your password: ".format('*'*(len(emailid)-7)+emailid[-13:]))
			if int(otp) == code:
				regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
				pass_accepted = False
				while not pass_accepted:			
					print("\nPlease enter password(should be greater than 5 characters and should contain atleast one special character, one letter and one digit)")
					password = stdiomask.getpass()
					if len(password) > 5 and regex.search(password) != None and bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', password)) == True:
						print("Please enter password again to confirm")
						password2 = stdiomask.getpass()
						if password == password2:
							pass_accepted = True
						else:
							print("Password mismatch!")
					else:
						print("Password is weak, enter again!")

				password = self.apostrophe_balancing(password)
				sql_query = self.get_sql_query_to_change_password(password)
				try:
					with self.games_db_engine.connect() as con:
						con.execution_options(autocommit=True).execute(sql_query)
					print("\nPassword change successful!")
				except:
					raise Exception("\nPassword change not successful! :(")
				
				return

			else:
				if input("You have not entered the correct otp, do you want to re-send otp? Press y for yes, else enter any key...").lower() != "y":
					return

	def startpage(self):
		while True:  # because we need to show the user login page again and again until user exits using option number 4

			while True:
				option = input("\nPlease choose an option:\n1. Login (If existing user)\n2. Signup\n3. Play as a guest\n4. Forgot password\n5. Exit\n")
				options = {"1":"login", "2":"signup","3":"guest","4":"forgot password","5":"exit"}
				if option in options:
					if option == '1':
						self.usertype = 'user'
						self.login()
						break
					elif option == '2':
						self.usertype = 'user'
						self.signup()
						break
					elif option == '3':
						self.usertype = 'guest'
						print("Logging in as a guest...")
						time.sleep(1)
						break
					elif option == '4':
						self.forgotpassword()
					else:
						return
				else:
					print("\nInvalid option! Choose again.")


			while True:
				choice = input("\nPlease choose from below:\n1. Play a game\n2. Check Scores (Only if you are a user)\n3. Back\n")
				if choice == "1":
					gametype = self.checkgametype()  # can be single, multi, or back option
					if gametype == None:  # no response means back option selected
						continue
					game = GamesScoresOptions(self.usertype, self.username, gametype)
					game.game_options()

				elif choice == "2":
					scores = GamesScoresOptions(self.usertype, self.username)
					scores.score_options()

				elif choice == "3":
					break

				else:
					print("Wrong option, please choose again!")

	def checkgametype(self):                           # check if 2 player game or single player 
		print("Do you want to play:\n1. Single Player\n2. Multi Player\n3. Back")
		while True:
			gametype = input()
			if gametype in self.gametypes:
				return self.gametypes[gametype]
			elif gametype == "3":
				return
			print("\nPlease enter a valid option!")

	def __str__(self):
		print("Start Page!")


if __name__ == '__main__':
	user = Start()
	user.startpage()
