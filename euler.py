import numpy as np

class Euler:
    N1_pattern = [
        np.array([[0, 0], [0, 1]]),
        np.array([[0, 0], [1, 0]]),
        np.array([[0, 1], [0, 0]]),
        np.array([[1, 0], [0, 0]]),
    ]
    N3_pattern = [
                np.array([[0, 1], [1, 1]]),
                np.array([[1, 0], [1, 1]]),
                np.array([[1, 1], [0, 1]]),
                np.array([[1, 1], [1, 0]]),
            ]

    ND_pattern = [
                np.array([[0, 1], [1, 0]]),
                np.array([[1, 0], [0, 1]]),
            ]

    def __init__(self, player, game_state):
        self.euler_game_state = np.copy(game_state)
        self.player = player
        for r in range(0,5):
            for c in range(0,5):
                if self.euler_game_state[r,c]==player:
                    self.euler_game_state[r,c]=1
                else:
                    self.euler_game_state[r,c]=0

    def euler_number(self):   
            N1, N3, ND = 0, 0, 0

            for r in range(0,5):  # go over rows
                for c in range(0,5):  # go over colums
                    game_slice = self.euler_game_state[r : r + 2, c : c + 2]
                    N1 += self.match_N1(game_slice)
                    N3 += self.match_N3(game_slice)
                    ND += self.match_ND(game_slice)
            return (N1 - N3 + 2*ND)/4

        
    def match_N1(self, game_slice):
        for pattern in Euler.N1_pattern:
            if np.all(pattern == game_slice):
                return 1
        return 0

    def match_N3(self, game_slice):
        for pattern in Euler.N3_pattern:
            if np.all(pattern == game_slice):
                return 1
        return 0

    def match_ND(self, game_slice):
        for pattern in Euler.ND_pattern:
            if np.all(pattern == game_slice):
                return 1
        return 0