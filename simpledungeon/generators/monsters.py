from classes import weapon, armor
import random
from code import util, terminal
from battle import buff



# gen monster

class Skeleton():
	def __init__(self):
		self.weapon = weapon.Weapon(
			random.choice(['sword', 'rusted sword']),
			random.randint(1, 3), 
			random.randint(1, 3), 
			random.randint(1, 3),
			random.randint(1, 3),
			random.randint(50, 100),
			random.randint(1, 10)
		)
		self.armor = armor.Armor(
			random.choice(['chain mail', 'rusted chain mail']),
			random.randint(1, 3),
			random.randint(1, 3),
			random.randint(50, 100),
			random.randint(1, 6)
		)

		self.id = '☠'
		self.name = 'Skeleton'

		self.life = random.randint(50, 100)
		self.speed = 8 # very fast

		self.loot = [random.choice(['bones', 'skull', 'bones', 'iron', 'iron', 'bones']) for i in range(random.randint(1, 4))]

		self.ether = random.randint(1, 5)

	
		

def gen_random():
	return random.choice(['☠'])


def get_monster(symbol):
	if symbol == '☠':
		return [Skeleton()]

	