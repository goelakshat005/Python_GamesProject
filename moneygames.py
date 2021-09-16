import random
import getpass
import pandas as pd
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from difficulty import Difficulty
from multiplayer import MultiPlayer
from gameresults import GameResults
from coinflip import BaseCoinFlip

class BaseMoneyGames():

	min_budget = 500
	max_budget = 1000
	
	game_options = {"1":"CoinFlip", "2":"BlackJack", "3":"HighLow", "4":"End Game/Show Results"}

	game_objects = {"CoinFlip": BaseCoinFlip,
					"BlackJack":"",
					"HighLow":""
				   }

	def __init__(self, usertype, gametype, username=''):
		self.usertype = usertype
		self.gametype = gametype
		self.username = username

		print("This is a special package of money games in which an initial amount is decided by each player, then you and your friend need to bet money on a chosen game and the betted amount "\
			  "can be raised by the other player and if the player is not ready to raise then that specific game ends there, then another game can be chosen, if not then the final amount "\
			  "is shown of who owes who, and what amount is actually left with each players.")

	def handle(self):
		multi_instance = MultiPlayer()
		name1 = multi_instance.player1_name()
		name2 = multi_instance.player2_name()
		print("The max budget you can have for this whole package is 1000 while the min budget is 500!")
		player1_starting_amount, player2_starting_amount = multi_instance.get_players_starting_amounts(self.min_budget, self.max_budget)
		print("{} has given an initial budget of: {}".format(name1, player1_starting_amount))
		print("{} has given an initial budget of: {}".format(name2, player2_starting_amount))

		while True:
			print("Please choose the game you want to play from below:")
			while True:
				for key, value in self.game_options.items():
					print("{}. {}".format(key, value))

				option = input("Please enter your choice: ")
				if option in self.game_options:
					break
				else:
					print("Invalid option! Choose again.\n")
			
			self.game = self.game_options[option]
			if self.game != 'End Game/Show Results':
				player1_amount = multi_instance.player1_amount()
				player2_amount = multi_instance.player2_amount()
				play = self.game_objects[self.game](self.usertype, self.gametype, self.username, player1_amount, player2_amount)       # a new object is created everytime
				play.update_multiplayer_names(name1, name2)
				play.handle()
			else:
				return