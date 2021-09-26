from common.multiplayer import MultiPlayer
from common.gameresults import GameResults

class TicTacToe():

	possible_choices = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
	marks = ['O','X']
	
	def __init__(self):
		self.board = [[' ',   ' ',   ' '],
					  [' ',   ' ',   ' '],
					  [' ',   ' ',   ' ']]
		self.choices_made = []

	def update_multiplayer_names(self, name1, name2):
		self.name1 = name1
		self.name2 = name2

	def update_difficulty(self):
		pass

	def user_game(self):
		self.print_board()
		print("You can choose to place your mark by typing in the coordinates of that spot, for example, for the spot at first column in the first row, type in 00.")
		print("Similarly it will be 11 for spot at second row second column, etc. Choose wisely, have fun!\n")
		while True:
			while True:
				choice1 = input("{} please select where you want to mark (O): ".format(self.name1))
				if choice1.isnumeric():
					choice1 = self.convert_choice_to_tuple(choice1)
				print("choice: ", choice1)
				if choice1 in self.possible_choices and choice1 not in self.choices_made:
					self.choices_made.append(choice1)
					self.board[int(choice1[0])][int(choice1[1])] = 'O'
					self.print_board()
					break
				else:
					if choice1 not in self.possible_choices:
						print("Invalid choice!")
					elif choice1 in self.choices_made:
						print("Already chosen!")

			result_mark = self.if_game_won()
			if result_mark is not None:
				if result_mark == 'O':
					print('{} won! Woohoo!!'.format(self.name1))
					return "player1"
				else:
					print('{} won! Woohoo!!'.format(self.name2))
					return "player2"

			while True:
				choice2 = input("{} please select where you want to mark (X): ".format(self.name1))
				if choice2.isnumeric():
					choice2 = self.convert_choice_to_tuple(choice2)
				print("choice: ", choice2)
				if choice2 in self.possible_choices and choice2 not in self.choices_made:
					self.choices_made.append(choice2)
					self.board[int(choice2[0])][int(choice2[1])] = 'X'
					self.print_board()
					break
				else:
					if choice2 not in self.possible_choices:
						print("Invalid choice!")
					elif choice2 in self.choices_made:
						print("Already chosen!")

			result_mark = self.if_game_won()
			if result_mark is not None:
				if result_mark == 'O':
					print('{} won! Woohoo!!'.format(self.name1))
					return "player1"
				else:
					print('{} won! Woohoo!!'.format(self.name2))
					return "player2"

	def convert_choice_to_tuple(self, choice):
		choice = list(choice)
		for i in range(len(choice)):
			choice[i] = int(choice[i])
		choice = tuple(choice)
		return choice

	def if_game_won(self):
		# below covers all horizontal cases
		for i in [0,1,2]:
			if len(set(self.board[i])) == 1 and (set(self.board[i]) == {'X'} or set(self.board[i]) == {'O'}):
				return self.board[i][0]

		# below covers all vertical cases
		if self.board[0][0] == self.board[1][0] and self.board[1][0] == self.board[2][0] and (self.board[2][0] == 'X' or self.board[2][0] == 'O'):
			return self.board[0][0]

		if self.board[0][1] == self.board[1][1] and self.board[1][1] == self.board[2][1] and (self.board[2][1] == 'X' or self.board[2][1] == 'O'):
			return self.board[0][1]

		if self.board[0][2] == self.board[1][2] and self.board[1][2] == self.board[2][2] and (self.board[2][2] == 'X' or self.board[2][2] == 'O'):
			return self.board[0][2]

		# below covers both diagonal cases
		if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and (self.board[2][2] == 'X' or self.board[2][2] == 'O'):
			return self.board[0][0]

		if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and (self.board[2][0] == 'X' or self.board[2][0] == 'O'):
			return self.board[0][2]

	def print_board(self): # to print neatly
		blank = [' ']
		print('     0      1      2\n')
		count = 0
		for lis in self.board:
			print(count, end = '   ')
			count += 1
			for i in range(0,len(lis)):
				if lis[i] == ' ':	
					let = str(blank)
					print(let[1:len(let)-1], end = '    ')
				else:
					let = str([lis[i]])
					print(let[1:len(let)-1], end = '    ')
			print("\n")

class BaseTicTacToe(GameResults):
	def __init__(self, usertype, gametype, username=''):
		self.usertype = usertype
		self.gametype = gametype
		self.username = username

	def handle(self):
		if self.gametype == "single":
			raise Exception("TicTacToe is not a singleplayer game!")

		elif self.gametype == "multi":
			multi_instance = MultiPlayer()
			name1 = multi_instance.player1_name()
			name2 = multi_instance.player2_name()

			while True:
				play = TicTacToe()
				play.update_multiplayer_names(name1, name2)
				player_won = play.user_game()
				multi_instance.updatescores_type2(player_won)
				multi_instance.displayscores()

				if ((input("\nDo you want to play again? (Press y for yes), else enter any key... ")).lower()) != 'y':
					return

