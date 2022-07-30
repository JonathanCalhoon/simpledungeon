import random, time
from code import util, randomness, screen


screen_size = 10

screen = screen.Screen()


#width is 65 counting borders
#actual width is 63




def animate_entry(dungeon, x, y, settings, stats):
    """Show the portal open and disappear as the player enters"""
    dungeon[y][x] = '@'


    delay = .5
    base_map = build_display_map(dungeon, x, y)

    for row in base_map:
        if '@' in row:
            y = base_map.index(row)
            for i in row:
                if i == '@':
                    x = row.index(i)

    base_map[y][x] = '.'

    display(settings, base_map, x, y, stats, noplace=True)

    time.sleep(delay)

    base_map[y][x] = '@'

    display(settings, base_map, x, y, stats, noplace=True)

    time.sleep(delay)

    base_map[y+1][x] = '.'
    base_map[y-1][x] = '.'
    base_map[y][x+1] = '.'
    base_map[y][x-1] = '.'

    display(settings, base_map, x, y, stats, noplace=True)

    time.sleep(delay)

    base_map[y][x] = 'p'

    display(settings, base_map, x, y, stats, noplace=True)

    time.sleep(delay)








def build_display_map(dungeon, x, y):
    """Cuts the full map into a size based on the users location"""
    # TODO: Fix this crap
    display_map = []
    for i in range(-screen_size, screen_size):
        try:
            display_map.append(dungeon[y+i])
        except:
            display_map.append(["."]*screen_size)
    final = []
    for row in display_map:
        new_row = []
        for i in range(-screen_size+x, screen_size+1+x):
            try:
                new_row.append(row[i])
            except:
                new_row.append(".")
                
        final.append(new_row)
    return final
    
    

def display(settings, dungeon, x, y, stats=[], noplace=False):
    print("\033[H",end="")
    if not noplace:
        dungeon[y][x] = 'p'
    _map = build_display_map(dungeon, x, y)

    out_list = []

    out_list.append("---"*21+"--")
    for stat in stats:
        count = int((60-len(stat))/2)
        _str = "|  " + (" "*count) + stat + (" "*count)
        if len(_str) == 62:
            _str += "  |"
        else:
            _str += " |"

        out_list.append(_str)

        
    out_list.append("---"*21+"--")
    for row in _map:
        r = "|"
        for cell in row:
            if cell == 't':
                r += settings.treasure
            elif cell == '*':
                r += settings.shards
            elif cell == 'p':
                r += settings.player
            elif cell == '#':
                r += settings.walls
            elif cell == '.':
                r += settings.empty
            elif cell == ' ':
                r += settings.floor
            elif cell == '@':
                r += settings.portal
            elif cell == 'exit':
                r += " 🚪"
            elif cell == '-':
                r += '---'
            else:
                r += " "+cell+" "
        out_list.append(r+"|")
    out_list.append("---"*21+"--")
    out_list.append(util.center(" 1. View Stats | 2. Change Loadout | 3. Eat", 65))
    out_list.append(util.center(" 4. Save | 5. Clear Screen", 65))

    screen.display_out(out_list)


class action():
    def __init__(self, dungeon, x, y):
        self.dungeon = dungeon
        self.x = x
        self.y = y
        self.valid = False
        self.treasure = False
        self.character = False
        self.enemy = False
        self.shard = False
        self.portal = False


        self.check_position()

    def check_position(self):
        """Check the position of the character"""
        try:
            item = self.dungeon[self.y][self.x]
        except:
            self.valid = False
            item = ""


        if item in ['#', '@', '.', '|', '-', '+']:
            self.valid = False
        else:
            self.valid = True

        if item == 't':
            self.treasure = True

        if item == '@':
            self.portal = True
            self.valid = False

        if item in randomness.character_symbols:
            self.valid = False
            self.character = item

        if item in randomness.enemy_symbols:
            self.enemy = item
            self.valid = True
        
        if item == '*':
            self.shard = True

        if item in ["⚔","⍬","⇟","⌑","✹"]:
            self.special = item
            self.valid = True
        else:
            self.special = False
        

def getSpawn(dungeon):
    valid = False
    count = 0
    spawny, spawnx = 0,0
    while not valid:
        try:
            if ' ' in dungeon[count]:
                spawny = count
                spawnx = random.randint(0, len(dungeon))
                if dungeon[spawny][spawnx] == ' ':
                    valid = True
            else:
                count += 1
        except:
            pass
    return spawny, spawnx


def check_pos(y, x, dungeon):
    """Checks if the position is valid for Character Placement"""

    # Checks if the character is in a legal spot
    # to keep them from blocking the way for the player
    # checks if the spot above, below, to the right and left
    # of the spawn being tested are clear. 
    # While this will not completely keep the character
    # from blocking the players movement. it should
    # make it a lot less likely to accur. Hopefull...

    pos = dungeon[y][x]
    if pos != ' ':
        return False
    else:
        spots = []

        #check position above
        spots.append(dungeon[y+1][x])

        # check position below
        spots.append(dungeon[y-1][x])

        # check position right
        spots.append(dungeon[y][x+1])

        # check position left
        spots.append(dungeon[y][x-1])

        for position in spots:
            if position != ' ':
                return False
    return True


def place_rand_object(dungeon, obj):
    """Place an Object in a random location somewhere in the dungeon"""
    valid = False
    while True:
        y = random.randint(0, 99)
        if " " in dungeon[y]:
            while True:
                x = random.randint(0, 99)
                if dungeon[y][x] == ' ':
                    dungeon[y][x] = obj
                    return