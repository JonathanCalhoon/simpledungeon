from code import terminal, map, randomness, util, read, screen
from battle import battle
from getkey import getkey, keys
import random, time, sys
from classes import weapon, armor
from generators import monsters, dungeon
from save_game import save, save_util

class Game():
	def __init__(self, settings, dungeon, player, posx=False, posy=False, filename=None):
		"""Initiate the Game"""

		self.screen = screen.Screen()

		self.settings = settings
		
		self.dungeon = dungeon

		self.player = player

		self.filename = filename

		if not posx and not posy:
			self.y, self.x = map.getSpawn(dungeon)
		else:
			self.y = posy
			self.x = posx


	def gen_dungeon(self):
		"""Generate a dungeon and move to it"""

		self.dungeon = dungeon.build_dungeon(self.player)
				
		self.y, self.x = map.getSpawn(self.dungeon)

		self.in_dungeon = True

		map.animate_entry(self.dungeon, self.x, self.y, self.settings, [self.player.get_stats()])

	def play(self):
		"""The main Game Loop"""
		play_count = 0

		map.animate_entry(self.dungeon, self.x, self.y, self.settings, [self.player.get_stats()])
		
		while True:
			# disabled count clear for now. Manual clear is still enabled
			play_count += 1
			if play_count == 20:
				#terminal.clear() # just to keep things from being messy
				play_count = 0
				save.save_player_data(self.player, self.x, self.y, self.filename)
				save.save_map_data(self.filename, self.player.dungeon_level, self.dungeon)

			stats = [self.player.get_stats()]
			
			map.display(self.settings, self.dungeon, self.x, self.y, stats)

			self.dungeon[self.y][self.x] = ' '

			key = getkey()

			x = self.x
			y = self.y
			
			if key == 'w' or key == keys.UP:
				y -= 1

			elif key == 's' or key == keys.DOWN:
				y += 1

			elif key == 'd' or key == keys.RIGHT:
				x += 1

			elif key == 'a' or key == keys.LEFT:
				x -= 1

			elif key == 't':
				self.player.xp += 1
				self.player.level_up()

			elif key == '1':
				self.player_stats()
			elif key == '2':
				self.player.shuffle_loadout()
			elif key == '3':
				self.player.eat()
			elif key == '4':
				save.save_player_data(self.player, self.x, self.y, self.filename)
				save.save_map_data(self.filename, self.player.dungeon_level, self.dungeon)
			elif key == '5':
				terminal.clear()
			elif key == '0':
				choice = self.screen.ask_question(self.player, "Are you sure you want to exit?", prompts=["Yes", "No"])
				if choice == 'yes':
					print("Saving...")
					save.save_player_data(self.player, self.x, self.y, self.filename)
					save.save_map_data(self.filename, self.player.dungeon_level, self.dungeon)
					exit()
				elif choice == 'no':
					terminal.clear()

			action = map.action(self.dungeon, x, y)

			if action.valid:
				self.y = y
				self.x = x

			if action.portal:
				self.gen_dungeon()

			if action.treasure:
				self.open_treasure()
			
			if action.shard:
				self.collect_shard()

			if action.enemy:
				enemies = monsters.get_monster(action.enemy)
				if enemies[0].name == "skeleton" and self.player.character == "skeleton":
					self.screen.display_card(self.player, ["Your fellow Skelly waves hello"])
					util.cnt()
				else:
					battle.fight(self.player, enemies)

			if action.special:

				if action.special == "⚔":
					terminal.clear()
					i = self.screen.ask_question(self.player, "You found a strangely familar sword", ["Keep", "Throw away"])
					if i == 'keep':
						w = weapon.Weapon("Rusty Longsword", 15, 15, 20, 10, 10, 1000)
						self.player.store_weapon(w)
					else:
						self.screen.display_card(self.player, "You threw away the rusty old sword.")
						util.cnt()

				elif action.special == "⍬":
					terminal.clear()
					i = self.screen.ask_question(self.player, "You found a strange glowing orb...", ["Keep", "Throw away"])
					if i == 'keep':
						w = weapon.Weapon("The Eye of GįjvœD", 30, 10, 10, 10, 10, 1000)
						self.player.store_weapon(w)
					else:
						self.screen.display_card(self.player, "You dropped the strange glowing orb")
						util.cnt()

				elif action.special == "⇟":
					terminal.clear()
					i = self.screen.ask_question(self.player, "You found an ancient weapon... a strange black tube", ["Keep", "Throw away"])
					if i == "keep":
						w = weapon.Weapon("Shoulder Cannon", 100, 1, 30, 10, 10, 1000)
						self.player.store_weapon(w)
					else:
						self.screen.display_card(self.plyaer, "You threw away the rusty black tube")
						util.cnt()

				elif action.special == "⌑":
					terminal.clear()
					i = self.screen.ask_question(self.player, "In the hands of a dusty old skelly lies a weapon", ["Take it", "Ignore it"])
					if i == "take it":
						w = weapon.Weapon("Ghoul's Voulge", 15, 40, 4, 10, 10, 1000)
						self.player.store_weapon(w)
					else:
						self.screen.display_card(self.player, "You ingored the weapon")
						util.cnt()

				elif action.special == "✹":
					terminal.clear()
					i = self.screen.ask_question(self.player, "You found a spiky ball.", ["Take it", "Leave it"])
					if i == 'take it':
						w = weapon.Weapon("Spiked Ball", 30, 2, 30, 10, 10, 1000)
						self.player.store_weapon(w)
					else:
						self.screen.display_card(self.player, "You left the spiky ball.")
						util.cnt()


			if action.character:
				for character in self.characters:
					if character.symbol == action.character:
						character.touch_action(self.player)

	def player_stats(self):
		"""Show the user inventory, armor, etc"""


		char = randomness.get_char(self.player)

		terminal.clear()

		card = ["", "", ""]

		
		char[2] += f"  SHARDS: {str(self.player.shards)}"
		char[4] += f"  LEVEL: {str(self.player.level)}"
		char[5] += f"  XP: {str(self.player.xp)}/{str(self.player.max_xp)}"

		for c in char:
			card.append(c)

		card.append("")

		card.append(self.player.weapon.stats())
		card.append(self.player.armor.stats())

		"""
		for item in sorted(self.player.inventory):
			exist = False
			for i in items:
				if item == i[0]:
					i[1] += 1
					exist = True
			if not exist:
				items.append([item, 1])

		for item in items:
			util.indent(f"{item[0]} x{str(item[1])}", 26)
		"""
		
		self.screen.display_card(self.player, card)

		util.cnt()

	def open_treasure(self):
		"""Gens Random Box and opens it"""

		terminal.clear()

		loot = random.choice(randomness.loot)

		if loot['type'] == 'weapon':
			w = weapon.generate_weapon(self.player.character)
			choice = self.screen.ask_question(self.player, "You found a tier " + str(w.tier) + " " + str(w.name), ["Equip", "Keep", "Throw away"])

			if choice == 'equip':
				self.player.equip_weapon(w)
				self.player.store_weapon(w)

			elif choice == 'keep':
				self.player.store_weapon(w)

			else:
				self.screen.display_card(self.player, ["You threw away the " + w.name])
				util.cnt()

		elif loot['type'] == 'armor':
			a = armor.generate_armor(self.player.character)
			choice = self.screen.ask_question(self.player, "You found a tier " + str(a.tier) + " " + str(a.name), ["Equip", "Keep", "Throw away"])

			if choice == 'equip':
				self.player.equip_armor(a)
				self.player.store_armor(a)

			elif choice == 'keep':
				self.player.store_armor(a)

			else:
				self.screen.display_card(self.player, ["You threw away the " + a.name])
				util.cnt()

		elif loot['type'] == 'inventory':
			self.screen.display_card(self.player, ["You found a " + loot['name']])
			util.cnt()
			self.player.inventory.append(loot['name'])

		elif loot['type'] == 'food':
			self.screen.display_card(self.player, ["You found a " + loot['name']])
			util.cnt()
			self.player.food.append(loot['name'])

		elif loot['type'] == 'gold':
			amount = random.randint(1, loot['max'])
			self.screen.display_card(self.player, ["You found " + str(amount) + " gold"])
			util.cnt()
			self.player.gold += amount

	
	def collect_shard(self):
		self.screen.display_card(self.player, ["You found a shard... A small glowing blue stone"])
		util.cnt()
		
		self.player.shards += 1
		self.player.max_life += 10
		self.player.life += 10
		self.player.max_magic += 5
		self.player.magic += 5
	