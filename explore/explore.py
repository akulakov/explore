#!/usr/bin/env python3

import os, sys
from avkutil import Term

WIDTH, HEIGHT = 75, 20
init_loc = int(WIDTH/2), int(HEIGHT/2)
level_loc = 0,0     # row, col

chars = dict(
    player = '★',
    space = ' ',
    rock = '▣',
)
rock = chars["rock"]

class BoardDef:
    def __init__(self, rooms, corridors):
        self.rooms, self.corridors = rooms, corridors

row1 = [
     BoardDef(rooms = [(Loc(30,7),10,5),
                        ],
                  corridors = [(Loc(40,40), None, 'r'),
                   ],

     BoardDef([(Loc(30,7),10,5),
                ],
               [(Loc(40,40), None, 'l')
                ]
]
level.append(row1)


def mkrow(size):
    return [[rock] for _ in range(size)]


class Player:
    def __init__(self, loc, board, char):
        self.loc = Loc(loc)
        self.board = board
        self.char = char

    def __str__(self):
        return self.char

    def move(self, newloc):
        self.board[self.loc].remove(self)
        try: self.board[self.loc].remove(self)
        except:pass
        self.board[newloc].append(self)
        # print("self.board", self.board.board)
        print("moving from %s to %s" % (self.loc, newloc))
        # input()

    def move_dir(self, x_mod, y_mod):
        x,y = self.loc
        x += x_mod
        y += y_mod
        loc = Loc(x,y)
        if not (0 <= x <= WIDTH-1) or not (0 <= y <= HEIGHT-1):
            return False
        if self.board[loc] and chars["rock"] in self.board[loc]:
            return False
        self.move(loc)
        self.loc = loc

    def up(self): self.move_dir(0,-1)
    def down(self): self.move_dir(0,1)
    def right(self): self.move_dir(1,0)
    def left(self): self.move_dir(-1,0)
    def up_right(self): self.move_dir(1,-1)
    def up_left(self): self.move_dir(-1,-1)
    def down_left(self): self.move_dir(-1,1)
    def down_right(self): self.move_dir(1,1)
        
class Loc:
    def __init__(self, x, y=None):
        if y is None:
            x, y = x
        self.x, self.y = x, y

    def __iter__(self):
        yield self.x; yield self.y

    def __repr__(self):
        return "<Loc: %d,%d>" % tuple(self)
        

class Board:
    def __init__(self, width, height):
        self.board = [mkrow(width) for _ in range(height)]

    def load(self, bdef):
        for room in bdef.rooms:
            make_room(*room)
        for c in bdef.corridors:
            make_line(*c)

    def __setitem__(self, k, val):
        self.board[k.y][k.x].append(val)

    def __getitem__(self, k):
        return self.board[k.y][k.x]

    def display(self):
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
                self[Loc(x,y)].remove(rock)
        if y==y2:
            x, x2 = min(x,x2), max(x,x2)
            for x in range(x,x2+1):
                self[Loc(x,y)].remove(rock)
        

board = Board(WIDTH, HEIGHT)

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

    def __init__(self):
        self.level_loc = ll = level_loc
        self.player = Player(init_loc, board, chars["player"])
        board[Loc(init_loc)] = self.player 
        board_def = level[ll[0]][ll[1]]
        make_room(Loc(30,7), 10, 5)
        make_line(Loc(40,10), dir='r')
        board.display()

    def quit(self):
        sys.exit()
        
    def main_loop(self):
        t = Term()
        player = self.player
        while True:
            board.display()
            c = t.getch().decode("utf-8")
            print("c", c)
            if c not in self.cmds:
                print("command not found")
                continue
            obj, cmd = self.cmds[c].split('.')
            m = getattr(locals()[obj], cmd)
            m()
        
    
Explore().main_loop()
