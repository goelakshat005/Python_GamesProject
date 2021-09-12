import time

class Flames():
	flames_word = "FLAMES"
	flames_word_length = len(flames_word)
	flames_meaning_dict = {"F":"Friends", "L":"Lovers", "A":"Affection", "M":"Marriage", "E":"Enemies", "S":"Siblings"}
	
	def __init__(self, usertype, gametype):
		pass

	def update_multiplayer_names(self, name1, name2):
		self.name1 = name1
		self.name2 = name2

	def reset_class_vars(self):
		pass

	def update_difficulty(self):
		pass

	def user_game(self):
		print("name1: {}".format(self.name1))
		print("name2: {}".format(self.name2))
		print("Let's get to know the relationship status with each other!")
		
		name1_lis = list(self.name1)
		name2_lis = list(self.name2)
		length_name1 = len(self.name1)
		length_name2 = len(self.name2)
		
		for letter in name1_lis:
			if letter in name2_lis:
				length_name1 -= 1
				length_name2 -= 1
				name2_lis.pop(name2_lis.index(letter))

		total_names_len = length_name2 + length_name1
		length_left =  total_names_len % self.flames_word_length
		print("Calculating your relationship status, hold on!\n")
		time.sleep(1)
		print("The relationship status for you guys is: {}".format(self.flames_meaning_dict[self.flames_word[length_left-1]]))

