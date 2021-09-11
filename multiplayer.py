class MultiPlayer():
	gametypes = {"1": "single", "2": "multi"}

	def __init__(self):
		while True:
			player1 = input("Please enter name for first player: ")
			if player1.isspace() == False:
				self.player1 = player1
				break
			print("Enter a valid name please!")

		while True:
			player2 = input("Please enter name for second player: ")
			if player2.isspace() == False and self.player1 != player2:
				self.player2 = player2
				break
			print("Enter a valid name please or a different name from player 1!")

		self.player1score_won = 0
		self.player1score_lost = 0
		self.player2score_won = 0
		self.player2score_lost = 0

	def player1_name(self):
		return self.player1

	def player2_name(self):
		return self.player2
		

	def checkgametype(self):                           # check if 2 player game or single player 
		print("Do you want to play:\n1. Single Player\n2. Multi Player\n3. Back")
		while True:
			gametype = input()
			if gametype in self.gametypes:
				return self.gametypes[gametype]
			elif gametype == "3":
				return
			print("Please enter a valid option!\n")

	def updatescores_type1(self, player, result):
		if player == "player1":
			if result == "won":
				self.player1score_won += 1
			else:
				self.player1score_lost += 1
		else:			
			if result == "won":
				self.player2score_won += 1
			else:
				self.player2score_lost += 1

	def updatescores_type2(self, player):
		if player == "player1":
			self.player1score_won += 1
			self.player2score_lost += 1
		else:			
			self.player2score_won += 1
			self.player1score_lost += 1

	def displayscores(self):
		print("The scores are:\n1. {}'s score: Won - {}, Lost - {}\n2. {}'s score: Won - {}, Lost - {}".
			format(self.player1, self.player1score_won, self.player1score_lost, self.player2, self.player2score_won, self.player2score_lost))
