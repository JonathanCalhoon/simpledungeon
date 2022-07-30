import json
from classes import weapon, armor, player
import os
from datetime import date
from save_game import save_util
from generators import dungeon
import glob, shutil





def delete_all_saves():
	"""Deletes all Saves"""

	files = glob.glob('saves/*')
	for f in files:
		if os.path.isfile(f):
			os.system("rm " + f)
		else:
			shutil.rmtree(f)

	with open('saves/saves.txt', 'x') as file:
		pass
	with open('saves/saves.txt', 'w') as file:
		file.write(json.dumps({"saves":[],"count":1}))

	
delete_all_saves() # always call


def get_dungeon(folder, num, player):
	"""Checks if a dungeon exists and returns if it does, else false"""

	# These floors will not exist for now util we create the Enemies related to them

	#if num == 51:
	#	_map = save_util.map_from_file('special_floors/castle.txt')
	#	return _map

	#elif num == 72:
	#	_map = save_util.map_from_file('special_floors/castle.txt')
	#	return _map

	if os.path.isfile(f"saves/save_{str(folder)}/maps/map_{str(num)}.txt"):
		_map = save_util.map_from_file(f"saves/save_{str(folder)}/maps/map_{str(num)}.txt")
		return _map

	else:
		with open(f"saves/save_{str(folder)}/maps/map_{str(num)}.txt", 'x') as file:
			pass

		if num == 113:
			new_dungeon = dungeon.build_dungeon(player, add_rare="🗡") # change this later
		else:
			new_dungeon = dungeon.build_dungeon(player)

		with open(f"saves/save_{str(folder)}/maps/map_{str(num)}.txt", 'w') as file:
			file.write(save_util.map_to_string(new_dungeon))

		return new_dungeon


def get_game_data(save):
	"""Converts 'nested' JSON to 'nested' Game Data and Player Object"""

	with open(save['file'], 'r') as file:
		JSON = json.loads(file.read())

	p = player.Player()
	p.restore(JSON['player'])

	val = save['val']
	game_map = save_util.map_from_file(f"saves/save_{str(val)}/maps/map_{str(p.dungeon_level)}.txt")

	posx = JSON['posx']
	posy = JSON['posy']

	return [p, game_map, posx, posy]




def save_player_data(player, posx, posy, save_num):
	"""Writes Player Data to File"""

	JSON = {
		'player' : save_util.class_to_json(player),
		'posx' : posx,
		'posy' : posy,
	}

	with open(f"saves/save_{str(save_num)}/save.txt", 'w') as file:
		file.write(json.dumps(JSON))


def save_map_data(save_num, level, map):
	"""Save the map to file"""
	with open(f"saves/save_{str(save_num)}/maps/map_{str(level)}.txt", 'w') as file:
		data = save_util.map_to_string(map)
		file.write(data)




def get_saves():
	"""Get the list of saves"""
	with open('saves/saves.txt', 'r') as file:
		data = json.loads(file.read())

	return data['saves']


def add_save(name):
	global save
	"""Add a save to the list of saves"""

	with open('saves/saves.txt', 'r') as file:
		data = json.loads(file.read())

	val = data['count']

	os.mkdir('saves/save_'+str(val))
	os.mkdir('saves/save_'+str(val)+"/maps")

	filename = 'saves/save_'+str(val)+'/save.txt'

	with open(filename, 'x') as file:
		pass

	with open('saves/save_'+str(val)+"/maps/map_52.txt", 'x') as file:
		pass


	data['count'] += 1

	save = {
		'name' : name,
		'date' : str(date.today()),
		'file' : filename,
		'val' : val
	}

	data['saves'].append(save)

	with open('saves/saves.txt', 'w') as file:
		file.write(json.dumps(data))

	return val






					

		

		
		