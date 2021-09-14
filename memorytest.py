import random
import getpass
import time
import os
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from multiplayer import MultiPlayer
from gameresults import GameResults

class MemoryTest():
	words = { "easy": ["water", "soil", "ladder", "learn", "little", "above", "lamp", "juice", "ocean", "queen", "king", "woman", "world", "good", "week", "hybrid"],
			  "medium": ["central", "mediate", "meditate", "context", "sensitive", "extreme", "minimal", "aquatic", "bizarre", "adjacent", "aggregate", "analogy", "beautiful", "gorgeous", "memories"],
			  "hard": ["mathematician", "awesomeness", "eagerness", "gratitude", "arbitrary", "apprehension", "aspiration", "capability", "cognitive", "controversy", "eloquent", "environment", "extravagant", "hereditary", "illegitimate"]}

	def __init__(self, gametype):
		self.gametype = gametype
		self.name1 = ''
		self.name2 = ''
		self.difficulty_level = ''

	def update_multiplayer_names(self, name1, name2):
		self.name1 = name1
		self.name2 = name2

	def update_difficulty(self, difficulty_level):
		self.difficulty_level = difficulty_level

	def user_game(self):

		if self.gametype == "single":
			print("The difficulty of word will increase gradually! After display of each word you will get 2 seconds to memorize it before the screen goes blank and you have to write all the "\
				"words. Please be alert!")
			print("GET READY!")
			time.sleep(10)
			result = self.singleplayer_game()
			return result

		elif self.gametype == "multi":
			print("The players will be shown words on screen which they have to then write simultaneously. The difficulty of word will increase gradually! After display of each word you "\
				  "will get 2 seconds to memorize it before the screen goes blank and you have to write all the words. Please be alert!")
			print("GET READY!")
			time.sleep(10)
			result = self.multiplayer_game()
			return result

	def singleplayer_game(self):
		words_lis = []
		count = 0

		self.update_difficulty("easy")

		while True:
			if count == 4:
				self.update_difficulty("medium")
			elif count == 8:
				self.update_difficulty("hard")

			while True:
				word = random.choice(self.words[self.difficulty_level])
				if word in words_lis:
					continue
				else:
					break
			print("\n")
			print(word)
			time.sleep(2)
			os.system('cls' if os.name == 'nt' else "printf '\033c'")
			words_lis.append(word)
			print("Write all words shown from very starting in order, after writing each word please press enter.")
			for word in words_lis:
				if word != input("ENTER WORD: ").lower():
					print("You messed up a bit, your final score is:", count)
					return count
			
			count += 1
			print("Your score up till now is:", count)

	def multiplayer_game(self):
		words_lis = []
		count = 0

		self.update_difficulty("easy")

		while True:
			if count == 4:
				self.update_difficulty("medium")
			elif count == 8:
				self.update_difficulty("hard")

			while True:
				word = random.choice(self.words[self.difficulty_level])
				if word in words_lis:
					continue
				else:
					break
			print("\n")
			print(word)
			time.sleep(2)
			os.system('cls' if os.name == 'nt' else "printf '\033c'")
			words_lis.append(word)
			print("Write all words shown from very starting in order, after writing each word please press enter.")
			
			print("{} your turn to write.".format(self.name1))
			flag1 = 0
			for word in words_lis:
				if word != getpass.getpass("ENTER WORD: ").lower():
					flag1 = 1
					print("{}, for you game is over if {} is able to write correctly he/she will win, otherwise both will lose. Your score is {}!".format(self.name1, self.name2, count))

			flag2 = 0
			print("\n{} your turn to write.".format(self.name2))
			for word in words_lis:
				if word != getpass.getpass("ENTER WORD: ").lower():
					flag2 = 1
					print("{}, game is over. Your score is {}!".format(self.name2, count))
					
			count += 1
			if flag1==1 and flag2==1:
				print("You both lose as no one is a clear winner. You both stopped at score: {}".format(count-1))
				return "both_lose"
			elif flag1==0 and flag2==1:
				print("{} won, your score is: {}!".format(self.name1, count))
				return "player1"
			elif flag1==1 and flag2==0:
				print("{} won, your score is: {}!".format(self.name2, count))
				return "player2"
			else:
				print("Your score up till now is:", count)

class BaseMemoryTest(GameResults):
	def __init__(self, usertype, gametype, username=''):
		self.usertype = usertype
		self.gametype = gametype
		self.username = username

	def handle(self):
		print("BE ATTENTIVE! YOU WILL NEED IT!")
		if self.gametype == "single":
			while True:
				play = MemoryTest(self.gametype)
				result = play.user_game()

				if self.usertype != 'guest':
					super().base_results(self.username, "MemoryTest", '', result, False, True)  # blank signifies the difficulty level and False signifies 
					# if we need to save a game with difficulty levels and True signifies that it's a score type game with no win or lose
					super().display_games_with_only_scores(self.username, "MemoryTest")

				if ((input("\nDo you want to play again? (Press y for yes), else enter any key... ")).lower()) != 'y':
					return

		elif self.gametype == "multi":
			multi_instance = MultiPlayer()
			name1 = multi_instance.player1_name()
			name2 = multi_instance.player2_name()
			play = MemoryTest(self.gametype)
			play.update_multiplayer_names(name1, name2)
			
			while True:			
				player_won = play.user_game()
				multi_instance.updatescores_type2(player_won)
				print("\n")
				multi_instance.displayscores()

				if ((input("\nDo you want to play again? (Press y for yes), else enter any key... ")).lower()) != 'y':
					return

