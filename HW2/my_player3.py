# CS561 HW2 Mini GO
# Zhiqin Lei
# USCID: 1436737564

import sys
import random
import timeit
import math
import argparse
from collections import Counter
from copy import deepcopy

# read the input file
f = open("input.txt", 'r+')
player = int(f.readline().rstrip('\n')) # line 1: indicate color (black = 1, white = 2)
opponent = 3- player                    # if player is black, enemy is white, else enemy is black 
previous_board = []                     
current_board = []
for i in range (5):                     # line 2-6: the previous state of the 5x5 game board
    row = []                            # the state after player's last move
    line = f.readline().rstrip('\n')    # black = 1, white = 2, unoccupied = 0
    for piece in line:
        row.append(int(piece))
    previous_board.append(row)

for i in range (5):                     # line 7-11: the current state of the game board.
    row = []                            # the state after opponent's last move
    line = f.readline().rstrip('\n')
    for piece in line:
        row.append(int(piece))
    current_board.append(row)

GO = []
for i in range(5):
    for j in range(5):
        GO.append((i,j))

def p(piece):
    return piece[0],piece[1]

def position(piece, board):
    return board[piece[0]][piece[1]]

def change_board(piece, board, typ):
    board[piece[0]][piece[1]] = typ
    return board

def neighbor(piece):
    # detect neighbbots of piece in i,j position
    # i: row number, j: column number
    i,j = p(piece)
    neighbors = []
    if i == 0:
        if j == 0:
            neighbors.append((i+1, j))
            neighbors.append((i, j+1))
        if 1 <= j <= 3:
            neighbors.append((i+1, j))
            neighbors.append((i, j+1))
            neighbors.append((i, j-1))
        if j == 4:
            neighbors.append((i, j-1))
            neighbors.append((i+1, j))
    if 1 <= i <= 3:
        if j == 0:
            neighbors.append((i+1, j))
            neighbors.append((i-1, j))
            neighbors.append((i, j+1))
        if 1 <= j <= 3:
            neighbors.append((i+1, j))
            neighbors.append((i-1, j))
            neighbors.append((i, j+1))
            neighbors.append((i, j-1))
        if j == 4:
            neighbors.append((i+1, j))
            neighbors.append((i-1, j))
            neighbors.append((i, j-1))
    if i == 4:
        if j == 0:
            neighbors.append((i-1, j))
            neighbors.append((i, j+1))
        if 1 <= j <= 3:
            neighbors.append((i-1, j))
            neighbors.append((i, j+1))
            neighbors.append((i, j-1))
        if j == 4: 
            neighbors.append((i-1, j))
            neighbors.append((i, j-1))
    return neighbors

def all_ally(piece, board, player):
    queue = [piece]
    visited = set()
    all_allies = []
    while queue:
        member = queue.pop(0)
        if member not in visited:
            visited.add(member)
            all_allies.append(member)
            neighbors = neighbor(member)
            for p in neighbors:
                if position(p, board) != player:
                    neighbors.remove(p)
                if position(p, board) == player and p not in visited and p not in queue:
                    queue.append(p)
    return all_allies

def check_liberty(piece, board, player):
    all_allies = all_ally(piece, board, player)

    for a in all_allies:
        neighbors = neighbor(a)
        for p in neighbors:
            position = position(p,board)
            if position != 1 and position != 2:
                return True
    return False


def place(piece, board, player):
    opponent = 3-player
    after_board = board
    change_board(piece, after_board, player)

    dead_pieces = set()
    dead_num = 0

    for p in GO:
        position = position(p, board)
        if position == opponent:
            if check_liberty(p, board, player) == False:
                dead_pieces.add(p)
                dead_num += 1

    if dead_num == 0:
        return after_board, dead_num, after_board
    else:
        for i in list(dead_pieces):
            next_board = change_board(i, after_board, 0)
        return next_board, dead_num, after_board
    
