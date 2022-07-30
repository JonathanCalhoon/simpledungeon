




with open("assets/attack_animations.txt", "r") as file:
	data = file.read()

attack_animations = data.split("ANIMATION")

with open("assets/defend_animations.txt", "r") as file:
	data = file.read()

defend_animations = data.split("ANIMATION")

quick_index = ['knight', 'archer', 'wizard', 'human', 'skeleton']



def get_attack_animation(_type):
	animation = attack_animations[quick_index.index(_type)]
	return animation.split("FRAME")

def get_defend_animation(_type):
	animation = defend_animations[quick_index.index(_type)]
	return animation.split("FRAME")

