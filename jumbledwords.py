import sys
sys.path.append("..") # Adds higher directory to python modules path.

from difficulty import Difficulty
from multiplayer import MultiPlayer
from gameresults import GameResults

class BaseJumbledWords(Difficulty):

	def __init__(self, usertype, gametype):
		self.usertype = usertype
		self.gametype = gametype

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