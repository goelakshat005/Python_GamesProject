import random
import getpass

from common.difficulty import Difficulty
from common.multiplayer import MultiPlayer
from common.gameresults import GameResults

class JumbledWords(Difficulty):

	words = { "easy": ["water", "soil", "ladder", "learn", "little", "above", "lamp", "juice", "ocean", "queen", "king", "woman", "world", "good", "week", "hybrid"],
			  "medium": ["central", "mediate", "meditate", "context", "sensitive", "extreme", "minimal", "aquatic", "bizarre", "adjacent", "aggregate", "analogy", "beautiful", "gorgeous", "memories"],
			  "hard": ["mathematician", "awesomeness", "eagerness", "gratitude", "arbitrary", "apprehension", "aspiration", "capability", "cognitive", "controversy", "eloquent", "environment", "extravagant", "hereditary", "illegitimate"]}

	num_of_chances = {"easy": 6, "medium":4, "hard":3}

	def __init__(self, gametype):
		self.gametype = gametype
		self.turns = 0
		self.difficulty_level = ''
		self.name = ''
		self.name1 = ''
		self.name2 = ''

	def get_word(self, multi_type=""):
		if multi_type == "2":
			while True:
				self.word = getpass.getpass("Please enter word for {} to guess (word should be greater than 3 letters if difficulty chosen is easy, greater than 5 for medium, greater than 7 for hard): ".format(self.name))  # mask the i/p
				if self.word.isspace() == False:
					if self.difficulty_level == "easy" and len(self.word) > 3:
						break
					elif self.difficulty_level == "medium" and len(self.word) > 5:
						break
					elif self.difficulty_level == "hard" and len(self.word) > 7:
						break
					else:
						print("Please give word according to the difficulty!")
						continue
				print("Please enter a valid word!")

			random_word = random.sample(self.word, len(self.word))
			self.jumbled_word = ''.join(random_word)
		
		else:
			self.word = random.choice(self.words[self.difficulty_level])
			random_word = random.sample(self.word, len(self.word))
			self.jumbled_word = ''.join(random_word)	

	def update_multiplayer_name(self, name):
		self.name = name

	def update_multiplayer_names(self, name1, name2):
		self.name1 = name1
		self.name2 = name2

	def update_difficulty(self, difficultyifplayer2=''):
		if difficultyifplayer2 != '':
			self.difficulty_level = difficultyifplayer2
		else:
			print("You get 6 chances in easy mode, 4 chances in medium mode, and 3 chances in hard mode so choose wisely! Also, the word you will have to guess in each mode will be more difficult than the previous. All the best!\n")
			self.difficulty_level = super().getdifficultylevel()
		
		return self.difficulty_level

	def calculate_turns(self):
		self.turns = self.num_of_chances[self.difficulty_level]

	def user_game(self, multi_type=''):
		print("\nThe jumbled up word is {}, number of guesses you have are: {}.".format(self.jumbled_word, self.turns))
		if multi_type == "1":
			result = self.only_multi1_play()   # for multiplayers playing simultaneously
			return result

		else:
			result = self.single_and_multi2_play()  # for single player and multiplayer giving each other words
			return result


	def only_multi1_play(self):
		already_guessed = []
		count = self.turns
		print("On your first attempt you both will get a chance! Your input will be masked for the first attempt.")
		while self.turns > 0:
			if count == self.turns:
				while True:
					print("What word is on your mind {}?".format(self.name1))
					input_word1 = getpass.getpass("Word: ").lower()
					if input_word1.isspace() == False and input_word1 not in already_guessed:
						break
					else:
						print("Enter a valid response! It should not be blank and should not be already guessed.")

				while True:
					print("What word is on your mind {}?".format(self.name2))
					input_word2 = getpass.getpass("Word: ").lower()
					if input_word2.isspace() == False and input_word2 not in already_guessed:
						break
					else:
						print("Enter a valid response! It should not be blank and should not be already guessed.")
				
				print("{} entered {}".format(self.name1, input_word1))
				print("{} entered {}".format(self.name2, input_word2))
				already_guessed.append(input_word1)
				already_guessed.append(input_word2)

				if self.word == input_word1 and self.word == input_word2:
					print("You both won!")
					print("The word was:", self.word)
					return "both_won"
				elif self.word == input_word1:
					print("{} won!".format(self.name1))
					print("The word was:", self.word)
					return "player1"
				elif self.word == input_word2:
					print("{} won!".format(self.name2))
					print("The word was:", self.word)
					return "player2"
				else:
					print("You both guessed it wrong!")
				self.turns -= 1

			else:
				while True:
					print("What word is on your mind {}?".format(self.name1))
					input_word1 = input().lower()
					if input_word1.isspace() == False and input_word1 not in already_guessed:
						already_guessed.append(input_word1)
						if input_word1 == self.word:
							print("{} won!".format(Self.name1))
							print("The word was:", self.word)
							return "player1"
						else:
							print("Wrong word entered!")
							break
					else:
						print("Enter a valid response! It should not be blank and should not be already guessed.")
				
				while True:
					print("What word is on your mind {}?".format(self.name2))
					input_word2 = input().lower()
					if input_word2.isspace() == False and input_word2 not in already_guessed:
						already_guessed.append(input_word2)
						if input_word2 == self.word:
							print("{} won!".format(Self.name2))
							print("The word was:", self.word)
							return "player2"
						else:
							print("Wrong word entered!")
							break
					else:
						print("Enter a valid response! It should not be blank and should not be already guessed.")

				self.turns -=1

		print("You both lost, better luck next time!")
		print("The word was:", self.word)
		return "both_lost"

	def single_and_multi2_play(self):
		already_guessed = []
		while self.turns > 0:
			while True:
				print("What word is on your mind {}?".format(self.name))
				input_word = input().lower()
				if input_word.isspace() == False and input_word not in already_guessed:
					already_guessed.append(input_word)
					if input_word == self.word:
						print("You won!")
						print("The word was:", self.word)
						return "won"
					else:
						print("Wrong word entered!")
						break
				else:
					print("Enter a valid response! It should not be blank and should not be already guessed.")

			self.turns -=1

		print("You lost! Better luck next time!")
		print("The word was:", self.word)
		return "lost"
					
class BaseJumbledWords(GameResults):
	def __init__(self, usertype, gametype, username=''):
		self.usertype = usertype
		self.gametype = gametype
		self.username = username

	def handle(self):
		if self.gametype == "single":
			while True:
				play = JumbledWords(self.gametype)
				difficulty_level = play.update_difficulty()
				play.get_word()
				play.calculate_turns()
				result = play.user_game()

				if self.usertype != 'guest':
					super().base_results(self.username, "JumbledWords", difficulty_level, result, True)
					super().display_games_scores_with_win_lose(self.username, "JumbledWords")

				if ((input("\nDo you want to play again? (Press y for yes), else enter any key... ")).lower()) != 'y':
					return

		elif self.gametype == "multi":
			print("1. Do you want computer to give a jumbled word and both the players trying to sort simultaneously and first one to do so wins?\n2. Do you want to give each other word (you can write proper word and computer will jumble it up for you) and play seperately?")
			while True:
				option = input()
				if option in ["1", "2"]:
					break
				else:
					print("Please choose from the given options only!")

			if option == "1":
				multi_instance = MultiPlayer()
				name1 = multi_instance.player1_name()
				name2 = multi_instance.player2_name()

				while True:			
					play = JumbledWords(self.gametype)
					play.update_multiplayer_names(name1, name2)
					difficulty_level = play.update_difficulty()
					play.get_word("1")
					play.calculate_turns()
					player_won = play.user_game("1")
					multi_instance.updatescores_type2(player_won)
					multi_instance.displayscores()

					if ((input("\nDo you want to play again? (Press y for yes), else enter any key... ")).lower()) != 'y':
						return

			elif option == "2":
				multi_instance = MultiPlayer()
				while True:	
					players = ['player1', 'player2']
					for player in players:
						if player == "player1":
							name = multi_instance.player1_name()
							print("{} playing first.".format(name))
							play = JumbledWords(self.gametype)
							play.update_multiplayer_name(name)
							difficulty_level = play.update_difficulty()
							play.get_word("2")
							play.calculate_turns()

						else:
							name = multi_instance.player2_name()
							print("{} playing now.".format(name))	
							play = JumbledWords(self.gametype)							
							play.update_multiplayer_name(name)
							difficulty_level = play.update_difficulty(difficulty_level)  # since we want player2 to have the same difficulty as player1
							play.get_word("2")
							play.calculate_turns()

						result = play.user_game("2")
						multi_instance.updatescores_type1(player, result)

					multi_instance.displayscores()

					if ((input("\nDo you want to play again? (Press y for yes), else enter any key... ")).lower()) != 'y':
						return