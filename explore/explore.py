#!/usr/bin/env python3

import os, sys
from avkutil import Term

player_char = '★'
width, height = 75, 20
init_loc = int(width/2), int(height/2)
space = ' '

def mkrow(size):
    return [[] for _ in range(size)]

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
        if not (0 <= x <= width-1) or not (0 <= y <= height-1):
            return False
        self.move(Loc(x,y))
        self.loc.x, self.loc.y = x, y

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

    def __setitem__(self, k, val):
        self.board[k.y][k.x].append(val)

    def __getitem__(self, k):
        return self.board[k.y][k.x]

    def display(self):
        os.system("clear")
        def join_row(row):
            return str.join('', [str(x[-1]) if x else space for x in row] + ['|'])
            
        print( str.join('\n', [join_row(r) for r in self.board] ))
    

board = Board(width, height)

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
        self.player = Player(init_loc, board, player_char)
        board[Loc(init_loc)] = self.player 
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
