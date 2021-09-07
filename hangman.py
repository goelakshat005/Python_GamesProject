import random

class Hangman():
	avail_letters = 'abcdefghijklmnopqrstuvwxyz'
	random_names = {'fruit': ['lemon', 'mango', 'apple', 'carrot', 'peach', 'grapes', 'orange'], 
					'country': ['china', 'turkey', 'india', 'nepal', 'britian', 'bhutan', 'cuba', 'mexico', 'spain', 'russia', 'france', 'south korea'],
					'furniture': ['table', 'chair', 'stool', 'sofa', 'almirah', 'door', 'grill', 'panel']}   # can also create csv file for the same and then import here

	turns_diff = {'easy': 5, 'medium': 3, 'hard' : 2}

	def __init__(self, usertype, gametype, difficulty_level, name=''):
		self.gametype = gametype

		if self.gametype == "multi":
			while True:
				self.random_name = input("Please enter word for {} to guess (word should be greater than or equal to 3 letters, don't include spaces for your own sake, lol): ".format(name))
				if self.random_name.isspace() == False and len(self.random_name) >= 3:
					break
				print("Please enter a valid word!")

			while True:
				self.random_key = input("Please enter a hint for {}: ".format(name))
				if self.random_key.isspace() == False:
					break
				print("Please enter a valid hint!")

		elif gametype == "single":
			self.random_key = random.choice(list(self.random_names.keys()))
			self.random_name = random.choice(self.random_names[self.random_key])
			self.random_name = " ".join((self.random_name).split())

		self.difficulty_level = difficulty_level		

		self.guessed_letters = ''
		self.name_while_guess = []
		turns = 0
		words = self.random_name.split(" ")
		for word in words:
			turns += len(word)
			dashes = "_"*len(word)
			dashes_list = list(dashes)
			self.name_while_guess += dashes_list
			self.name_while_guess.append(" ")
		self.name_while_guess.pop()

		self.turns = self.turns_diff[self.difficulty_level] + turns

	def return_if_guessing_possible(self, letter_guessed):
		if letter_guessed in self.avail_letters and len(letter_guessed) == 1:
			if letter_guessed not in self.guessed_letters:
				self.guessed_letters += letter_guessed
				return 'possible guess'
			return 'already guessed'
		return 'illegal guess'

	def word_after_guessing(self, letter_guessed):
		if letter_guessed in self.random_name:
			count = 0
			for pos in self.random_name:
				if pos == letter_guessed:
					self.name_while_guess[count] = letter_guessed 		
				count += 1
			return True
		return False

	def display_to_user(self):
		print("\nThe word is of {} letters, number of guesses you have are: {}. [Hint: {}]".
			format(self.turns-self.turns_diff[self.difficulty_level], self.turns, self.random_key))
		print(' '.join(self.name_while_guess))

		while self.turns > 0:
			
			flag = 0

			while flag == 0:
			
				input_letter = (str(input("Please enter the letter you want to guess: "))).lower()
				option = self.return_if_guessing_possible(input_letter)
			
				if option == 'illegal guess':
					print("The letter you entered is illegal, guess again.")
			
				elif option == 'already guessed':
					print("The letter you entered is already entered, guess again.")
			
				else:
					present = self.word_after_guessing(input_letter)
			
					if present:
						print("You entered the right choice!")
			
						if "_" not in self.name_while_guess:
							print("The word is: ", self.random_name)
							print("\nCONGRATULATIONS, YOU WON! WOOHOO!")
							return 'won', self.difficulty_level
					else:
						self.turns -= 1
						print("Wrong choice!")
			
					print("Word left is: ", ' '.join(self.name_while_guess))
					flag = 1

			print("\nNumber of guesses left: {}".format(self.turns))

		print("You lost, better luck next time!")
		print("The word was: ", self.random_name)
		return 'lost', self.difficulty_level

	def __str__(self):
		print("Hangman Game!")


if __name__ == '__main__':
	user = Hangman()
	# user.display_to_user()


# to add later - 
# hangman name with space in between, show properly to user and process accordingly (eg. south korea)
# login user maintaining prev scores and all (parent class)  -- done
# play again option.  -- done
# add timer  -- done
# difficulty based on choice of user  -- done
# clean code if possbile - if won or not in a seperate function, show to user number of guesses left --done
# setting up postgres- for storing authentications detailsand other things  -- done
# can password be entered in stars while user is typing -- done
# add def __str__ to all classes  -- done
# display user games details, give an option -- done
# check if username requires any case sensitiveness  -- done
# don't decrease turn when choice is right in hangman  -- done
# option for display all results for all games and display only specific game results -- done
# back option  -- done
# take care of case sensitivity when user is making a choice  -- done
# exit option only on start page very first page   -- done
# multiplayer game or single player (multiplayer - other person gives the words and hint, keep track of both players scores -- done

# in multiplayer the word given by player should be in stars
# what to do if user guesses the whole name at once in hangman
# difficulty level? - based on past of the user maybe -- later 
# add more categories, (import from csv with multiple categories?), add this feature to multiplayer as well  -- later
# add another hint but it costs you one chance, hints can store in csv  -- later
# the password is stored in stars in db and should contain letters and special characters
# get mail id as i/p as well
# update passwprd option if forgot, update modified on accordingly
# can send otp through mail when forgot option
# send mail when log in
# change random function in hangman to make truly random
# can create a constants file if useful
# write test cases if possible

# rock papers scissors
# tic tac toe  # only 2 players