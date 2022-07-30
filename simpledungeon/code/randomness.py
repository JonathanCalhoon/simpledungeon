import random
import copy

loot = [
    {"type":"food", "name":"healing potion", "max":1},
    {"type":"food", "name":"dry bones", "max":1},
    {"type":"inventory", "name":"potion of energy", "max":1},
    {"type":"food", "name":"moldy apple", "max":1},
    {"type":"food", "name":"old potato", "max":1},
    {"type":"food", "name":"withered carrot", "max":1},
    {"type":"food", "name":"severed hand", "max":1},
    {"type":"food", "name":"severed finger", "max":1},
    {"type":"food", "name":"rotting flesh", "max":1},
    {"type":"food", "name":"moldy bread", "max":1},
    {"type":"food", "name":"squishy tomato", "max":1},
    {"type":"food", "name":"damp onion", "max":1},
    {"type":"food", "name":"onion", "max":1},
    {"type":"food", "name":"bread", "max":1},
    {"type":"food", "name":"apple", "max":1},
    {"type":"armor", "name":"", "max":1},
    {"type":"weapon", "name":"", "max":1},
    {"type":"gold", "name":"", "max":25}
]


foods = [
    {'name':'dry bones', 'health':2},
    {'name':'moldy apple', 'health':10},
    {'name':'old potato', 'health':10},
    {'name':'withered carrot', 'health':6},
    {'name':'severed hand', 'health':30},
    {'name':'severed finger', 'health':16},
    {'name':'rotting flesh', 'health':-6},
    {'name':'squishy tomato', 'health':8},
    {'name':'damp onion', 'health':6},
    {'name':'onion', 'health':12},
    {'name':'bread', 'health':20},
    {'name':'moldy bread', 'health':16},
    {'name':'apple', 'health':15},
]

valid_foods = [
    'dry bones',
    'moldy apple',
    'old potato',
    'withered carrot',
    'severed hand',
    'severed finger',
    'rotting flesh',
    'squishy tomato',
    'damp onion',
    'onion',
    'bread',
    'moldy bread',
    'apple',
]

valid_potions = ['potion of energy', 'healing potion']

valid_spells = ['sana ego', 'sana vulnera', 'sana omnis ego', 'confirma impetum', 'confirma defensio', 'noxa hostilis']


enemy_symbols = ['☠']


character_symbols = ['R', 'D', "L"]




knight = """
----------
|   __   |
|  [--]  |
| \/||\} |
|   /\   |
----------""".split("\n")

archer = """
------------
|  __      |
| (OO)|\   |
| \||-||-> |
|  /\ |/   |
------------""".split("\n")

wizard = """
--------
|  __  |
| (**) |
| //\\\ |
| /__\ |
--------""".split("\n")

human = """
--------
|  __  |
| (oo) |
| /||\ |
|  /\  |
--------""".split("\n")

skeleton = """
--------
|  __  |
| (xx) |
| /][\ |
|  /\  |
--------""".split("\n")

def get_char(player):
    if player.character == "knight":
        return copy.deepcopy(knight)
    elif player.character == "archer":
        return copy.deepcopy(archer)
    elif player.character == "wizard":
        return copy.deepcopy(wizard)
    elif player.character == "human":
        return copy.deepcopy(human)
    elif player.character == "skeleton":
        return copy.deepcopy(skeleton)