import random
import time

from common.multiplayer import MultiPlayer
from common.gameresults import GameResults

class CowsAndBulls():

	def __init__(self, gametype):
		self.gametype = gametype
		self.name = ''
	
	def update_multiplayer_name(self, name):
		self.name = name

	def user_game(self):

		if self.gametype == "single":
			result = self.game()
			return result

		elif self.gametype == "multi":
			result = self.game()
			return result

	def game(self):
		while True:
			code = random.randint(1000,9999)
			code_digits_list = list(str(code))
			if len(set(code_digits_list)) != 4:
				continue
			else:
				break
		
		print("Getting secret code.")
		time.sleep(1)
		guessed_code = "*"*4
		print("\nCode:", guessed_code)
		total_number_of_guesses = 0
		already_guessed = []
		while True:
			cows = 0
			bulls = 0
			print()
			guess = input("Please enter your guess or type 'giveup' if you wanna give up: ")
			if guess.isnumeric() and len(set(list(guess))) == 4:
				if guess == str(code):
					total_number_of_guesses += 1
					print("You won in {} number of chances.".format(total_number_of_guesses))
					return total_number_of_guesses
				
				elif guess in already_guessed:
					print("You have already guessed this code!")
					continue

				else:
					total_number_of_guesses += 1
					guess_digits_list = list(guess)
					for ind in range(len(guess_digits_list)):
						if guess_digits_list[ind] == code_digits_list[ind]:
							bulls += 1
						elif guess_digits_list[ind] in code_digits_list:
							cows += 1
					print("\nCows: {}, Bulls: {}".format(cows, bulls))
				
				already_guessed.append(guess)
				print("You have taken {} chances up till now.".format(total_number_of_guesses))

			elif guess == "giveup":
				print("Code was:", code)
				return 'giveup' 

			else:
				print("Enter a valid guess!")

class BaseCowsAndBulls(GameResults):
	def __init__(self, usertype, gametype, username=''):
		self.usertype = usertype
		self.gametype = gametype
		self.username = username

		if self.gametype == "single":
			print("\nA player will get a secret code, usually a 4-digit number.  This number will have no repeated digits.")
			print("Player makes a guess (4 digit number) to crack the secret number. Upon making a guess, 2 hints will be provided- Cows and Bulls.")
			print("Bulls indicate the number of correct digits in the correct position and cows indicates the number of correct digits in the wrong position. For example, if the secret code is 1234 and the guessed number is 1246 then we have 2 BULLS (for the exact matches of digits 1 and 2) and 1 COW (for the match of digit 4 in the wrong position)")
			print("The player keeps on guessing until the secret code is cracked. The player should take the minimum number of tries wins.")
			
		elif self.gametype == "multi":
			print("\nA player will create a secret code, usually a 4-digit number.  This number should have no repeated digits.")
			print("Another player makes a guess (4 digit number) to crack the secret number. Upon making a guess, 2 hints will be provided- Cows and Bulls.")
			print("Bulls indicate the number of correct digits in the correct position and cows indicates the number of correct digits in the wrong position. For example, if the secret code is 1234 and the guessed number is 1246 then we have 2 BULLS (for the exact matches of digits 1 and 2) and 1 COW (for the match of digit 4 in the wrong position)")
			print("The player keeps on guessing until the secret code is cracked. The player who guesses in the minimum number of tries wins.")

	def handle(self):
		if self.gametype == "single":
			while True:
				play = CowsAndBulls(self.gametype)
				result = play.user_game()
				if result != "giveup":
					if self.usertype != 'guest':
						super().base_results(self.username, "CowsAndBulls", '', result, False, True)  # blank signifies the difficulty level and False signifies 
						# if we need to save a game with difficulty levels and True signifies that it's a score type game with no win or lose
						super().display_games_with_only_scores(self.username, "CowsAndBulls")

				if ((input("\nDo you want to play again? (Press y for yes), else enter any key... ")).lower()) != 'y':
					return

		elif self.gametype == "multi":
			multi_instance = MultiPlayer()
			while True:
				players = ['player1', 'player2']
				for player in players:
					if player == "player1":
						name = multi_instance.player1_name()
						print("{} playing first.".format(name))
						play = CowsAndBulls(self.gametype)
						play.update_multiplayer_name(name)
						result_player1 = play.user_game()

					else:
						name = multi_instance.player2_name()
						print("\n{} playing now.".format(name))	
						play = CowsAndBulls(self.gametype)							
						play.update_multiplayer_name(name)
						result_player2 = play.user_game()

				if result_player1 == "giveup" and result_player1 == result_player2:
					multi_instance.updatescores_type2("both_lose")

				elif result_player1 == "giveup":
					multi_instance.updatescores_type2("player2")

				elif result_player2 == "giveup":
					multi_instance.updatescores_type2("player1")
				
				elif result_player1 == result_player2:
					multi_instance.updatescores_type2("both_won")

				elif result_player1 > result_player2:  # since we need to check for player who took minimum tries to guesss the code
					multi_instance.updatescores_type2("player2")

				elif result_player1 < result_player2:  # since we need to check for player who took minimum tries to guesss the code
					multi_instance.updatescores_type2("player1")

				multi_instance.displayscores()

				if ((input("\nDo you want to play again? (Press y for yes), else enter any key... ")).lower()) != 'y':
					return

