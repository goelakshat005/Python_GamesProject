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

	game_starting_bet = {"CoinFlip": 50,
						 "BlackJack": 70,
						 "HighLow":10
						}

	def __init__(self, usertype, gametype, username=''):
		self.usertype = usertype
		self.gametype = gametype
		self.username = username

		self.name1 = ''
		self.name2 = ''
		self.game = ''

		print("This is a special package of money games in which an initial budget is decided by each player and multiple games can be played within that budget, "\
			  "then you and your friend need to bet money on a chosen game and the amount "\
			  "can be raised by each of the player, multiple games can be chosen from to play, the final amount "\
			  "is shown of how much money each player has, and what amount is owed by whom to who.")

	def handle(self):
		multi_instance = MultiPlayer()
		self.name1 = multi_instance.player1_name()
		self.name2 = multi_instance.player2_name()
		print("The max budget you can have for this whole package is 1000 while the min budget is 500!")
		print()
		player1_starting_amount, player2_starting_amount = multi_instance.get_players_starting_amounts(self.min_budget, self.max_budget)
		print("{} has given an initial budget of: {}".format(self.name1, player1_starting_amount))
		print("{} has given an initial budget of: {}".format(self.name2, player2_starting_amount))

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
				player1_amount = multi_instance.get_player1_amount()
				player2_amount = multi_instance.get_player2_amount()
				possibility = self.check_if_game_can_be_played(player1_amount, player2_amount)
				if possibility == "no_possible_game":
					break
				elif possibility == "this_game_not_possible":
					continue

				play = self.game_objects[self.game](self.usertype, self.gametype, self.username, player1_amount, player2_amount)  # a new object is created
				play.update_multiplayer_names(self.name1, self.name2)
				player1_amount, player2_amount = play.handle()
				multi_instance.update_player1_amount(player1_amount)
				multi_instance.update_player2_amount(player2_amount)
			else:
				break

		player1_starting_amount = multi_instance.get_player1_starting_amount()
		player2_starting_amount = multi_instance.get_player2_starting_amount()
		player1_amount = multi_instance.get_player1_amount()
		player2_amount = multi_instance.get_player2_amount()

		print("\n{}, you started with {}$ amount, and now you have {}$.".format(self.name1, player1_starting_amount, player1_amount))
		print("{}, you started with {}$ amount, and now you have {}$.".format(self.name2, player2_starting_amount, player2_amount))	
		if player1_amount > player1_starting_amount:
			print("{} you owe {} this amount - {}$\n".format(self.name2, self.name1, str(player2_starting_amount-player2_amount)))
		elif player2_amount > player2_starting_amount:
			print("{} you owe {} this amount - {}$\n".format(self.name1, self.name2, str(player1_starting_amount-player1_amount)))

	def check_if_game_can_be_played(self, player1_amount, player2_amount):
		if player1_amount < self.game_starting_bet[self.game]:
			if self.game == "HighLow":
				print("{}, you cannot play any game at this point of time, please add money to play further!".format(self.name1))
				return "no_possible_game"
			else:
				print("{}, you cannot play this game at this point of time, try another or add more money!".format(self.name1))
				return "this_game_not_possible"

		elif player2_amount < self.game_starting_bet[self.game]:
			if self.game == "HighLow":
				print("{} you cannot play any game at this point of time, please add money to play further!".format(self.name2))
				return "no_possible_game"
			else:
				print("{} you cannot play this game at this point of time, try another or add more money!".format(self.name2))
				return "this_game_not_possible"

		else:
			return ''