import json
from code import terminal, util


defualt = {
    'dungeon_options' : {
        'walls' : '#',
        'floor' : ' ',
        'empty' : '.',
        'treasure' : ' []',
        'player' : 'p',
        'shards' : '*',
        'portal' : '@',
    },
    'color_options' : {
        'walls' : None,
        'floor' : None,
        'empty' : None,
        'treasure' : None,
        'player' : None,
        'shards' : "\033[34m",
        'portal' : None,
    }
}
reset = "\033[0m"

class Settings():
    def __init__(self):
        self.build()
        
    def build(self):
        """Check if Settings File has content, else Initiate Settings"""
        with open('settings/settings.txt', 'r') as file:
            data = json.loads(file.read())

        if not data:
            with open('settings/settings.txt', 'w') as file:
                file.write(json.dumps(defualt))
                data = defualt

        colors = data['color_options']
        dungeon = data['dungeon_options']
        
        if colors['walls']:
            self.walls = colors['walls'] + " " + dungeon['walls'] + " " + reset
        else:
            self.walls = " " + dungeon['walls'] + " "


        if colors['floor']:
            self.floor = colors['floor'] + " " + dungeon['floor'] + " " + reset
        else:
            self.floor = " " + dungeon['floor'] + " "

        if colors['empty']:
            self.empty = colors['empty'] + " " + dungeon['empty'] + " " + reset
        else:
            self.empty = " " + dungeon['empty'] + " "

        if colors['treasure']:
            self.treasure = colors['treasure'] + dungeon['treasure'] +  reset
        else:
            self.treasure = dungeon['treasure']

        if colors['player']:
            self.player = colors['player'] + " " + dungeon['player'] + " " + reset
        else:
            self.player = " " + dungeon['player'] + " "

        if colors['shards']:
            self.shards = colors['shards'] + " " + dungeon['shards'] + " " + reset
        else:
            self.shards = " " + dungeon['shards'] + " "

        if colors['portal']:
            self.portal = colors['portal'] + " " + dungeon['portal'] + " " + reset
        else:
            self.portal = " " + dungeon['portal'] + " "


    def setup(self):
        """Change Settings around"""


        with open('settings/settings.txt', 'r') as file:
            current = json.loads(file.read())

        while True:
            terminal.clear()
    
            print("   SETTINGS   ")
            print("\n\n")
    
            print(f"[1] Walls: {self.walls}")
            print(f"[2] Floor: {self.floor}")
            print(f"[3] Empty: {self.empty}")
            print(f"[4] Treasure: {self.treasure}")
            print(f"[5] Player: {self.player}")
            print(f"[6] Shards: {self.shards}")
            print(f"[7] Portals: {self.portal}")
            print("[8] Import Color Scheme")
            print("[9] Export Color Scheme")
            print("[10] Exit")
    
            c1 = util.get_input("-> ", valid=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])

            if c1 == '10':
                return

            if c1 == '8':
                scheme = input("Enter Color Scheme: ")
                try:
                    new = json.loads(scheme)
                    with open('settings/settings.txt', 'w') as file:
                        file.write(json.dumps(new))
                except:
                    print("Scheme failed!")

                print("Theme Saved")

                util.cont()

            if c1 == '9':
                with open('settings/settings.txt', 'r') as file:
                    data = json.loads(file.read())
                print("Color Scheme: ")
                print(data)

                util.cont()

                return

    
            print("[1] Edit Symbol")
            print("[2] Edit Color")
            print("[3] Back")
    
            c2 = util.get_input("-> ", valid=['1', '2', '3'])
    
            if c2 == '3':
                pass
    
            if c2 == '1':
                dungeon = current['dungeon_options']
                if c1 == '1':
                    symbol = input("Type a symbol for walls: ")
                    if len(symbol) == 1:
                        dungeon['walls'] = symbol
                    else:
                        print(f"{symbol} is too long. Must be 1 character")
    
                elif c1 == '2':
                    symbol = input("Type a symbol for floor: ")
                    if len(symbol) == 1:
                        dungeon['floor'] = symbol
                    else:
                        print(f"{symbol} is too long. Must be 1 character")
    
                elif c1 == '3':
                    symbol = input("Type a symbol for empty: ")
                    if len(symbol) == 1:
                        dungeon['empty'] = symbol
                    else:
                        print(f"{symbol} is too long. Must be 1 character")
    
                elif c1 == '4':
                    symbol = input("Type a symbol for treasure (3 symbols): ")
                    if len(symbol) == 3:
                        dungeon['treasure'] = symbol
                    else:
                        print(f"{symbol} is not valid. Treasure must be 3 symbols")
    
                elif c1 == '5':
                    symbol = input("Type a symbol for player: ")
                    if len(symbol) == 1:
                        dungeon['player'] = symbol
                    else:
                        print(f"{symbol} is too long. Must be 1 character")
    
                elif c1 == '6':
                    symbol = input("Type a symbol for shards: ")
                    if len(symbol) == 1:
                        dungeon['shards'] = symbol
                    else:
                        print(f"{symbol} is too long. Must be 1 character")
    
                elif c1 == '7':
                    symbol = input("Type a symbol for portals: ")
                    if len(symbol) == 1:
                        dungeon['portal'] = symbol
                    else:
                        print(f"{symbol} is too long. Must be 1 character")

                current['dungeon_options'] = dungeon
    
                        
            elif c2 == '2':
                print("Type RGB Value seperated by Comma's (with no spaces)")
    
                val = input("-> ")
                valid = False
                
                try:
                    val = val.split(",")
                    if len(val) == 3:
                        valid = True
                except:
                    valid = False
    
    
                if not valid:
                    print("Not a valid color!")
                    util.cont()
    
                elif valid:
                    colors = current['color_options']
                    color = terminal.custom([val[0], val[1], val[2]])
                    if c1 == '1':
                        colors['walls'] = color
                    elif c1 == '2':
                        colors['floor'] = color
                    elif c1 == '3':
                        colors['empty'] = color
                    elif c1 == '4':
                        colors['treasure'] = color
                    elif c1 == '5':
                        colors['player'] = color
                    elif c1 == '6':
                        colors['shards'] = color
                    elif c1 == '7':
                        colors['portal'] = color

                    current['color_options'] = colors

            with open('settings/settings.txt', 'w') as file:
                file.write(json.dumps(current))
        
        
            self.build()
                
    
    
    
    
    
    
    
            

        


        