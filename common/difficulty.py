class Difficulty():
	def __init__(self):
		pass
	
	def getdifficultylevel(self):
		level_ok = False
		levels = {'1':'easy', '2':'medium', '3':'hard'}
		while not level_ok:
			print("Enter the level of difficulty you want: ")
			for key, level in levels.items():
				print("{}. {}".format(key, level))

			difficulty_level = input()
			if difficulty_level in levels:
				print("Difficulty level chosen: ", levels[difficulty_level])
				level_ok = True
			else:
				print("Wrong choice, choose again.\n")

		difficulty_level = levels[difficulty_level]
		return difficulty_level
