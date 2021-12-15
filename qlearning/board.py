import numpy as np

class Board:
    def __init__(self, previous_game_state, current_game_state):
        self.previous_game_state = np.copy(previous_game_state)
        self.current_game_state = np.copy(current_game_state)
        self.count = 0

    def move_count(self):
        self.count += 1

    def get_move_count(self):
        return self.count

    def encode_state(self, game_state=None):
        """ Encode the current state of the board as a string
        """
        if game_state is None:
            s =  ''.join([str(self.current_game_state[r][c]) for r in range(0,5) for c in range(0,5)])
        else:
            s =  ''.join([str(game_state[r][c]) for r in range(0,5) for c in range(0,5)])
        return s

    def display_board(self):
        for r in range(0,5):
            disp = ""
            for c in range(0,5):
                disp += str(self.current_game_state[r,c])
            print(disp)

    # def switch_board(self,player):
    #     switched_board = np.copy(self.current_game_state)
    #     switched_board[switched_board==player] = 3
    #     switched_board[switched_board==3-player] = player
    #     switched_board[switched_board==3]=3-player
    #     return switched_board

    # def symmetry(self,player):
    #     left_right_symmetry = np.copy(self.current_game_state)
    #     up_down_symmetry = np.copy(self.c)
    #     left_right_up_down_symmetry = np.copy(left_right_symmetry)


    def get_current_state(self):
        current_state = np.copy(self.current_game_state)
        return current_state

    def update_previous_game_state(self, previous_state):
        # for r in range(0,5):
        #     for c in range(0,5):
        #         self.previous_game_state[r,c] = previous_state[r,c]
        self.previous_game_state = previous_state

    def check_pass(self):
        # for r in range(0,5):
        #     for c in range(0,5):
        #         if self.previous_game_state[r,c] != self.current_game_state[r,c]:
        #             return False
        # return True
        return np.array_equal(self.current_game_state,self.previous_game_state)

    def clear(self):
        self.count = 0
        # for r in range(0,5):
        #     for c in range(0,5):
        #         self.current_game_state[r,c] = 0
        self.current_game_state.fill(0)

    def update_board(self, row, col, player):
        self.current_game_state[row,col] = player
        self.remove_dead_stones(player)

    def game_result(self):
        black_stones = np.count_nonzero(self.current_game_state==1)
        white_stones = np.count_nonzero(self.current_game_state==2) + 2.5
        if black_stones>white_stones:
            return 1
        else:
            return 2
            
    # get all the empty places on the board
    def get_possible_moves(self):
        empty_spaces = [(r,c) for r, row in enumerate(self.current_game_state) for c, i in enumerate(row) if i == 0]
        return empty_spaces

    # get all the valid moves on the board
    def get_valid_moves(self, player):
        valid_moves = []
        for r in range(0,5):
            for c in range(0,5):
                if self.current_game_state[r,c]==0:
                    if self.check_validity(r,c, player):
                        valid_moves.append((r,c))
        return valid_moves
            
    # check if the move is valid or not
    def check_validity(self, row, col, player):
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

        self.current_game_state[row,col] = player
        # check if the move has liberty
        if self.liberty_rule(row,col,player):
            self.current_game_state[row,col] = 0
            return True
        
        # remove dead opposition stones and check liberty again, if True now then check for KO rule
        dead_stones = self.remove_dead_stones(player)
    
        if not self.liberty_rule(row,col,player):
            for dead in dead_stones:
                self.current_game_state[dead[0],dead[1]]=3-player
            self.current_game_state[row,col] = 0
            return False
        else:
            if self.ko_rule():
                for dead in dead_stones:
                    self.current_game_state[dead[0],dead[1]]=3-player
                self.current_game_state[row,col] = 0
                return False
            for dead in dead_stones:
                self.current_game_state[dead[0],dead[1]]=3-player
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
    def remove_dead_stones(self,player):
        dead_stones = []
        opponent = 3-player
        opponent_stones_index = np.where(self.current_game_state==opponent)
        opponent_stones_index = list(zip(opponent_stones_index[0],opponent_stones_index[1]))
        for osi in opponent_stones_index:
            if not self.liberty_rule(osi[0],osi[1],opponent):
                dead_stones.append(osi)
        
        for dead in dead_stones:
            self.current_game_state[dead[0],dead[1]]=0 
        return dead_stones

    # check if the capture is resulting in previous state
    def ko_rule(self):
        return np.array_equal(self.current_game_state,self.previous_game_state)
