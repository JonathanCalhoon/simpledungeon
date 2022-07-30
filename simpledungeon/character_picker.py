from code import terminal, screen
from getkey import getkey, keys


screen = screen.Screen()

def pick_character():
	"""Return the character the user has picked"""

	with open("characters.txt", "r") as file:
		characters = file.read().split("FRAME")


	charries = ['knight', 'archer', 'wizard', 'human', 'skeleton']


	index = 0
	max_index = len(characters)-1

	while True:
		terminal.clear()
		print(screen.build_out_string(characters[index]))

		key = getkey()

		if key == keys.RIGHT or key  == 'd':
			if index != max_index:
				index += 1

		elif key == keys.LEFT or key == 'a':
			if index != 0:
				index -= 1

		elif key == '\n':
			return charries[index]


