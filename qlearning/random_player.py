from random import choice
from board import Board

from board import Board

class Random_Player:
    def __init__(self, player) -> None:
        self.player = player

    def get_next_move(self, board: Board):
        if board.get_move_count()>=24:
            return board
        previous_state = board.get_current_state()
        valid_moves = board.get_valid_moves(self.player)
        if len(valid_moves)==0:
            board.move_count()
            board.update_previous_game_state(previous_state)
            return board
        random_move = choice(valid_moves)
        board.move_count()
        board.update_previous_game_state(previous_state)
        return board.update_board(random_move[0],random_move[1],self.player)