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

class CoinFlip():

	coin_results = {'1':'Heads', '2':'Tails'}

	def __init__(self, gametype, player1_amount, player2_amount):
		self.gametype = gametype
		self.name1 = ''
		self.name2 = ''
		self.player1_amount = player1_amount
		self.player2_amount = player2_amount

	def update_multiplayer_names(self, name1, name2):
		self.name1 = name1
		self.name2 = name2

	def user_game(self):

		if self.gametype == "single":
			return

		elif self.gametype == "multi": # take care of the amount calcualtion and then send back so that changes can be made when want to play this game no more
			print("In this game both players get a chance to choose alteratively, the coin will be flipped, result can be either Heads or Tails. Bets will be placed before that.")
			print("The starting bet is of 50$ and the raise can be made of 10$/20$/30$.")

			players = ["player1", "player2"]   # chances will be given alternatively
			chance_of = "player1"
			while True:
				start_amount = 50
				can_play, player = self.check_bet(start_amount)
				if can_play == "no":
					# if player == "player1":				
					# 	print("{} you have insufficient balance to play, please consider adding amount to play!".format(self.name1))
					# elif player == "player2":
					# 	print("{} you have insufficient balance to play, please consider adding amount to play!".format(self.name2))
					return self.player1_amount, self.player2_amount

				self.player1_amount -= start_amount
				self.player2_amount -= start_amount

				raise_amount, player_who_lost = self.multiplayer_raise_bet(chance_of)
				print("\nFinal amount that was raised/betted: {}$".format(raise_amount))
				if player_who_lost == "":
					choice = self.choose_side_of_coin(chance_of)
					choice_of_player1 = choice
					result = random.choice(list(self.coin_results.values()))
					print("Flipping coin...")
					time.sleep(1)
					print("Coin shows:", result)
					if result == choice_of_player1:
						self.update_amounts("player1", raise_amount)
					else:
						self.update_amounts("player2", raise_amount)

				elif player_who_lost == "player1":
					self.update_amounts("player2", raise_amount)
				
				elif player_who_lost == "player2":
					self.update_amounts("player1", raise_amount)


				if chance_of == "player1":
					chance_of = "player2"
				
				else:
					chance_of = "player1"	
				
				can_play, player = self.check_bet(start_amount)
				if can_play == "no":
					return self.player1_amount, self.player2_amount
				
				if ((input("\nDo you want to play again? (Press y for yes), else enter any key...")).lower()) != 'y':
					print()
					return self.player1_amount, self.player2_amount

	def update_amounts(self, player_won, raise_amount):
		if player_won == "player1":
			print("\n{} you won this round.".format(self.name1))
			self.player1_amount += (2*raise_amount)
		elif player_won == "player2":
			print("\n{} you won this round.".format(self.name2))
			self.player2_amount += (2*raise_amount)

		print("\nYour final amounts are: ")
		print("{}: {}$".format(self.name1, self.player1_amount))
		print("{}: {}$\n".format(self.name2, self.player2_amount))

	def choose_side_of_coin(self, chance_of):
		if chance_of == "player1":
			print("\n{} enter your choice.\n1. Heads\n2. Tails".format(self.name1))
		elif chance_of == "player2":
			print("\n{} enter your choice.\n1. Heads\n2. Tails".format(self.name2))
		
		while True:
			option = input("Enter your choice: ")
			if option in ['1','2']:
				print("You choose:", self.coin_results[option])
				return self.coin_results[option]
			else:
				print("Please select valid option.")

	def check_bet(self, check_amount):
		if self.player1_amount < check_amount:
			return "no", "player1"
		elif self.player2_amount < check_amount:
			return "no", "player2"
		else:
			return "yes", ""

	def multiplayer_raise_bet(self, chance_of):
		min_bet = 10
		can_play, player = self.check_bet(min_bet)
		if can_play == "no":
			if player == "player1":				
				print("{} you have insufficient balance for a raise!".format(self.name1))
			elif player == "player2":
				print("{} you have insufficient balance for a raise!".format(self.name2))
			return 50, ""

		player_who_wants_to_raise = ""

		if chance_of == "player1":
			print("\nDo you want to raise amount {}? (Press y for yes), else enter any key... ".format(self.name1))
			if ((input()).lower()) == 'y':
				player_who_wants_to_raise = "player1"
			if player_who_wants_to_raise == "":
				print("\nDo you want to raise amount {}? (Press y for yes), else enter any key... ".format(self.name2))
				if ((input()).lower()) == 'y':
					player_who_wants_to_raise = "player2"

		elif chance_of == "player2":
			print("\nDo you want to raise amount {}? (Press y for yes), else enter any key... ".format(self.name2))
			if ((input()).lower()) == 'y':
				player_who_wants_to_raise = "player2"
			if player_who_wants_to_raise == "":
				print("\nDo you want to raise amount {}? (Press y for yes), else enter any key... ".format(self.name1))
				if ((input()).lower()) == 'y':
					player_who_wants_to_raise = "player1"

		if player_who_wants_to_raise == "":
			return 50, ""

		elif player_who_wants_to_raise != "":
			amount_raised, value, player_who_lost = self.check_for_raise(player_who_wants_to_raise)
			if value == "lost":
				return amount_raised, player_who_lost
			elif value == "":
				return amount_raised, ""

	def check_for_raise(self, player_who_raised):
		amount_raised = 50
		min_bet = 10
		while True:
			if player_who_raised == "player1":
				name_who_raised = self.name1
				player_to_check_for_raise = "player2"
				name_to_check_for_raise = self.name2
			else:
				name_who_raised = self.name2
				player_to_check_for_raise = "player1" 
				name_to_check_for_raise = self.name1

			while True:
				print("{} please enter the amount by which you want to raise, can be 10$/20$/30$!".format(name_who_raised))
				amount = input()
				if amount in ["20","30"]:
					amount = int(amount)
					can_play, player = self.check_bet(amount)
					if can_play == "no":
						if player == "player1":				
							print("{} has insufficient balance for a raise of that amount, try lesser amount!".format(self.name1))
						elif player == "player2":
							print("{} has insufficient balance for a raise of that amount, try lesser amount!".format(self.name2))
						continue
					else:
						print("{}, do you wanna comply and raise this amount, if you choose not to you will lose your money raised up till now. (Press y for yes), else enter any key...".format(name_to_check_for_raise))
						yes_or_no = input().lower()
						if yes_or_no != 'y':
							return amount_raised, "lost", player_to_check_for_raise
						
						self.player1_amount -= amount
						self.player2_amount -= amount
						amount_raised += amount
						print("Amount raised up till now:", amount_raised)

						can_play, player = self.check_bet(min_bet)
						if can_play == "no":
							if player == "player1":				
								print("{} has insufficient balance for any further raise!".format(self.name1))
							elif player == "player2":
								print("{} has insufficient balance for any further raise!".format(self.name2))
							return amount_raised, "", ""
						else:
							print("\n{}, do you wanna raise further? (Press y for yes), else enter any key...".format(name_to_check_for_raise))
							yes_or_no = input().lower()
							if yes_or_no == 'y':
								if player_who_raised == "player1":
									player_who_raised = "player2"
								else:
									player_who_raised = "player1"
								break
							else:
								return amount_raised, "", ""

				elif amount == "10":
					amount = int(amount)
					print("{}, do you wanna comply and raise this amount, if you choose not to you will lose your money raised up till now. (Press y for yes), else enter any key...".format(name_to_check_for_raise))
					yes_or_no = input().lower()
					if yes_or_no != 'y':
						return amount_raised, "lost", player_to_check_for_raise
					
					self.player1_amount -= amount
					self.player2_amount -= amount
					amount_raised += amount
					print("Amount raised up till now:", amount_raised)
					
					can_play, player = self.check_bet(min_bet)
					if can_play == "no":
						if player == "player1":				
							print("{} has insufficient balance for any further raise!".format(self.name1))
						elif player == "player2":
							print("{} has insufficient balance for any further raise!".format(self.name2))
						return amount_raised, "", ""
					else:
						print("\n{}, do you wanna raise further? (Press y for yes), else enter any key...".format(name_to_check_for_raise))
						yes_or_no = input().lower()
						if yes_or_no == 'y':
							if player_who_raised == "player1":
								player_who_raised = "player2"
							else:
								player_who_raised = "player1"
							break
						else:
							return amount_raised, "", ""

				else:
					print("Please enter a valid amount!")

class BaseCoinFlip(GameResults):
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
			play = CoinFlip(self.gametype, self.player1_amount, self.player2_amount)
			play.update_multiplayer_names(self.name1, self.name2)
			player1_amount, player2_amount = play.user_game()
			return player1_amount, player2_amount
