import random
import getpass
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from multiplayer import MultiPlayer
from gameresults import GameResults

class RockPaperScissor():
	choices_win_dict = {('paper','rock'):'paper', ('paper','scissor'):'scissor', ('rock','scissor'):'rock'}  # combinations and winner of that combo
	choices = {"1":"rock", "2":"paper", "3":"scissor"}

	def __init__(self, gametype):
		self.gametype = gametype
		self.name1 = ''
		self.name2 = ''

	def update_multiplayer_names(self, name1, name2):
		self.name1 = name1
		self.name2 = name2

	def user_game(self):
		while True:
			turns = input("Please enter the number of turns you would like to play (max 20): ")
			if turns.isnumeric():
				if int(turns) <= 20:
					break
				else:
					print("Please enter a value less than or equal to 20!\n")
					continue

			else:
				print("Wrong value entered, enter a valid number!")

		turns = int(turns)
		for key, val in self.choices.items():
			print("{}. {}".format(key, val))

		if self.gametype == "single":
			result = self.singleplayer_game(turns) 
			if result == "tie":
				print("Let's have the tie breaker!")
				result = self.singleplayer_game(1)
			return result

		elif self.gametype == "multi":
			result = self.multiplayer_game(turns)
			if result == 0:
				print("Let's have the tie breaker!")
				result = self.multiplayer_game(1)
			if result == "player1":
				print("{} won! Woohoo!!".format(self.name1))
			else:
				print("{} won! Woohoo!!".format(self.name2))
			return result

	def singleplayer_game(self, turns):
		player_won = 0
		computer_won = 0
		
		while turns > 0 :
			while True:
				choice = input("Please select option you want to choose: ")
				if choice in ["1","2","3"]:
					user_choice = self.choices[choice]
					num = str(random.randint(1,3))
					comp_choice = self.choices[num]
					print("You chose: {}".format(user_choice))
					print("Computer chose: {}".format(comp_choice))
					if comp_choice == user_choice:   # turns is not decreased until and unless the it's not a tie
						print("It's a tie!")
					else:
						key = self.sort_choices(user_choice, comp_choice)
						win = self.choices_win_dict[key] 
						if win == user_choice:
							player_won += 1
							print("you won!")
						else:
							computer_won += 1
							print("You lost!")
						turns -= 1
					print("\nYour score: {}\nComputer's score: {}\n".format(player_won, computer_won))
					break

				else:
					print("Wrong option, please choose again.")

		if player_won > computer_won:
			return "won"
		elif player_won < computer_won:
			return "lost"
		return "tie"

	def multiplayer_game(self, turns):
		player1_won = 0
		player2_won = 0
		
		while turns > 0 :
			while True:
				choice1 = getpass.getpass("{} please select option you want to choose: ".format(self.name1))
				choice2 = getpass.getpass("{} please select option you want to choose: ".format(self.name2))

				if choice1 in ["1","2","3"] and choice2 in ["1","2","3"]:
					choice1 = self.choices[choice1]
					choice2 = self.choices[choice2]
					print("{} chose: {}".format(self.name1,choice1))
					print("{} chose: {}".format(self.name2,choice2))
					if choice1 == choice2:   # turns is not decreased until and unless the it's not a tie
						print("It's a tie!")
					else:
						key = self.sort_choices(choice1, choice2)
						win = self.choices_win_dict[key]
						if win == choice1:
							player1_won += 1
							print("{} won!".format(self.name1))
						else:
							player2_won += 1
							print("{} won!".format(self.name2))
						turns -= 1
					print("\n{}'s score: {}\n{}'s score: {}\n".format(self.name1, player1_won, self.name2, player2_won))
					break

				else:
					if choice1 not in ["1","2","3"]:
						print("{}'s choice is wrong!".format(self.name1))
					elif choice2 not in ["1","2","3"]:
						print("{}'s choice is wrong!".format(self.name2))

		if player1_won > player2_won:
			return "player1"
		elif player1_won < player2_won:
			return "player2"
		return 0


	def sort_choices(self, user_choice, comp_choice):
		if user_choice[0] < comp_choice[0]:
			return (user_choice, comp_choice)
		else:
			return (comp_choice, user_choice)

class BaseRockPaperScissor(GameResults):
	def __init__(self, usertype, gametype, username=''):
		self.usertype = usertype
		self.gametype = gametype
		self.username = username

	def handle(self):
		if self.gametype == "single":
			while True:
				play = RockPaperScissor(self.gametype)
				result = play.user_game()

				if self.usertype != 'guest':
					super().base_results(self.username, "RockPaperScissor", '', result, False)  # blank signifies the difficulty level and False signifies 
					# if we need to save a game with difficulty levels
					super().display_user_game_details(self.username, "RockPaperScissor")

				if ((input("\nDo you want to play again? (Press y for yes), else enter any key... ")).lower()) != 'y':
					return

		elif self.gametype == "multi":
			multi_instance = MultiPlayer()
			name1 = multi_instance.player1_name()
			name2 = multi_instance.player2_name()
			play = RockPaperScissor(self.gametype)
			play.update_multiplayer_names(name1, name2)
			
			while True:			
				player_won = play.user_game()
				multi_instance.updatescores_type2(player_won)
				multi_instance.displayscores()

				if ((input("\nDo you want to play again? (Press y for yes), else enter any key... ")).lower()) != 'y':
					return

