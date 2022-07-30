from generators import dungeon
from code import game, map, terminal, util
from classes import player
from save_game import menu, save, save_util
from settings import settings
import random




###################
#  INIT SETTINGS  #
###################

settings = settings.Settings()

# delete all saves

#save.delete_all_saves()


class LoginManager():
	def __init__(self, save=False):
		"""Initate the Login Manager"""

		self.save = save

	def example():
		"""Example Menu (no save)"""

		return menu.show_example()
		

	def login(self):
		"""Handle User Login and Player/Map Restore"""

		if self.save:
			return self.example()


		if menu.show_menu():
			terminal.clear()
			saves = save.get_saves()

			print("SELECT SAVE: ")

			valids = []
			
			for i in saves:
				index = str(saves.index(i))
				print(f"[{index}] {i['name']} | {i['date']}")
				valids.append(index)

			i = int(util.get_input("-> ", valids))

			game_save = saves[i]

			g = save.get_game_data(game_save)

			mygame = game.Game(
				settings,
		        dungeon=save_util.map_from_file('generators/basic_map.txt'),
		        player = g[0],
		        characters=dungeon.characters,
		        posx = 15,
		        posy = 15,
				filename=game_save['val']
			)

			return mygame
			

		else:
			terminal.clear()
			print("Creating New Game")
			print("\n\n")

			name = input("Save Name: ")

			filename = save.add_save(name)

			p = player.Player()

			mygame = game.Game(
				settings,
				dungeon = save_util.map_from_file("generators/basic_map.txt"),
				player=p,
				posy=15,
				posx=15,
				filename=filename
			)

			return mygame
					

			

			



				
				

		