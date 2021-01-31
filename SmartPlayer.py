# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (default, Jul 16 2020, 14:00:26) 
# [GCC 9.3.0]
# Embedded file name: /Users/bo/Documents/projects/561/TA Spring 2020/QL-Example-For-TicTacToe/SmartPlayer.py
# Compiled at: 2020-01-30 16:30:12
# Size of source mod 2**32: 2805 bytes
from Board import Board
from RandomPlayer import RandomPlayer
import numpy as np
WIN_REWARD = 1.0
DRAW_REWARD = 0.0
LOSS_REWARD = -1.0

class SmartPlayer:

    def __init__(self, side=None):
        self.side = side
        self.transition = {}

    def set_side(self, side):
        self.side = side

    def learn(self, board):
        pass

    def move(self, board):
        if board.game_over():
            return
        else:
            random_number = np.random.randint(10)
            if random_number > 1:
                score, action = self._max(board)
                return board.move(action[0], action[1], self.side)
            randomPlayer = RandomPlayer(side=(self.side))
            return randomPlayer.move(board)

    def _min(self, board):
        state = board.encode_state()
        if state in self.transition:
            return self.transition[state]
        if board.game_result == 0:
            return (
             DRAW_REWARD, None)
        if board.game_result == self.side:
            return (WIN_REWARD, None)
        else:
            if board.game_result > 0:
                return (
                 LOSS_REWARD, None)
            min_value, action = WIN_REWARD, None
            candidates = [(i, j) for i in range(3) if board.state[i][j] == 0 for j in range(3)]
            for i, j in candidates:
                copyBoard = Board(board.state)
                if self.side == 1:
                    opponent = 2
                else:
                    opponent = 1
                copyBoard.move(i, j, opponent)
                score, a = self._max(copyBoard)
                if score < min_value or action == None:
                    min_value, action = score, (i, j)
                    if min_value == LOSS_REWARD:
                        self.transition[state] = (
                         min_value, action)
                        break
                self.transition[state] = (
                 min_value, action)

            return (
             min_value, action)

    def _max(self, board):
        state = board.encode_state()
        if state in self.transition:
            return self.transition[state]
        if board.game_result == 0:
            return (
             DRAW_REWARD, None)
        if board.game_result == self.side:
            return (WIN_REWARD, None)
        else:
            if board.game_result > 0:
                return (
                 LOSS_REWARD, None)
            max_value, action = DRAW_REWARD, None
            candidates = [(i, j) for i in range(3) if board.state[i][j] == 0 for j in range(3)]
            for i, j in candidates:
                b = Board(board.state)
                b.move(i, j, self.side)
                score, a = self._min(b)
                if score > max_value or action == None:
                    max_value, action = score, (i, j)
                    if max_value == WIN_REWARD:
                        self.transition[state] = (
                         max_value, action)
                        break
                self.transition[state] = (
                 max_value, action)

            return (
             max_value, action)
# okay decompiling SmartPlayer.pyc
