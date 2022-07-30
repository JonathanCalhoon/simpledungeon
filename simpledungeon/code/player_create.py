from code import util, terminal



def pick():
	"""Pick a player type"""

	terminal.clear()

	print("Choose your warrior: ")


	print("""

	    KNIGHT

	[+] Increased Battle Damage
	[+] Increased Durability
	[+] Better Spawn Armor

	[-] Cannot use Magic


	    SKELETON

	[+] Skeletons will not attack
	[+] Heal without eating

	[-] Everything else will attack
	[-] Cannot use potions
	[-] Cannot eat


	    WIZARD

	[+] Increased Magic
	[+] Increased Durability

	[-] Decreased Health


	    HUMAN

	[+] Nothing

	[-] Nothing

	""")

	choice = util.get_input("-> ", valid=["knight", "skeleton", "wizard", "human"])

	name = util.get_input("Name for your character: ")