import numpy as np
from little_go import Little_Go
from heuristics import Heuristic
from random import shuffle

class Alpha_Beta:
    def __init__(self, player, previous_game_state, current_game_state) -> None:
        self.player = player
        self.opponent = 3 - player
        self.previous_game_state = previous_game_state
        self.current_game_state = current_game_state

    def get_next_move(self):
        board = Little_Go(self.player,self.previous_game_state,self.current_game_state)
        starting_moves = [(2,2), (2,1), (1,2), (2,3), (3,2)]        # best starting moves in 5X5 board
        possible_moves = board.get_possible_moves()            # number of empty places on the board
        valid_moves = board.get_valid_moves()                  # number of valid moves on the board

        if len(valid_moves)==0:
            return "PASS"

        # if there are at most 4 stones on the board, check if any of the best move is a valid move
        if len(possible_moves)>20:                                 
            for sm in starting_moves:
                if sm in valid_moves:
                    return sm

        # find the best move using the alpha beta algorithm
        move = self.maximize(board,3,-12345,12345)
        print(move)
        if move[0] == -12345:
            return "PASS"
        return move[1]

    # check if there are any empty spaces left on the board
    def isTerminal(self, board: Little_Go):
        terminal = len(board.get_possible_moves())
        if terminal == 1:
            return True
        return False

    # player is trying to maximize the values given by the opponent
    def maximize(self, board: Little_Go, depth, alpha, beta):
        if self.isTerminal(board) or depth==0:
            score = self.calculate_score(board)
            board.switch_player()
            return score, [5,5]

        value = -12345
        valid_moves = board.get_valid_moves()
        best_move = [0,0]
        shuffle(valid_moves)
        for valid_move in valid_moves:
            board.update_previous_game_state()
            board.place_stone(valid_move[0],valid_move[1])
            dead_stones = board.remove_dead_stones()
            board.switch_player()
            temp_value = self.minimize(board, depth-1, alpha, beta)[0]
            if value < temp_value:
                value =  temp_value
                best_move[0] = valid_move[0]
                best_move[1] = valid_move[1]   
            if value >= beta:
                board.remove_stone(valid_move[0],valid_move[1])
                for dead in dead_stones:
                    board.place_stone_opponent(dead[0],dead[1])
                board.switch_player()
                return value, valid_move
            alpha = max(alpha, value)
            board.remove_stone(valid_move[0],valid_move[1])
            for dead in dead_stones:
                board.place_stone_opponent(dead[0],dead[1])
        board.switch_player()
        return value, best_move

    # opponent is trying to minimize the values given by the player
    def minimize(self, board: Little_Go, depth, alpha, beta):
        if self.isTerminal(board) or depth==0:
            score = self.calculate_score(board)
            board.switch_player()
            return score, [5,5]

        value = 12345
        valid_moves = board.get_valid_moves()
        best_move = [0,0]
        shuffle(valid_moves)
        for valid_move in valid_moves:
            board.update_previous_game_state()
            board.place_stone(valid_move[0],valid_move[1])
            dead_stones = board.remove_dead_stones()
            board.switch_player()
            temp_value = self.maximize(board, depth-1, alpha, beta)[0]
            if value > temp_value:
                value = temp_value
                best_move[0] = valid_move[0]
                best_move[1] = valid_move[1]
            if value <= alpha:
                board.remove_stone(valid_move[0],valid_move[1])
                for dead in dead_stones:
                    board.place_stone_opponent(dead[0],dead[1])
                board.switch_player()
                return value, valid_move
            beta = min(beta, value)
            board.remove_stone(valid_move[0],valid_move[1])
            for dead in dead_stones:
                board.place_stone_opponent(dead[0],dead[1])
        board.switch_player()
        return value, best_move

    # heuristic evaluation function
    def calculate_score(self, board: Little_Go):
        heuristic = Heuristic(board.get_player(),board.get_game_state())       
        number_of_centre_stones = heuristic.get_number_of_stones()
        number_of_edge_stones = heuristic.get_number_of_edge_stones()
        liberty = heuristic.get_liberty()
        euler_number = heuristic.get_euler_number()
        # atari = heuristic.get_atari()
        # score = -2*euler_number + 1.5*(1.5*number_of_centre_stones + number_of_edge_stones) + 1.25*liberty - 1.5*atari
        score = -4*euler_number + 5*number_of_centre_stones + number_of_edge_stones + min(max(liberty,-4), 4)
        return -score