class MultiPlayer():

	def __init__(self):
		while True:
			print()
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

		self.player1_starting_amount = 0
		self.player2_starting_amount = 0
		self.player1_amount = 0
		self.player2_amount = 0

		self.player_who_owes = ''
		self.amount_owed = 0

	def player1_name(self):
		return self.player1

	def player2_name(self):
		return self.player2

	def get_players_starting_amounts(self, min_budget, max_budget):
		while True:
			amount = input("{}, please enter your budget (enter in whole numbers): ".format(self.player1))
			if amount.isnumeric() == True:
				if int(amount) >= min_budget and int(amount) <= max_budget:
					self.player1_starting_amount = int(amount)
					self.player1_amount = self.player1_starting_amount
					break
				else:
					print("Please enter an amount in range of {} and {}.".format(min_budget, max_budget))
			else:
				print("Please enter a valid number!")
		
		while True:
			amount = input("{}, please enter your budget (enter in whole numbers): ".format(self.player2))
			if amount.isnumeric() == True:
				if int(amount) >= min_budget and int(amount) <= max_budget:
					self.player2_starting_amount = int(amount)
					self.player2_amount = self.player2_starting_amount
					break
				else:
					print("Please enter an amount in range of {} and {}.".format(min_budget, max_budget))
			else:
				print("Please enter a valid number!")

		return self.player1_starting_amount, self.player2_starting_amount

	def update_owed_vars(self):
		if self.player1_amount < self.player1_starting_amount:
			self.player_who_owes = 'player1'
			self.amount_owed = self.player1_starting_amount - self.player1_amount
		elif self.player2_amount < self.player2_starting_amount:
			self.player_who_owes = 'player2'
			self.amount_owed = self.player2_starting_amount - self.player2_amount

	def display_owed_vars(self):
		if self.player_who_owes == "player1":
			print("{} owes {} amount {}$".format(self.player1, self.player2, self.amount_owed))
		elif self.player_who_owes == "player2":
			print("{} owes {} amount {}$".format(self.player2, self.player1, self.amount_owed))
		else:
			print("No one owes anyone any amount!")

	def get_player1_amount(self):
		return self.player1_amount

	def get_player2_amount(self):
		return self.player2_amount	

	def get_player1_starting_amount(self):
		return self.player1_starting_amount

	def get_player2_starting_amount(self):
		return self.player2_starting_amount	

	def update_player1_amount(self, amount):
		self.player1_amount = amount

	def update_player2_amount(self, amount):
		self.player2_amount = amount

	def updatescores_type1(self, player, result):  # one player won doesn't necessarily mean other player lost
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

	def updatescores_type2(self, player):  # in which if one player wins in a game, it is decided that other person lost, so both are simultaneous
		if player == "player1":
			self.player1score_won += 1
			self.player2score_lost += 1
		elif player == "player2":			
			self.player2score_won += 1
			self.player1score_lost += 1
		elif player == "both_won":
			self.player1score_won += 1
			self.player2score_won += 1
		elif player == "both_lost":
			self.player1score_lost += 1
			self.player2score_lost += 1

	def displayscores(self):
		print("The score table is:\n1. {}'s score: Won - {}, Lost - {}\n2. {}'s score: Won - {}, Lost - {}".
			format(self.player1, self.player1score_won, self.player1score_lost, self.player2, self.player2score_won, self.player2score_lost))
