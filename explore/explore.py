#!/usr/bin/env python3

"""
Explore

One global var is used by Board and Player: `explore`
"""

import os, sys
import random
from avkutil import Term
import npcs
import items
import level

debug=0
WIDTH, HEIGHT = 75, 20
init_loc = int(WIDTH/2), int(HEIGHT/2)
level_loc = (0,0)     # row, col

chars = dict(
    player = '★',
    space = ' ',
    rock = '▨',
)
rock = chars["rock"]

def mkrow(size):
    return [[rock] for _ in range(size)]

class Loc:
    def __init__(self, x, y=None):
        if y is None:
            x, y = x
        self.x, self.y = x, y

    def __iter__(self):
        yield self.x; yield self.y

    def __repr__(self):
        return "<Loc: %d,%d>" % tuple(self)
level_loc = Loc(*level_loc)


class Player:
    def __init__(self, loc, board, char):
        self.loc = Loc(loc)
        self.board = board
        self.char = char
        self.message = False

    def __str__(self):
        return self.char

    def move(self, newloc, old_board=None, oldloc=None):
        B = old_board or self.board
        try:
            B[oldloc or self.loc].remove(self)
        except ValueError as e:
            print(e)
        tile = self.board[newloc]
        # print("tile", tile)
        msg = []
        if tile:
            msg.append("You see a few items here:" if len(tile)>1 else "You see an item here:")
            for item in tile:
                msg.append(item.description)
            msg.append("\nContinue..")
        self.message = msg
        tile.append(self)
        # print("moving from %s to %s" % (self.loc, newloc))
        # print("self.board[newloc]", self.board[newloc])

    def level_move_dir(self, x_mod, y_mod):
        x,y = explore.level_loc
        print("x,y", x,y)
        x += x_mod
        y += y_mod
        loc = Loc(x,y)

        if not (0 <= x <= len(explore.level[0])-1) or not (0 <= y <= len(explore.level)-1):
            return False

        print("to: x,y", x,y)
        # explore.set_board(level[y][x])
        explore.set_board(x, y)
        self.board = explore.board
        self.board.load()
        return True

    def move_dir(self, x_mod, y_mod):
        x,y = self.loc
        x += x_mod
        y += y_mod

        loc = Loc(x,y)

        wi = WIDTH-1
        hi = HEIGHT-1
        old_board = explore.board
        if not (0 <= x <= WIDTH-1) or not (0 <= y <= HEIGHT-1):
            if x<0:
                ok = self.level_left()
                loc = Loc(wi, y)
            elif x>WIDTH-1:
                ok = self.level_right()
                loc = Loc(0,y)
            elif y<0:
                ok = self.level_up()
                loc = Loc(x, hi)
            elif y>HEIGHT-1:
                ok = self.level_down()
                loc = Loc(x, 0)
            if not ok:
                print(1)
                return False
        B = self.board
        # if loc not in B:
            # return False
        if B[loc] and chars["rock"] in B[loc]:
            print(3)
            return False
        old = self.loc
        self.move(loc, old_board, old)
        self.loc = loc
        return True

    def up(self): return self.move_dir(0,-1)
    def down(self): return self.move_dir(0,1)
    def right(self): return self.move_dir(1,0)
    def left(self): return self.move_dir(-1,0)
    def up_right(self): return self.move_dir(1,-1)
    def up_left(self): return self.move_dir(-1,-1)
    def down_left(self): return self.move_dir(-1,1)
    def down_right(self): return self.move_dir(1,1)

    def level_up(self): return self.level_move_dir(0,-1)
    def level_down(self): return self.level_move_dir(0,1)
    def level_right(self): return self.level_move_dir(1,0)
    def level_left(self): return self.level_move_dir(-1,0)


class Board:
    loaded = False

    def __init__(self, rooms, corridors, width=WIDTH, height=HEIGHT, items=None):
        self.items = items or []
        self.width, self.height = width, height
        self.rooms, self.corridors = rooms, corridors
        self.load()

    def __iter__(self):
        return ((x,y) for x in random.randrange(0,WIDTH) for y in random.randrange(0,HEIGHT))

    def random_tile(self):
        for n in range(200):
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, HEIGHT)
            if not self[Loc(x,y)]:
                return self[Loc(x,y)]
        for x,y in self:
            if not self[Loc(x,y)]:
                return self[Loc(x,y)]

    def random_place(self, item):
        tile = self.random_tile()
        tile.append(item)

    def load(self):
        if self.loaded: return
        self.board = [mkrow(self.width) for _ in range(self.height)]
        for room in self.rooms:
            self.make_room(*room)
        for c in self.corridors:
            self.make_line(*c)
        for item in self.items:
            self.random_place(item)
        for _ in range(random.randint(0,6)):
            self.random_place(random.choice(items.items))
        self.loaded = True

    def __setitem__(self, k, val):
        self.board[k.y][k.x].append(val)

    def __getitem__(self, k):
        try:
            return self.board[k.y][k.x]
        except:
            print("k", k)
            raise

    def display(self):
        if not debug:
            os.system("clear")
        def join_row(row):
            return str.join('', [str(x[-1]) if x else chars["space"] for x in row]) # + ['|'])

        print( str.join('\n', [join_row(r) for r in self.board] ))

    def make_room(self, loc, width=None, height=None, loc2=None):
        x, y = loc
        if not width:
            x2, y2 = loc2
            width = x2-x
            height = y2-y
        for y in range(loc.y, loc.y+height):
            for x in range(loc.x, loc.x+width):
                # print(x,y)
                self[Loc(x,y)].remove(rock)

    def make_line(self, start, end=None, dir=None):
        x, y = x2, y2 = start
        if dir:
            # _dir = dict(u=(0,-1), d=(0,1), r=(1,0), l=(-1,0))
            # dir = _dir[dir]
            if dir=='u': y2 = 0
            elif dir=='l': x2 = 0
            elif dir=='d': y2 = HEIGHT-1
            elif dir=='r': x2 = WIDTH-1
            end = Loc(x2,y2)
        x2, y2 = end
        assert x2==x or y2==y
        if x==x2:
            y, y2 = min(y,y2), max(y,y2)
            for y in range(y,y2+1):
                try:
                    self[Loc(x,y)].remove(rock)
                    # vertical corridor should be wider to look better when displayed
                    self[Loc(x+1,y)].remove(rock)
                except: pass
        if y==y2:
            x, x2 = min(x,x2), max(x,x2)
            for x in range(x,x2+1):
                try: self[Loc(x,y)].remove(rock)
                except:
                    pass
                    # print(x,y,self[Loc(x,y)])
                    # raise



# level.append(row1)
# y, x = level_loc
# board = level[y][x]
# board.load()

class Explore:
    cmds = {
            'l': "player.right",
            'h': "player.left",
            'k': "player.up",
            'j': "player.down",
            'u': "player.up_right",
            'y': "player.up_left",
            'b': "player.down_left",
            'n': "player.down_right",
            'q': "self.quit",
            }

    def __init__(self, level):
        self.level_loc = loc = level_loc
        self.level = level
        B = self.board = level[loc.y][loc.x]
        B.load()
        self.player = Player(init_loc, B, chars["player"])
        B[Loc(init_loc)] = self.player
        B.display()

    def set_board(self, x, y):
        self.level_loc = x, y
        self.board = self.level[y][x]

    def quit(self):
        sys.exit()

    def run_cmd(self, cmd):
        player = self.player
        num, cmd = int(cmd[:-1] or 1), cmd[-1]
        if cmd not in self.cmds:
            print("command not found")
            return False
        obj, cmd = self.cmds[cmd].split('.')
        for n in range(num):
            m = getattr(locals()[obj], cmd)
            m()
        return True

    def main_loop(self):
        t = Term()
        while True:
            self.board.display()
            if self.player.message:
                for line in self.player.message:
                    print(line)
                # pause for reading a message
                t.getch()
                self.player.message = False
                self.board.display()
            c = ''
            while not c or c[-1].isdigit():
                c += t.getch().decode("utf-8")
            if not self.run_cmd(c):
                continue


explore = Explore(level.level(Board, Loc))
explore.main_loop()
