from random import choice
import numpy as np
from numpy.lib import copy
from board import Board

import pickle

class QLearner:

    def __init__(self, player, q_table=None, alpha=.9, gamma=.9, initial_value=.01):
        self.player = player
        self.alpha = alpha
        self.gamma = gamma
        if q_table is None:
            self.q_table = {}
        else:
            self.q_table = q_table
        self.history_states = []
        self.initial_value = initial_value
        self.board_coordinates = np.array(np.arange(0,25,1))
        self.wins = 0

    # def set_player(self, player):
    #     self.player = player

    def get_next_move(self, board: Board):
        # check if max moves limit reached
        if board.get_move_count()>=24:
            return board

        previous_state = board.get_current_state()                        # store the current state before making changes
        valid_moves = board.get_valid_moves(self.player)                  # number of valid moves on the board

        # if no valid moves then PASS
        if len(valid_moves)==0:
            board.update_previous_game_state(previous_state)
            board.move_count()
            return board

        state = board.encode_state()                            # encode current game state in string to act as a key for its q values
        # q_value = np.reshape(np.asarray(self.Q(state)),(5,5))                                 # get the q values for the current game state
        q_value = np.reshape(self.Q(state),(5,5))
        # make q values for invalid moves = 0
        board_matrix = np.zeros((5,5)).astype(int)
        x, y  = [*zip(*valid_moves)]
        board_matrix[np.array(x), np.array(y)] = 1
        q_value[board_matrix==0] = 0
        # self.update_q_value(state,q_value.ravel())

        q_value_list = np.copy(q_value.ravel())                 # flatten q value for current state in a list
        
        # if valid moves also have 0 in their respective q values then PASS
        if sum(q_value_list)==0:
            board.update_previous_game_state(previous_state)
            board.move_count()
            return board

        # convert the q values into normalized values between 0 and 1 to serve as probability for the next move
        normalized_q_values = [float(i)/sum(q_value_list) for i in q_value_list]
        # if not a number obtained in the normalized values, raise error
        nan = [n for n in normalized_q_values if np.isnan(n)]
        assert(len(nan)==0),("Probability distribution contains nan",valid_moves,q_value_list,normalized_q_values)
        # select the next move with the probability obtained 
        coord = np.random.choice(self.board_coordinates,None,True, normalized_q_values)
        # conversion from row major form
        row = int(coord/5)
        col = int(coord%5)
        move = (row,col)
        
        symmetry_board = board.get_current_state()
        """ rotate the current game state 3 times 90 degree
        for each rotation find the upside-down, right-left and left-right-upside-down game states
        for each game state obtained add to history states with updating the moves """
        i=0
        for i in range(2):
            board_flip_upside_down = np.flipud(symmetry_board)
            move_upside_down = (4-row,col)
            board_flip_left_right = np.fliplr(symmetry_board)
            move_left_right = (row,4-col)
            board_flip_left_right_upside_down = np.flipud(board_flip_left_right)
            move_left_right_upside_down = (4-row,4-col)
            self.history_states.append((board.encode_state(symmetry_board),(row,col)))
            self.history_states.append((board.encode_state(board_flip_upside_down),move_upside_down))
            self.history_states.append((board.encode_state(board_flip_left_right),move_left_right))
            self.history_states.append((board.encode_state(board_flip_left_right_upside_down),move_left_right_upside_down))
            if i==0:
                temp_board = np.zeros((5,5)).astype(int)
                temp_board[row,col] = 1
                temp_board = np.rot90(temp_board)
                index = np.where(temp_board==1)
                index = list(zip(index[0],index[1]))
                symmetry_board = np.rot90(symmetry_board)
                row, col = index[0][0], index[0][1]

        board.move_count()
        board.update_previous_game_state(previous_state)
        return board.update_board(move[0],move[1],self.player)
        


    # def get_best_move(self, board: Board):
    #     if board.get_move_count()>24:
    #         return board
    #     previous_state = board.get_current_state()
    #     state = board.encode_state()
    #     q_values = self.Q(state)
    #     valid_moves = board.get_valid_moves(self.player)                  # number of valid moves on the board
    #     if len(valid_moves)==0:
    #         board.update_previous_game_state(previous_state)
    #         board.move_count()
    #         return board
    #     while True:
    #         best_move, max_q_value = self.get_max(q_values)
    #         if max_q_value == 0:
    #             best_move = choice(valid_moves)
    #             break
    #         if best_move in valid_moves:
    #             break
    #         else:
    #             q_values[best_move[0]][best_move[1]] = 0
    #     self.history_states.append((board.encode_state(),best_move))
    #     board.move_count()
    #     board.update_previous_game_state(previous_state)
    #     return board.update_board(best_move[0],best_move[1],self.player)

    def get_max(self, q_values):
        result = np.where(q_values == np.amax(q_values))
        return list(zip(result[0], result[1]))[0],np.amax(q_values)

    def Q(self, state):
        if state not in self.q_table:
            q_val = np.zeros(25)
            q_val.fill(self.initial_value)
            # q_val = q_val.tolist()
            self.q_table[state] = q_val
        #     q_val = np.zeros((5, 5))
        #     q_val.fill(self.initial_value)
        #     self.q_table[self.player][state] = q_val
        return self.q_table[state]

    def get_wins(self):
        wins = copy(self.wins)
        return wins

    def learn(self, board: Board):
        """ when games ended, this method will be called to update the qvalues
        """
        result = board.game_result()
        if result == self.player:
            self.wins += 1
            reward = 1
        else:
            reward = 0
      
        self.history_states.reverse()
        for i in range(0,8):
            final_state, final_move = self.history_states[i]
            q = np.reshape(self.Q(final_state),(5,5))
            # q = np.reshape(np.asarray(self.Q(final_state)),(5,5))
            q[final_move[0]][final_move[1]] = reward
            # self.update_q_value(final_state,q.ravel())

        max_q_value = reward
        symmetry = 0
        for hist in self.history_states[8:]:
            state, move = hist
            q = np.reshape(self.Q(state),(5,5))
            # q = np.reshape(np.asarray(self.Q(state)),(5,5))
            q[move[0]][move[1]] = (q[move[0]][move[1]] * (1 - self.alpha)) + (self.alpha * self.gamma * max_q_value)
            # self.update_q_value(state,q.ravel())
            symmetry+=1
            if symmetry==8:
                max_q_value = np.max(q)
                symmetry = 0
        self.history_states = []

    # def update_q_value(self, state, q_value):
    #     self.q_table[state] = q_value.tolist()

    def get_q_table(self):
        return self.q_table



# board_flip_upside_down = np.flipud(board.get_current_state())
        # move_upside_down = (4-row,col)
        # board_flip_left_right = np.fliplr(board.get_current_state())
        # move_left_right = (row,4-col)
        # board_flip_left_right_upside_down = np.flipud(board_flip_left_right)
        # move_left_right_upside_down = (4-row,4-col)
        # self.history_states.append((board.encode_state(board_flip_upside_down),move_upside_down))
        # self.history_states.append((board.encode_state(board_flip_left_right),move_left_right))
        # self.history_states.append((board.
        # 
        # 
        # (board_flip_left_right_upside_down),move_left_right_upside_down))
        # add players reversed
        # switched_board = board.switch_board(self.player)