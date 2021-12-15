import random
import numpy as np

class Little_Go:
    def __init__(self, player_color, previous_game_state, current_game_state):
        self.player_color = player_color
        self.opponent_color = 3 - player_color
        self.previous_game_state = np.copy(previous_game_state)
        self.current_game_state = np.copy(current_game_state)

    # returns the current game state
    def get_game_state(self):
        return np.copy(self.current_game_state)

    # returns the current player
    def get_player(self):
        return self.player_color

    # update the previous game state
    def update_previous_game_state(self):
        self.previous_game_state = np.copy(self.current_game_state)

    # switch players for alpha beta
    def switch_player(self):
        temp = self.player_color
        self.player_color = self.opponent_color
        self.opponent_color = temp

    # put stone corresponding to the move
    def place_stone(self, row, col):
        self.current_game_state[row, col] = self.player_color

    def place_stone_opponent(self, row, col):
        self.current_game_state[row, col] = self.opponent_color

    # remove the stone corresponding to the move
    def remove_stone(self, row, col):
        self.current_game_state[row, col] = 0

    # get the 4 diagonal coordinates
    def get_diagonal_coordinates(self, row, col):
        neighbor = []
        if row>0 and col>0:
            neighbor.append((row-1,col-1))
        if row>0 and col<4:
            neighbor.append((row-1,col+1))
        if row<4 and col<4:
            neighbor.append((row+1,col+1))
        if row<4 and col>0:
            neighbor.append((row+1,col-1))
        return neighbor

    # get all the empty places on the board
    def get_possible_moves(self):
        empty_spaces = [(r,c) for r, row in enumerate(self.current_game_state) for c, i in enumerate(row) if i == 0]
        return empty_spaces

    # get all the valid moves on the board
    def get_valid_moves(self):
        valid_moves = []
        for r in range(0,5):
            for c in range(0,5):
                if self.current_game_state[r,c]==0:
                    if self.check_validity(r,c):
                        valid_moves.append((r,c))
        return valid_moves
            
    # check if the move is valid or not
    def check_validity(self, row, col):
        # out of bounds
        if row>=5 or row<0 or col<0 or col>=5:
            return False

        # already a stone exists at the place
        if self.current_game_state[row,col]!=0:
            return False

        # if any neigbour is empty then it is a valid move
        neighbours = self.get_neighbor_stones(row,col)
        if 0 in neighbours:
            return True

        self.current_game_state[row,col] = self.player_color
        # check if the move has liberty
        if self.liberty_rule(row,col,self.player_color):
            self.current_game_state[row,col] = 0
            return True
        
        # remove dead opposition stones and check liberty again, if True now then check for KO rule
        dead_stones = self.remove_dead_stones()
    
        if not self.liberty_rule(row,col,self.player_color):
            for dead in dead_stones:
                self.current_game_state[dead[0],dead[1]]=self.opponent_color
            self.current_game_state[row,col] = 0
            return False
        else:
            if self.ko_rule():
                for dead in dead_stones:
                    self.current_game_state[dead[0],dead[1]]=self.opponent_color
                self.current_game_state[row,col] = 0
                return False
            for dead in dead_stones:
                self.current_game_state[dead[0],dead[1]]=self.opponent_color
            self.current_game_state[row,col] = 0
        return True

    # get the 4 neighboring stones
    def get_neighbor_stones(self, row, col):
        neighbor = []
        if row>0:
            neighbor.append(self.current_game_state[row-1,col])
        if col<4:
            neighbor.append(self.current_game_state[row,col+1])
        if row<4:
            neighbor.append(self.current_game_state[row+1,col])
        if col>0:
            neighbor.append(self.current_game_state[row,col-1])
        return neighbor
    
    # get the 4 neighboring coordinates
    def get_neighbor_coordinates(self, row, col):
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

    # get the neighboring coordinates having our stone
    def get_neighbor_allies(self, row, col, player):
        neighbor_allies = []
        neighbor = self.get_neighbor_coordinates(row,col)
        for n in neighbor:
            if self.current_game_state[n[0],n[1]]==player:
                neighbor_allies.append(n)
        return neighbor_allies

    # get the coordinates of the connected group of our stone
    def get_allies(self, row, col, player):
        allies = []
        player_color_allies = [(row,col)]             # queue having all the player color neighbors of the move
        while len(player_color_allies)!=0:
            first_ally = player_color_allies.pop()
            allies.append(first_ally)
            neighbor_allies = self.get_neighbor_allies(first_ally[0],first_ally[1], player)
            for n in neighbor_allies:
                if n not in player_color_allies and n not in allies:
                    player_color_allies.append(n)
        return allies

    # check if the move has any liberty
    def liberty_rule(self, row, col, player):
        allies = self.get_allies(row,col,player)
        for ally in allies:
            neighbor = self.get_neighbor_stones(ally[0],ally[1])
            if 0 in neighbor:
                return True
        return False

    # remove all the captured opposition stones
    def remove_dead_stones(self):
        dead_stones = []
        opponent_stones_index = np.where(self.current_game_state==self.opponent_color)
        opponent_stones_index = list(zip(opponent_stones_index[0],opponent_stones_index[1]))
        for osi in opponent_stones_index:
            if not self.liberty_rule(osi[0],osi[1],self.opponent_color):
                dead_stones.append(osi)
        
        for dead in dead_stones:
            self.current_game_state[dead[0],dead[1]]=0 
        return dead_stones

    # check if the capture is resulting in previous state
    def ko_rule(self):
        return np.array_equal(self.current_game_state,self.previous_game_state)

    def display_board(self):
        for r in range(0,5):
            disp = ""
            for c in range(0,5):
                disp += str(self.current_game_state[r,c])
            print(disp)
