import random
import getpass
import pandas as pd
import os
import time
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from difficulty import Difficulty
from multiplayer import MultiPlayer
from gameresults import GameResults

class HighLow():

	min_bet = 10

	def __init__(self, gametype, player1_amount, player2_amount):
		self.gametype = gametype
		self.name1 = ''
		self.name2 = ''
		self.player1_amount = player1_amount
		self.player2_amount = player2_amount
		self.dice_pairs = self.dices_pair_options()

	def update_multiplayer_names(self, name1, name2):
		self.name1 = name1
		self.name2 = name2

	def dices_pair_options(self):
		dice_pairs = []
		for dice_value in range(1,7):
			for dice_value2 in range(1,7):
				dice_pairs.append((dice_value, dice_value2))

		random.shuffle(dice_pairs)
		return dice_pairs

	def user_game(self):

		if self.gametype == "single":
			return

		elif self.gametype == "multi": # take care of the amount calcualtion and then send back so that changes can be made when want to play this game no more
			print("Both players will get a chance to choose whether the sum of value on 2 dices adding up will be greater than 7, less than 7 or equal to 7, the "\
				"the dices will be rolled, result can be >7/=7/<7. Bets will be placed before that.")
			print("The minimum amount that can bet is 10$ and can extend to any multiple of 10 upto 100$.")

			while True:
				can_play, player = self.check_bet(self.min_bet)
				if can_play == "no":
					# if player == "player1":				
					# 	print("{} you have insufficient balance to play, please consider adding amount to play!".format(self.name1))
					# elif player == "player2":
					# 	print("{} you have insufficient balance to play, please consider adding amount to play!".format(self.name2))
					return self.player1_amount, self.player2_amount

				player1_raise_amount, player2_raise_amount = self.multiplayer_raise_bet()
				print("\nAmount that was raised/betted by {}: {}$".format(self.name1, player1_raise_amount))
				print("Amount that was raised/betted by {}: {}$".format(self.name2, player2_raise_amount))

				choice_player1, choice_player2 = self.choose_dice_sum_option()
				print("\nRolling dices, hold on...")
				# time.sleep(1)
				random_dice_pair = random.choice(self.dice_pairs)
				dices_sum = random_dice_pair[0] + random_dice_pair[1]
				print("First dice value: {}, Second dice value: {}".format(random_dice_pair[0], random_dice_pair[1]))
				if dices_sum > 7:
					result_option = "1"
				elif dices_sum < 7:
					result_option = "2"
				elif dices_sum == 7:
					result_option = "3"

				if choice_player1 == result_option:
					self.update_amounts("player1", "won", player1_raise_amount)
				else:
					self.update_amounts("player1", "lost", player1_raise_amount)


				if choice_player2 == result_option:
					self.update_amounts("player2", "won", player2_raise_amount)
				else:
					self.update_amounts("player2", "lost", player2_raise_amount)


				self.display_final_amounts()
				
				can_play, player = self.check_bet(self.min_bet)
				if can_play == "no":
					# if player == "player1":				
					# 	print("{} you have insufficient balance to play, please consider adding amount to play!".format(self.name1))
					# elif player == "player2":
					# 	print("{} you have insufficient balance to play, please consider adding amount to play!".format(self.name2))
					return self.player1_amount, self.player2_amount
				
				if ((input("\nDo you want to play again? (Press y for yes), else enter any key...")).lower()) != 'y':
					print()
					return self.player1_amount, self.player2_amount

	def update_amounts(self, player, result, raise_amount):
		if player == "player1":
			if result == "won":
				print("\n{} you won this round.".format(self.name1))
				self.player1_amount += raise_amount
			else:
				print("\n{} you lost this round.".format(self.name1))
				self.player1_amount -= raise_amount
		
		elif player == "player2":
			if result == "won":
				print("\n{} you won this round.".format(self.name2))
				self.player2_amount += raise_amount
			else:
				print("\n{} you lost this round.".format(self.name2))
				self.player2_amount -= raise_amount

	def display_final_amounts(self):
		print("\nYour final amounts are: ")
		print("{}: {}$".format(self.name1, self.player1_amount))
		print("{}: {}$\n".format(self.name2, self.player2_amount))

	def choose_dice_sum_option(self):
		while True:
			print("\nPlease enter your choice {}: 1. Greater than 7, 2: Less than 7, 3: Equal to 7".format(self.name1))
			choice_player1 = input()
			if choice_player1 in ["1", "2", "3"]:
				break
			else:
				print("\nYou entered wrong choice. Choose again.")

		while True:
			print("\nPlease enter your choice {}: 1. Greater than 7, 2: Less than 7, 3: Equal to 7".format(self.name2))
			choice_player2 = input()
			if choice_player2 in ["1", "2", "3"]:
				break
			else:
				print("\nYou entered wrong choice. Choose again.")

		return choice_player1, choice_player2

	def check_bet(self, check_amount):
		if self.player1_amount < check_amount:
			return "no", "player1"
		elif self.player2_amount < check_amount:
			return "no", "player2"
		else:
			return "yes", ""

	def check_bet_for_player(self, player, check_amount):
		if player == "player1":
			if self.player1_amount < check_amount:
				return "no"
			else:
				return "yes"
		else:
			if self.player2_amount < check_amount:
				return "no"
			else:
				return "yes"

	def multiplayer_raise_bet(self):
		player1_bet_amount = 0
		print("\nDo you want to raise amount {}? (Press y for yes), else enter any key... ".format(self.name1))
		if ((input()).lower()) == 'y':
			while True:
				print("{}, please enter the amount by which you want to raise (max 100$, min 10$): ".format(self.name1), end = '')
				amount = input()
				if amount.isnumeric() == True:
					amount = int(amount)
					if amount >= 10 and amount <= 100:
						can_play = self.check_bet_for_player("player1", amount)
						if can_play == "yes":
							player1_bet_amount += amount
							break
						else:
							print("Consider entering a different amount, you have insufficient balance for this amount raise!")
					else:
						print("Please enter a value between 10 and 100!")
				else:
					print("Please enter a valid number!")

		player2_bet_amount = 0
		print("\nDo you want to raise amount {}? (Press y for yes), else enter any key... ".format(self.name2))
		if ((input()).lower()) == 'y':
			while True:
				print("{}, please enter the amount by which you want to raise (max 100$, min 10$): ".format(self.name2), end = '')
				amount = input()
				if amount.isnumeric() == True:
					amount = int(amount)
					if amount >= 10 and amount <= 100:
						can_play = self.check_bet_for_player("player2", amount)
						if can_play == "yes":
							player2_bet_amount += amount
							break
						else:
							print("Consider entering a different amount, you have insufficient balance for this amount raise!")
					else:
						print("Please enter a value between 10 and 100!")				
				else:
					print("Please enter a valid number!")

		return player1_bet_amount, player2_bet_amount

class BaseHighLow(GameResults):
	def __init__(self, usertype, gametype, username='', player1_amount='', player2_amount=''):
		self.usertype = usertype
		self.gametype = gametype
		self.username = username
		self.player1_amount = player1_amount
		self.player2_amount = player2_amount

	def update_multiplayer_names(self, name1, name2):
		self.name1 = name1
		self.name2 = name2

	def handle(self):
		if self.gametype == "single":
			# multi_instance = MultiPlayer()
			# name1 = multi_instance.player1_name()
			# name2 = multi_instance.player2_name()
			return

		elif self.gametype == "multi":
			play = HighLow(self.gametype, self.player1_amount, self.player2_amount)
			play.update_multiplayer_names(self.name1, self.name2)
			player1_amount, player2_amount = play.user_game()
			return player1_amount, player2_amount
