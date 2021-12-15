import numpy as np
from euler import Euler
# from atari import Atari

class Heuristic:
    def __init__(self, player, game_state):
        self.player = player
        self.opponent = 3 - player
        self.game_state = np.copy(game_state)

    # maximize the number of stones not on edge
    def get_number_of_stones(self):
        number_of_stones = 0
        for r in range(1,4):
            for c in range(1,4):
                if self.game_state[r,c] == self.player:
                    number_of_stones += 1
                elif self.game_state[r,c] == self.opponent:
                    number_of_stones -= 1
        return number_of_stones

    # maximize the number of stones on edge
    def get_number_of_edge_stones(self):
        number_of_edge_stones = 0
        for r in range(0,5):
            for c in range(0,5):
                if r==0 or r==4 or c==0 or c==4:
                    if self.game_state[r,c] == self.player:
                        number_of_edge_stones += 1
                    elif self.game_state[r,c] == self.opponent:
                        number_of_edge_stones -= 1
        return number_of_edge_stones

    # minimze the euler number
    def get_euler_number(self):
        player_euler = Euler(self.player,self.game_state)
        opponent_euler = Euler(self.opponent,self.game_state)
        pe = player_euler.euler_number()
        oe = opponent_euler.euler_number()
        return pe - oe

    # maximize the liberty 
    def get_liberty(self):
        liberty_player = set()
        liberty_opponent = set()
        for r in range(0,5):
            for c in range(0,5):
                if self.game_state[r,c] == self.player:
                    player_neighbor = self.calculate_liberty(r,c)
                    for pn in player_neighbor:
                        if self.game_state[pn[0],pn[1]] == self.player:
                            liberty_player.add(pn)
                elif self.game_state[r,c] == self.opponent:
                    opponent_neighbor = self.calculate_liberty(r,c)
                    for on in opponent_neighbor:
                        if self.game_state[on[0],on[1]] == self.opponent:
                            liberty_opponent.add(on)
        return len(liberty_player)-len(liberty_opponent)

    def calculate_liberty(self, row, col):
        neighbor = []
        if row>0:
            neighbor.append((row-1,col))
        if col<4:
            neighbor.append((row,col+1))
        if row<4:
            neighbor.append((row+1,col))
        if col>0:
            neighbor.append((row,col-1))
        return neighbor

    # minimize the atari
    # def get_atari(self):
    #     player_atari = Atari(self.player,self.game_state)
    #     opponent_atari = Atari(self.opponent,self.game_state)
    #     return player_atari.calculate_atari() - opponent_atari.calculate_atari()


    # # maximize the liberty 
    # def get_liberty(self):
    #     liberty = 0
    #     for r in range(0,5):
    #         for c in range(0,5):
    #             if self.game_state[r,c] == self.player:
    #                 liberty += self.calculate_liberty(r,c)
    #             elif self.game_state[r,c] == self.opponent:
    #                 liberty -= self.calculate_liberty(r,c)
    #     return liberty

    # def calculate_liberty(self, row, col):
    #     neighbor = []
    #     if row>0:
    #         neighbor.append(self.game_state[row-1,col])
    #     if col<4:
    #         neighbor.append(self.game_state[row,col+1])
    #     if row<4:
    #         neighbor.append(self.game_state[row+1,col])
    #     if col>0:
    #         neighbor.append(self.game_state[row,col-1])
    #     return neighbor.count(0)
        
