from Board import Board
import numpy as np

class RandomPlayer:

    def __init__(self, side=None):
        self.side = side

    def set_side(self, side):
        self.side = side

    def move(self, board):
        if board.game_over():
            return
        else:
            candidates = []
            for i in range(0, 3):
                for j in range(0, 3):
                    if board.state[i][j] == 0:
                        candidates.append(tuple([i, j]))

            idx = np.random.randint(len(candidates))
            random_move = candidates[idx]
            return board.move(random_move[0], random_move[1], self.side)

    def learn(self, board):
        pass

