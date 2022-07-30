from classes import armor, weapon
from code import util, terminal, randomness, screen, animation
import random
import character_picker
import time


screen = screen.Screen()


class Player():
	def __init__(self):
		"""Initiate the Player"""

		# game data
		self.global_room_counter = 1

		# Life/Magic
		# EDIT: Stamina has been Removed
		self.life = 100
		self.max_life = 100
		self.magic = 10
		self.max_magic = 10
		self.has_magic = True

		# Level
		self.level = 1
		self.xp = 0
		self.max_xp = 15

		# Weapons/Armor
		self.weapon = weapon.Weapon("Fists", 1, 1, 1, 10, 10, 0);
		self.armor = armor.Armor("Leather Tunic", 1, 3, 3, 10)

		# Inventory/Money
		self.inventory = []
		self.food = []
		self.weapons = [self.weapon]
		self.armors = [self.armor]
		self.loot = []
		self.max_weapons = 3
		self.max_armors = 3
		self.shards = 0
		self.gold = 0

		# Keep track of rooms played
		self.dungeon_level = 1

		# keep track of NPC stats
		self.npc_data = []

		# character
		self.character = character_picker.pick_character()
		self.give_boosts()

	def restore(self, dict):
		"""Restores the player from a dictionary"""


		# game data

		self.global_room_counter = dict['global_room_counter']

		# Life/Magic
		# EDIT: Stamina has been Removed
		self.life = dict['life']
		self.max_life = dict['max_life']
		self.magic = dict['magic']
		self.max_magic = dict['max_magic']
		self.has_magic = dict['has_magic']

		# Level
		self.level = dict['level']
		self.xp = dict['xp']
		self.max_xp = dict['max_xp']

		# Weapons/Armor
		self.weapon = weapon.weapon_from_dict(dict['weapon'])
		self.armor = armor.armor_from_dict(dict['armor'])

		# Inventory/Money
		self.inventory = dict['inventory']
		self.food = dict['food']
		self.max_weapons = dict['max_weapons']
		self.max_armors = dict['max_armors']
		self.weapons = weapon.weapons_from_dict(dict['weapons'])
		self.armors = armor.armors_from_dict(dict['armors'])
		self.loot = dict['loot']
		self.shards = dict['shards']
		self.gold = dict['gold']

		# Keep track of rooms played
		self.rooms_played = dict['rooms_played']

		# Keep track of NPC data
		self.npc_data = dict['npc_data']

		# character
		self.character = dict['character']

	def give_boosts(self):
		"""Boost player according to character stats"""

		if self.character == "knight":
			self.life = 120
			self.max_life = 120
			self.has_magic = False
			self.armor = armor.Armor("Iron Armor", 3, 3, 3, 25)
			self.weapon = weapon.Weapon("Broadsword", 4, 3, 7, 10, 10, 30)

			self.weapons = [self.weapon]
			self.armors = [self.armor]

		elif self.character == 'archer':
			self.life = 75
			self.max_life = 75
			self.has_magic = False
			self.weapon = weapon.Weapon("Long Bow", 10, 5, 4, 10, 10, 42)
			self.weapons = [self.weapon]

		elif self.character == 'wizard':
			self.life = 80
			self.max_life = 80
			self.magic = 30
			self.max_magic = 30
			self.weapon = weapon.Weapon("Ancient Staff", 10, 1, 5, 10, 10, 50)
			self.weapons = [self.weapon]

		elif self.character == 'human':
			pass # nothing

		elif self.character == 'skeleton':
			self.has_magic = False
			self.weapon = weapon.Weapon("Cracked Bone", 1, 1, 1, 10, 10, 1)
			self.weapons = [self.weapon]

	def level_up(self):
		if self.xp >= self.max_xp:
			self.level += 1
			self.xp = 0
			self.max_xp = int(self.max_xp*2.5)

			screen.display_card(self, ["LEVEL UP!"])
			input()

	def attack(self, enemy, buffs, enemies, noloot=False):
		"""Attack the Enemy and add Effects for Buffs"""

		terminal.clear()

		anim = animation.get_attack_animation(self.character)

		for frame in anim:
			terminal.clear()
			screen.display_card(self, frame.split("\n"))
			time.sleep(.2)

		card = []

		raw_dmg = (self.weapon.damage+self.weapon.sharpness)*self.weapon.weight

		card.append(f"+{str(raw_dmg)}")


		dmg = (self.weapon.damage+util.floor(self.weapon.sharpness - enemy.armor.armor))*self.weapon.weight

		armor_block = raw_dmg-dmg

		card.append(f"   -{str(armor_block)} -- armor")

		for buff in buffs:
			if buff.dmg:
				dmg += buff.dmg
				if buff.dmg > 0:
					card.append(f"   +{buff.dmg} --{buff.reason}")
				else:
					card.append(f"   -{buff.dmg} --{buff.reason}")

		if dmg > 0:
			card.append(f" {str(dmg)} Damage")
		else:
			dmg = 0
			card.append(f" {str(dmg)} Damage")

		enemy.life -= dmg

		screen.display_card(self, card)

		if enemy.life <= 0:
			screen.display_card(self, ["You defeated the " + enemy.name])
			enemies.remove(enemy)
			if noloot:
				return
			else:
				self.loot_enemy(enemy)


			

	def loot_enemy(self, enemy):
		"""Loot the Enemy"""

		magic = random.randint(1, 3)

		self.magic += magic
		if self.magic > self.max_magic:
			self.magic = self.max_magic

		for item in enemy.loot:
			self.loot.append(item)

		choice = screen.ask_question(self, enemy.weapon.stats(), ["Keep", "Throw away"])

		if choice == 'keep':
			self.store_weapon(enemy.weapon)


		choice = screen.ask_question(self, enemy.armor.stats(), ["Keep", "Throw away"])

		if choice == 'keep':
			self.store_armor(enemy.armor)
		
				
			

		

	
	def get_stats(self):
		"""Return Basic Player Stats"""
		if self.has_magic:
			return f"LIFE: {str(self.life)}/{str(self.max_life)} | MAGIC: {str(self.magic)}/{str(self.max_magic)} | GOLD: {str(self.gold)}"
		else:
			return f"LIFE: {str(self.life)}/{str(self.max_life)} | GOLD: {str(self.gold)}"





	def eat(self):
		"""Eat Food to Heal"""
		while True:
			terminal.clear()
			print(self.get_stats())

			print("\n\n")
	
			items = []
	
			for item in sorted(self.food):
				if item in randomness.valid_foods:
					exist = False
					for i in items:
						if item == i[0]:
							i[1] += 1
							exist = True
					if not exist:
						items.append([item, 1])
	
			for item in items:
				print(f"{item[0]} x{str(item[1])}")
	
			print("\nChoose an item to eat")
			print("type 'exit' to leave")
	
			choice = input("-> ").lower()

			if choice == 'exit':
				return
	
			if choice in self.food:
				found = False
				for food in randomness.foods:
					if food['name'].lower() == choice:
						print("You ate a " + choice)
						print("+"+str(food['health']) + " health")
						self.life += food['health']
						if self.life > self.max_life:
							self.life = self.max_life
						found = True
						self.food.remove(choice)
				if not found:
					print(choice+" is not a food!")
	
			input("\n\nPress Enter to Continue")

	def shuffle_loadout(self):
		"""Shuffle Weapon and Armor Loadout"""
		while True:
			terminal.clear()
	
			print("#### CURRENT LOADOUT ####\n")
			print(f"\nWEAPON: {self.weapon.name.capitalize()} DMG: {str(self.weapon.damage)} | SHRP: {str(self.weapon.sharpness)} | WGHT: {str(self.weapon.weight)} | TIER: {str(self.weapon.tier)}")
			print(f"\nARMOR: {self.armor.name.capitalize()} ARMOR: {str(self.armor.armor)} | TIER: {str(self.armor.tier)}")
	
			print("\n\n")
	
			print("[1] Equip Weapon")
			print("[2] Equip Armor")
			print("[3] Exit")
	
			choice = util.get_input('-> ', valid=['1', '2', '3'])
	
			if choice == '1':
				valids = []
				for w in self.weapons:
					index = str(self.weapons.index(w))
					valids.append(index)
					print(f"[{index}] {w.name} DMG: {str(w.damage)} | SHRP: {str(w.sharpness)} | WGHT: {str(w.weight)} | TIER: {str(w.tier)}")
	
				index = int(util.get_input("-> ", valid=valids))
	
				self.equip_weapon(self.weapons[index])
	
			elif choice == '2':
				valids = []
				for a in self.armors:
					index = str(self.armors.index(a))
					valids.append(index)
					print(f"[{index}] {a.name} ARMOR: {str(a.armor)} | TIER: {str(a.tier)}")
	
				index = int(util.get_input("-> ", valid=valids))
	
				self.equip_armor(self.armors[index])
	
			else:
				break

			input("Press Enter to Continue")

			
		

	def equip_weapon(self, weapon):
		"""Equip A Weapon"""
		self.weapon = weapon
		screen.display_card(self, [f"{self.weapon.name} equiped"])
		input()

	def store_weapon(self, weapon):
		"""Store A Weapon"""
		if len(self.weapons) >= 3:
			choice = screen.ask_question(self, "Not enough space to store weapon!", ["Throw away", "Replace a different weapon"])

			if choice == 'throw away':
				screen.display_card(self, ["You threw the " + weapon.name + " away"])
				input()

			else:
				weapons = []
				for w in self.weapons:
					weapons.append(f"{w.name} DMG: {str(w.damage)} | SHRP: {str(w.sharpness)} | WGHT: {str(w.weight)} | TIER: {str(w.tier)}")

				choice = screen.ask_question(self, "Choose a weapon to be replaced: ", weapons)

				self.weapons[weapons.index(choice)] = weapon

				screen.display_card(self, ["Weapon stored."])
				input()
		else:
			self.weapons.append(weapon)
			screen.display_card(self, ["Weapon stored."])
			input()


	def equip_armor(self, armor):
		"""Equip Armor"""
		self.armor = armor
		screen.display_card(self, [f"{self.armor.name} equiped"])

	def store_armor(self, armor):
		"""Store Armor"""
		if len(self.armors) >= 3:
			choice = screen.ask_question(self, "Not enough space to store armor!", ["Throw away", "Replace a different armor"])

			if choice == 'throw away':
				screen.display_card(self, ["You threw the " + armor.name + " away"])
				input()

			else:
				armors = []
				for a in self.armors:
					armors.append(f"{a.name} ARMOR: {str(a.armor)} | TIER: {str(a.tier)}")

				choice = screen.ask_question(self, "Choose an armor to be replaced: ", armors)

				self.armors[armors.index(choice)] = armor

				screen.display_card(self, ["Armor stored."])
				input()
		else:
			self.armors.append(armor)
			screen.display_card(self, ["Armor stored."])
			input()