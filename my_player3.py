# CS561 HW2 Mini GO
# Zhiqin Lei
# USCID: 1436737564

import sys
import random
import timeit
import time
import math
import argparse
from collections import Counter
from copy import deepcopy

start_time = time.time() # record the time cost

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

steps = ['0']

if previous_board == [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]:
    F = open("steps.txt", "w")
    F.write('0')
    F.close
else:
    F = open("steps.txt", "r+")
    steps = F.readlines()
    
    
next_steps = str(int(steps[0]) + 1)
F = open("steps.txt", "w")
F.write(next_steps)
F.close

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
                if position(p, board) == player and p not in visited and p not in queue:
                    queue.append(p)
    return all_allies

def check_liberty(piece, board, player):
    all_allies = all_ally(piece, board, player)
    liberty_num = 0

    for a in all_allies:
        neighbors = neighbor(a)
        for p in neighbors:
            positions = position(p,board)
            if positions == 0:
                liberty_num += 1
    return liberty_num

def dead_num(player, board):
    dead_num = 0
    for piece in GO:
        p = position(piece, board)
        if p == player:
            if check_liberty(piece, board, player) == 0:
                dead_num += 1
    return dead_num

def place(piece, board, player):
    opponent = 3-player
    after_board = board
    change_board(piece, after_board, player)

    dead_pieces = set()

    for p in GO:
        positions = position(p, after_board)
        if positions == opponent:
            if check_liberty(p, after_board, opponent) == 0:
                dead_pieces.add(p)
               
    if dead_num == 0:
        return after_board
    else:
        for i in list(dead_pieces):
            after_board = change_board(i, after_board, 0)
        return after_board
    
def valid_move(player, previous, current):
    moves = []
    valid_moves = []
    liberty = set()

    for p in GO:
        if position(p, current) == player:
            end = set()
            ally = all_ally(p, current, player)
            for m in ally:
                n = neighbor(m)
                for i in n:
                    if position(i, current) == 0:
                        end.add(i)
            
            if len(end) ==1:
                liberty = liberty|end
                
                i,j = p[0], p[1]
                if i==0 or i == 4 or j==0 or j==4:
                    safe = set()
                    e = list(end)  
                    nn = neighbor(e[0])
                    for k in nn:
                        if position(k, current) == 0:
                            safe.add(k)
                            if safe:
                                liberty = liberty|safe
        
        elif position(p, current) == 3- player:
            op = set() 
            opp = all_ally(p, current, 3-player)
            for o in opp:
                oo = neighbor(o)
                for i in oo:
                    if position(i, current) == 0:
                        op.add(i)
            liberty = liberty|op
        
        elif position(p, current) == 0:
            board_copy = deepcopy(current)
            after = place(p, board_copy, player)
            if check_liberty(p, after, player) > 0 and after != current and after != previous:
                valid_moves.append(p)
        
    if len(liberty):
        for x in list(liberty):
            board_copy = deepcopy(current)
            after = place(x, board_copy, player)
            if check_liberty(x, after, player) > 0 and after != current and after != previous:

                moves.append(x)
        if len(moves) != 0:
            
            return moves

    return valid_moves

def evaluate(player, board):
    black_piece = 0
    white_piece = 0
    endangered_black = 0 
    endangered_white = 0

    for piece in GO:
        
        if position(piece, board) == 1:
            black_piece += 1

            liberty_num = check_liberty(piece, board, player)
            if liberty_num <= 1:
                endangered_black += 1
            
        if position(piece, board) == 2:
            white_piece += 1

            liberty_num = check_liberty(piece, board, player)
            if liberty_num <= 1:
                endangered_white += 1
    
    white_piece += 2.5

    if player == 1:
        value = black_piece - white_piece + endangered_white *0.5 - endangered_black *0.5
    if player == 2:
        value = white_piece - black_piece + endangered_black *0.5 - endangered_white *0.5
    return value

def MAX(board, previous, player, depth, alpha, beta):

    opponent = 3 - player

    if depth == 0:
        value = evaluate(player, board)
        return value, []
    
    max_score = -9999
    best_actions = []
    valid_moves = valid_move(player, previous, board)
    

    if board == [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]:
        return 100, [(2,2)]

    for move in valid_moves:
        board_copy = deepcopy(board)
        next_board = place(move, board_copy, player)
        score, actions = MIN(next_board, board, opponent, depth -1, alpha, beta)

        if score > max_score:
            max_score = score
            best_actions = [move] 

        if max_score > beta:
            return max_score, best_actions
        
        if max_score > alpha:
            alpha = max_score
    
    return max_score, best_actions

def MIN(board, previous, player, depth, alpha, beta):
   
    opponent = 3 - player

    if depth == 0:
        value = evaluate(player, board)
        return value, []

    min_score = 9999
    worst_actions = []
    valid_moves = valid_move(player, previous, board)

    for move in valid_moves:
        board_copy = deepcopy(board)
        next_board = place(move, board_copy, player)
        score, actions = MAX(next_board, board, opponent, depth-1, alpha, beta)

        if score < min_score:
            min_score = score
            worst_actions = [move] 

        if min_score < alpha:
            return min_score, worst_actions
        
        if min_score < beta:
            beta = min_score

    return min_score, worst_actions



def minmax(player, board, previous):
    global steps
    
    num = int(steps[0])
    
    depth = 1
    
    
    if player == 1 and num == 11:
        depth =2
    
    if player == 2 and num == 11:
        depth =1
    
   
    print('num: ' , num)
    print('depth: ', depth)

    score, actions = MAX(board, previous, player, depth, -9999, 9999)
    

    if actions == []:
        return "PASS"
    else:
        return actions[0]


result = minmax(player, current_board, previous_board) 


ans = ""

end_time = time.time()
print("time= ", end_time-start_time)

if result != "PASS":
    f = open("output.txt", "w")
    ans += str(result[0]) + ',' + str(result[1])
    f.write(ans)
    f.close

if result == "PASS":
    f = open("output.txt", "w")
    ans = "PASS"
    f.write(ans)
    f.close

