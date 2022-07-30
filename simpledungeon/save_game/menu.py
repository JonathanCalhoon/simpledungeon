from code import terminal, util, screen
from getkey import getkey
from classes import player
from save_game import save
import time


screen = screen.Screen()


with open("save_game/menu.txt", "r") as file:
	data = file.read()

mymenu = data.split("\n")


def show_menu():
	"""Display The Menu"""
	while True:
		terminal.clear()

		screen.display_out(mymenu)

		choice = getkey()

		if choice == '1':
			return True

		elif choice == '2':
			return False

		elif choice == '3':
			return tutorial()

		elif choice == '4':
			exit()


def show_example():
	"""Display the Limited Menu"""
	terminal.clear()
	print(menu_text+limited_options)

	choice = util.get_input("-> ", valid=['1', '2', '3'])

	if choice == '1':
		return
	elif choice == '2':
		return tutorial(bob="bill")
	elif choice == '3':
		exit()



def tutorial(bob="bob"):
	"""Display Tutorial and call Menu Again"""

	with open('tutorial.txt', 'r') as file:
		parts = file.read().split('PART')

	for part in parts:
		terminal.clear()
		string = screen.build_out_string(part)
		for line in string.split("\n"):
			print(line)
			time.sleep(.05)
		util.cont()

	if bob == 'bob':
		# as all things should be
		return show_menu()

	elif bob == 'bill':
		# herm...
		return limited_menu()