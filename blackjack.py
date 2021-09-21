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

class BlackJack():

	card_types = ["clubs", "hearts", "spades", "diamond"]
	face_cards = ["king", "queen", "jack"]
	ace = "ace"
	total_decks = 1
	min_bet = 70
	
	def __init__(self, gametype, player1_amount, player2_amount):
		self.all_cards = []
		self.player1_cards = []
		self.player2_cards = []
		self.dealer_cards = []

		self.gametype = gametype
		self.name1 = ''
		self.name2 = ''
		
		self.player1_amount = player1_amount
		self.player2_amount = player2_amount
		self.player1_bet_amount = 0
		self.player2_bet_amount = 0

	def update_multiplayer_names(self, name1, name2):
		self.name1 = name1
		self.name2 = name2

	def get_new_decks(self):
		self.all_cards = []
		for deck in range(self.total_decks):
			for card_type in self.card_types:
				for num in range(2,11):
					self.all_cards.append((card_type, num))
				for face_card in self.face_cards:
					self.all_cards.append((card_type+"-"+face_card, 10))
				self.all_cards.append((card_type+"-"+self.ace, 1))         # aces can be considered as 11 but for sake of it, we take it as 1 for now
		random.shuffle(self.all_cards)

	def reset_vars(self):
		self.player1_cards = []
		self.player2_cards = []
		self.dealer_cards = []

		self.player1_bet_amount = 0
		self.player2_bet_amount = 0

	def user_game(self):

		if self.gametype == "single":
			return

		elif self.gametype == "multi": # take care of the amount calcualtion and then send back so that changes can be made when want to play this game no more
			option = input("Do you wanna go through rules once? (Press y/Y), else to start game press any key...")
			if option.lower() == "y":
				self.gamerules()
				# time.sleep(10)
			
			players = ["player1", "player2"]

			while True:
				self.reset_vars()
				self.get_new_decks()
				can_play = self.check_for_sufficient_balance("player1", self.min_bet)
				if can_play == "no":
					print("{} has insufficient balance, please add money to your account to play further!".format(self.name1))
					return self.player1_amount, self.player2_amount
				else:
					can_play = self.check_for_sufficient_balance("player2", self.min_bet)
					if can_play == "no":
						print("{} has insufficient balance, please add money to your account to play further!".format(self.name2))
						return self.player1_amount, self.player2_amount
				
				self.reset_bet_amounts()
				self.multiplayer_raise_bet()

				print("\nAmount that was raised/betted by {}: {}$".format(self.name1 ,self.player1_bet_amount))
				print("Amount that was raised/betted by {}: {}$".format(self.name2 ,self.player2_bet_amount))

				print("\nNow each player will be dealt two cards each and dealer will take 2 cards as well but one will be upside down.")
				self.first_round_deal_cards()
				
				dealer_num_of_cards_to_display = 1
				self.display_everyone_cards(dealer_num_of_cards_to_display)
				self.check_for_ace_facecard_combo()

				busted_players = self.round_of_dealing()
				if len(busted_players) < 2:
					dealer_busted = False
					self.display_cards_of_someone("dealer")
					while True:
						cards_value = self.get_values_of_cards_for_someone("dealer")
						if cards_value < 17:
							print("\nSince sum of dealer's cards is less than 17 so card will be taken by dealer.")
							self.deal_a_card("dealer")
							time.sleep(2)
							self.display_cards_of_someone("dealer")
						else:
							is_bust = self.check_for_bust(cards_value)
							if is_bust == "busted":
								print("Dealer got busted, dealer lost! Respective players (those who didn't bust in their chances) win!")
								dealer_busted = True
								break
							break

					if dealer_busted == True:
						for player in players:
							if player in busted_players:
								self.update_final_player_amounts(player, "lost")
							else:
								self.update_final_player_amounts(player, "won")
					else:
						players_result_list = self.compare_dealer_and_players_cards_values(players, busted_players)		
						for player, result in players_result_list:
							self.update_final_player_amounts(player, result)
				else:
					for player in players:
						self.update_final_player_amounts(player, "lost")

				self.display_final_player_amounts()

				if ((input("\nDo you want to play again? (Press y for yes), else enter any key...")).lower()) != 'y':
					print()
					return self.player1_amount, self.player2_amount


	def gamerules(self):
		print("Players make their bets.")
		print("Players are dealt 2 cards.")
		print("Dealer is dealt 2 cards where the second card is hidden from the players.")
		print("The objective of the game is to have a higher point total than the dealer (but no more than 21, anything over 21 is an automatic loss called a bust) — if you beat the dealer in this way, you win from the casino what you bet (you also win if the dealer busts). Aces can be worth either 1 or 11; every other card is worth its face amount (face cards are worth 10).")
		print("An initial 2 card hand composed of an ace and a face card is called a blackjack and is the best possible hand.")
		print("After the first round of dealing, each player has the option to hit (receive more cards) or stay (no more cards). If hitting results in the player busting (total going over 21), then his or her bet is lost.")
		print("After all the players are done hitting/staying, the dealer flips over his hidden card. If the dealer’s total is less than 17, then he or she needs to hit (receive a new card). This process repeats until the dealer’s hand either totals to 17 or more or busts (goes above 21).")
		print("After the dealer is done, the final results are decided — if the dealer busts, then any player who did not bust earlier wins his or her bet. If the dealer does not bust, then the dealer’s total is compared to each player’s. For any player whose total is greater than the dealer’s, he or she wins money (in the amount that was bet). For any player whose total is less than the dealer’s, he or she loses money. No money is exchanged in the event of a tie.")
		print("Player has to take care himself that his cards total value don't go over 21.\n")

	def compare_dealer_and_players_cards_values(self, players, busted_players):
		dealer_cards_value = self.get_values_of_cards_for_someone("dealer")
		players_result_list = []
		for player in players:
			if player not in busted_players:
				if player == "player1":
					player1_cards_value = self.get_values_of_cards_asking_for_ace_values_for_someone("player1")
					is_bust = self.check_for_bust(player1_cards_value)
					if is_bust == "busted":
						print("{}, you busted, should have entered proper values of aces!".format(self.name1))
						players_result_list.append((player, "lost"))
					else:
						if player1_cards_value > dealer_cards_value:
							players_result_list.append((player, "won"))
						elif player1_cards_value < dealer_cards_value:
							players_result_list.append((player, "lost"))
						elif player1_cards_value == dealer_cards_value:
							players_result_list.append((player, "tie"))

				elif player == "player2":
					player2_cards_value = self.get_values_of_cards_asking_for_ace_values_for_someone("player2")
					is_bust = self.check_for_bust(player2_cards_value)
					if is_bust == "busted":
						print("{}, you busted, should have entered proper values of aces!".format(self.name2))
						players_result_list.append((player, "lost"))
					else:
						if player2_cards_value > dealer_cards_value:
							players_result_list.append((player, "won"))
						elif player2_cards_value < dealer_cards_value:
							players_result_list.append((player, "lost"))
						elif player2_cards_value == dealer_cards_value:
							players_result_list.append((player, "tie"))
			else:
				if player == "player1":
					players_result_list.append((player, "lost"))

				elif player == "player2":
					players_result_list.append((player, "lost"))

		print("\nCalculating net value of cards for dealer: ")
		time.sleep(1)
		print("Total sum: ", dealer_cards_value)
		return players_result_list

	def round_of_dealing(self):
		busted_players = []
		print("\nFirst for {}:".format(self.name1))
		while True:
			option = input("Do you want to stay(want no more cards) or hit(want to be dealt more cards)? (type stay or hit respectively): ")
			if option == "stay":
				break
			elif option == "hit":
				self.deal_a_card("player1")
				self.display_cards_of_someone("player1")				
				cards_value = self.get_values_of_cards_for_someone("player1")
				is_bust = self.check_for_bust(cards_value)
				if is_bust == "busted":
					print("OOPS, you busted!")
					busted_players.append("player1")
					break

		print("\nNow for {}:".format(self.name2))
		while True:
			option = input("Do you want to stay(want no more cards) or hit(want to be dealt more cards)? (type stay or hit respectively): ")
			if option == "stay":
				break
			elif option == "hit":
				self.deal_a_card("player2")
				self.display_cards_of_someone("player2")
				cards_value = self.get_values_of_cards_for_someone("player2")
				is_bust = self.check_for_bust(cards_value)
				if is_bust == "busted":
					print("OOPS, you busted!")
					busted_players.append("player2")
					break

		return busted_players

	def deal_a_card(self, player):
		if len(self.all_cards) < 20:
			self.get_new_decks()

		if player == "player1":
			card = random.choice(self.all_cards)
			self.all_cards.remove(card)
			self.player1_cards.append(card)
		
		elif player == "player2":
			card = random.choice(self.all_cards)
			self.all_cards.remove(card)
			self.player2_cards.append(card)

		elif player == "dealer":
			card = random.choice(self.all_cards)
			self.all_cards.remove(card)
			self.dealer_cards.append(card)

	def display_cards_of_someone(self, player):
		if player == "player1":
			print("\nFor {}:".format(self.name1))
			for card in self.player1_cards:
				if card[0] in self.card_types:
					print("{} of {}".format(str(card[1]), card[0]))
				elif self.ace not in card[0]:
					card_split = card[0].split("-")
					print("{} of {} holding value {}".format(card_split[1], card_split[0], str(card[1])))
				else:
					card_split = card[0].split("-")
					print("{} of {} can have value of either 1 or 11".format(card_split[1], card_split[0]))

		elif player == "player2":
			print("\nFor {}:".format(self.name2))
			for card in self.player2_cards:
				if card[0] in self.card_types:
					print("{} of {}".format(str(card[1]), card[0]))
				elif self.ace not in card[0]:
					card_split = card[0].split("-")
					print("{} of {} holding value {}".format(card_split[1], card_split[0], str(card[1])))
				else:
					card_split = card[0].split("-")
					print("{} of {} can have value of either 1 or 11".format(card_split[1], card_split[0]))

		elif player == "dealer":
			print("\nDealer's cards:")
			for i in range(len(self.dealer_cards)):
				card = self.dealer_cards[i]
				if card[0] in self.card_types:
					print("{} of {}".format(str(card[1]), card[0]))
				elif self.ace not in card[0]:
					card_split = card[0].split("-")
					print("{} of {} holding value {}".format(card_split[1], card_split[0], str(card[1])))
				else:
					card_split = card[0].split("-")
					print("{} of {} can have value of either 1 or 11".format(card_split[1], card_split[0]))

	def get_values_of_cards_for_someone(self, player):
		if player == "player1":
			cards_value = 0
			for card in self.player1_cards:
				cards_value += card[1]

		elif player == "player2":
			cards_value = 0
			for card in self.player2_cards:
				cards_value += card[1]

		elif player == "dealer":
			cards_value = 0
			ace_count = 0
			ace_sum_with_one_ace_as_11 = 0
			ace_sum_with_all_aces_as_1 = 0
			for card in self.dealer_cards:
				if 'ace' in  card[0]:
					ace_count += 1
					if ace_count == 1:
						ace_sum_with_one_ace_as_11 += 11
						ace_sum_with_all_aces_as_1 += 1
					else:
						ace_sum_with_one_ace_as_11 += 1
						ace_sum_with_all_aces_as_1 += 1	
				else:
					cards_value += card[1]

			if ace_count == 1 and cards_value <= 10:
				cards_value += 11
			elif ace_count == 1 and cards_value > 10:
				cards_value += 1
			elif ace_count > 1 and (cards_value + ace_sum_with_one_ace_as_11) <= 21:
				cards_value += ace_sum_with_one_ace_as_11
			elif ace_count > 1:
				cards_value += ace_sum_with_all_aces_as_1
			# more than one aces can never have more than one aces valued at 11, sum will be 22
		
		return cards_value

	def get_values_of_cards_asking_for_ace_values_for_someone(self, player):
		ace_counts = {1:"first", 2:"second", 3:"third", 4:"fourth"}
		if player == "player1":
			print("\nCalculating net value of cards for {}: ".format(self.name1))
			time.sleep(1)
			cards_value = 0
			ace_count = 0
			for card in self.player1_cards:
				if self.ace in card[0]:
					ace_count += 1
					while True:
						print("Please enter the value of {} ace you have (1 or 11): ".format(ace_counts[ace_count]), end = '')
						ace_value = input()
						if ace_value == "1" or ace_value == "11":
							cards_value += int(ace_value)
							break
						else:	
							print("Please enter a valid value!")
				else:
					cards_value += card[1]
			print("Total sum:", cards_value)

		elif player == "player2":
			print("\nCalculating net value of cards for {}: ".format(self.name2))
			time.sleep(1)
			cards_value = 0
			ace_count = 0
			for card in self.player2_cards:
				if self.ace in card[0]:
					ace_count += 1
					while True:
						print("Please enter the value of {} ace you have (1 or 11): ".format(ace_counts[ace_count]), end = '')
						ace_value = input()
						if ace_value == "1" or ace_value == "11":
							cards_value += int(ace_value)
							break
						else:	
							print("Please enter a valid value!")
				else:
					cards_value += card[1]
			print("Total sum:", cards_value)

		return cards_value

	def check_for_bust(self, value):
		if value > 21:
			return "busted"

	def first_round_deal_cards(self):
		for i in range(2):
			card = random.choice(self.all_cards)
			self.all_cards.remove(card)
			self.player1_cards.append(card)
		for i in range(2):
			card = random.choice(self.all_cards)
			self.all_cards.remove(card)
			self.player2_cards.append(card)
		for i in range(2):
			card = random.choice(self.all_cards)
			self.all_cards.remove(card)
			self.dealer_cards.append(card)


	def display_everyone_cards(self, dealer_num_of_cards_to_display):
		print("\nFor {}:".format(self.name1))
		for card in self.player1_cards:
			if card[0] in self.card_types:
				print("{} of {}".format(str(card[1]), card[0]))
			elif self.ace not in card[0]:
				card_split = card[0].split("-")
				print("{} of {} holding value {}".format(card_split[1], card_split[0], str(card[1])))
			else:
				card_split = card[0].split("-")
				print("{} of {} can have value of either 1 or 11".format(card_split[1], card_split[0]))

		print("\nFor {}:".format(self.name2))
		for card in self.player2_cards:
			if card[0] in self.card_types:
				print("{} of {}".format(str(card[1]), card[0]))
			elif self.ace not in card[0]:
				card_split = card[0].split("-")
				print("{} of {} holding value {}".format(card_split[1], card_split[0], str(card[1])))
			else:
				card_split = card[0].split("-")
				print("{} of {} can have value of either 1 or 11".format(card_split[1], card_split[0]))

		print("\nDealer's cards:")
		for i in range(dealer_num_of_cards_to_display):
			card = self.dealer_cards[i]
			if card[0] in self.card_types:
				print("{} of {}".format(str(card[1]), card[0]))
			elif self.ace not in card[0]:
				card_split = card[0].split("-")
				print("{} of {} holding value {}".format(card_split[1], card_split[0], str(card[1])))
			else:
				card_split = card[0].split("-")
				print("{} of {} can have value of either 1 or 11".format(card_split[1], card_split[0]))

	def check_for_ace_facecard_combo(self):
		ace_found = False
		face_card_found = False
		for card in self.player1_cards:
			if self.ace in card[0]:
				ace_found=True
			elif card[0] not in self.card_types or card[1]==10:
				face_card_found=True
		if ace_found == True and face_card_found == True:
			print("\n{} you have the best possible combo!".format(self.name1))

		ace_found = False
		face_card_found = False
		for card in self.player2_cards:
			if self.ace in card[0]:
				ace_found=True
			elif card[0] not in self.card_types or card[1]==10:
				face_card_found=True
		if ace_found == True and face_card_found == True:
			print("\n{} you have the best possible combo!".format(self.name2))

	def reset_bet_amounts(self):
		self.player1_bet_amount = 0
		self.player2_bet_amount = 0

	def update_final_player_amounts(self, player, result):
		if player == "player1":
			if result == "won":
				print("\n{} you won this round.".format(self.name1))
				self.player1_amount += self.player1_bet_amount
			elif result == "lost":
				print("\n{} you lost this round.".format(self.name1))
				self.player1_amount -= self.player1_bet_amount
			elif result == "tie":
				print("\n{} you tied in this round.".format(self.name1))

		if player == "player2":
			if result == "won":
				print("{} you won this round.".format(self.name2))
				self.player2_amount += self.player2_bet_amount
			elif result == "lost":
				print("{} you lost this round.".format(self.name2))
				self.player2_amount -= self.player2_bet_amount
			elif result == "tie":
				print("{} you tied in this round.".format(self.name2))
				
	def display_final_player_amounts(self):
		print("\nYour final amounts are: ")
		print("{}: {}$".format(self.name1, self.player1_amount))
		print("{}: {}$\n".format(self.name2, self.player2_amount))

	def check_for_sufficient_balance(self, player, check_amount):
		if player == "player1" and self.player1_amount < check_amount:
			return "no"
		elif player == "player2" and self.player2_amount < check_amount:
			return "no"
		
	def multiplayer_raise_bet(self):
		# can_raise_players = []
		# can_raise1 = self.check_for_sufficient_balance("player1", self.min_raise)
		# if can_raise1 == "no":
		# 	print("{} has insufficient balance for any further raise!".format(self.name1))
		# else:
		# 	can_raise_players.append("player1")

		# can_raise2 = self.check_for_sufficient_balance("player2", self.min_raise)
		# if can_raise2 == "no":
		# 	print("{} has insufficient balance, please money to your account to play further!".format(self.name2))
		# else:
		# 	can_raise_players.append("player2")

		# if can_raise1 == "no" and can_raise2 == "no":
		# 	return

		# if "player1" in can_raise_players:
		while True:
			print("\n{}, please enter the amount by which you want to raise, enter whole numbers! (minimum bet of 50$): ".format(self.name1.capitalize()), end = "")
			player1_bet = input()
			if player1_bet.isnumeric():
				if int(player1_bet) >= 50:
					can_raise1 = self.check_for_sufficient_balance("player1", int(player1_bet))
					if can_raise1 == "no":
						print("{}, please consider a different amount to raise, you have insufficicent balance!".format(self.name1))
					else:
						# self.player1_amount -= int(player1_bet)
						self.player1_bet_amount += int(player1_bet)
						break
				else:
					print("Please enter an amount greater than or equal to 50$.")
			else:
				print("Enter valid amount!")

		# if "player2" in can_raise_players:
		while True:
			print("{}, please enter the amount by which you want to raise, enter whole numbers! (minimum bet of 50$): ".format(self.name2.capitalize()), end = "")
			player2_bet = input()
			if player2_bet.isnumeric():
				if int(player2_bet) >= 50:
					can_raise2 = self.check_for_sufficient_balance("player2", int(player2_bet))
					if can_raise2 == "no":
						print("{}, please consider a different amount to raise, you have insufficicent balance!".format(self.name2))
					else:
						# self.player2_amount -= int(player2_bet)
						self.player2_bet_amount += int(player2_bet)
						break
				else:
					print("Please enter an amount greater than or equal to 50$.")
			else:
				print("Enter valid amount!")


class BaseBlackJack(GameResults):
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
# 			# multi_instance = MultiPlayer()
# 			# name1 = multi_instance.player1_name()
# 			# name2 = multi_instance.player2_name()
			return

		elif self.gametype == "multi":
			play = BlackJack(self.gametype, self.player1_amount, self.player2_amount)
			play.update_multiplayer_names(self.name1, self.name2)
			player1_amount, player2_amount = play.user_game()
			return player1_amount, player2_amount

# if __name__ == '__main__':
# 	obj = BlackJack()
