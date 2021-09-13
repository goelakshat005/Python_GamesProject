import sys
sys.path.append("..") # Adds higher directory to python modules path.

from difficulty import Difficulty
from multiplayer import MultiPlayer
from gameresults import GameResults

class JumbledWords(Difficulty):

	def __init__(self, gametype):
		self.gametype = gametype
		self.guessed_letters = ''
		self.name_while_guess = []
		
		if self.gametype == "multi":
			while True:
				self.random_name = getpass.getpass("Please enter word for {} to guess (word should be greater than or equal to 3 letters): ".format(self.name))  # mask the i/p
				if self.random_name.isspace() == False and len(self.random_name) >= 3:
					break
				print("Please enter a valid word!")

			while True:
				self.random_key = input("Please enter a hint for {}: ".format(name))
				if self.random_key.isspace() == False:
					break
				print("Please enter a valid hint!")

		elif self.gametype == "single":
			self.row_dict = super().get_word_row()
			self.random_key = self.row_dict['category']
			self.random_name = self.row_dict['word']
			self.random_name = " ".join((self.random_name).split())	

		self.turns = 0
		self.difficulty_level = ''
		self.name = ''
	def update_multiplayer_name(self, name):
		self.name = name

	def reset_class_vars(self):
		if self.gametype == "multi":
			while True:
				self.random_name = getpass.getpass("Please enter word for {} to guess (word should be greater than or equal to 3 letters): ".format(self.name))  # mask the i/p
				if self.random_name.isspace() == False and len(self.random_name) >= 3:
					break
				print("Please enter a valid word!")

			while True:
				self.random_key = input("Please enter a hint for {}: ".format(name))
				if self.random_key.isspace() == False:
					break
				print("Please enter a valid hint!")

		elif self.gametype == "single":
			self.row_dict = super().get_word_row()
			self.random_key = self.row_dict['category']
			self.random_name = self.row_dict['word']
			self.random_name = " ".join((self.random_name).split())



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

class BaseJumbledWords():
	def __init__(self):
		pass

	def handle(self):
		pass
		# options of games can be in 3 categories:
				# single
				# multiplayer - when the word is provided by the computer and both players are trying to answer first one wins
				# multiplayer - both players give each other words and other tries to answer
