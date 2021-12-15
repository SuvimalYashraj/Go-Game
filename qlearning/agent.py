import numpy as np
import json
from board import Board
from alpha_beta import Alpha_Beta
from qlearner import QLearner
from random_player import Random_Player
from pickle import dump,load,HIGHEST_PROTOCOL

class Agent:
    def __init__(self) -> None:
        self.wins = 0

    def get_next_move(self, player, previous_game_state, current_game_state):
        #alpha_beta = Alpha_Beta(player,previous_game_state,current_game_state)
        # best_move = self.qlearner_agent(player,previous_game_state,current_game_state)
        self.qlearning(player, previous_game_state, current_game_state)
        return [0,0]
        # return alpha_beta.get_next_move()

    # def qlearner_agent(self, player, previous_game_state, current_game_state):
    #     board = Board(previous_game_state,current_game_state)
    #     q_learner = QLearner(player)
    #     if player==1:
    #         pickle_off = open ("black_q_table.txt", "rb")
    #         black_q_table = load(pickle_off)
    #         q_learner.get_best_move(board,black_q_table)
    #     else:
    #         pickle_off = open ("white_q_table.txt", "rb")
    #         white_q_table = load(pickle_off)
    #         q_learner.get_best_move(board,{},white_q_table)
        

    def qlearning(self, player, previous_game_state, current_game_state):
        board = Board(previous_game_state,current_game_state)
        pickle_off = open ("black_q_table.txt", "rb")
        q_table_black = load(pickle_off)
        pickle_off = open ("white_q_table.txt", "rb")
        q_table_white = load(pickle_off)
        # self.train_as_white(board, QLearner(2), Random_Player(1), 100)
        # self.train_as_black(board, QLearner(1), Random_Player(2), 100)
        # with open('json_black.json','r') as fp:
        #     q_table_black = json.loads(fp.read())
        # with open('json_white.json','r') as fp:
        #     q_table_white = json.loads(fp.read())
        
        self.train(board, QLearner(1,q_table_black), QLearner(2,q_table_white), 10000000)

    def train(self, board: Board, player1: QLearner, player2: QLearner, iterations):
        print("files loaded")
        checkpoint=1
        for iteration in range(0,iterations):
            self.play(board, player1, player2)
            board.clear()

            checkpoint += 1
            if checkpoint == 10000:
                self.update_q_table(player1)
                self.update_q_table(player2)
                print(iteration)
                checkpoint = 0
            
        result1 = player1.get_wins()
        result2 = player2.get_wins()
        print("black = "+ str(result1) + " white = "+str(result2))
        self.update_q_table(player1)
        self.update_q_table(player2)

    def play(self, board: Board, player1: QLearner, player2: QLearner):
        while board.get_move_count()<24:
            # print("stuck before black move "+str(board.get_move_count()))
            # board.display_board()
            flag1 = 0
            player1.get_next_move(board)
            if board.check_pass():
                flag1=1
                if flag2==1:
                    break
            # print("stuck before white move "+str(board.get_move_count()))
            # board.display_board()
            flag2 = 0
            player2.get_next_move(board)
            if board.check_pass():
                flag2=1
                if flag1==1:
                    break

        player1.learn(board)
        player2.learn(board)
        
    # def train_as_black(self, board: Board, player: QLearner, opponent: Random_Player, iterations):
    #     checkpoint = 1
    #     for iteration in range(0,iterations):
    #         self.play_black(board, player, opponent)
    #         board.clear()

    #         checkpoint += 1
    #         if checkpoint == 10000:
    #             self.update_q_table(player)
    #             print(iteration)
    #             checkpoint = 0
            
    #     results = player.get_wins()
    #     print(results)
    #     self.update_q_table(player)
 
    # def train_as_white(self, board: Board, player: QLearner, opponent: Random_Player, iterations):
    #     checkpoint = 1
    #     for iteration in range(0,iterations):          
    #         self.play_white(board, player, opponent)
    #         board.clear()

    #         checkpoint += 1
    #         if checkpoint == 10000:
    #             self.update_q_table(player)
    #             checkpoint = 0
    #             print(iteration)  

    #     results = player.get_wins()
    #     print("white" + str(results))
    #     self.update_q_table(player) 

    # def play_black(self, board: Board, player: QLearner, opponent: Random_Player):
    #     while board.get_move_count()<24:
    #         # print("stuck before black move "+str(board.get_move_count()))
    #         # board.display_board()
    #         flag1 = 0
    #         player.get_next_move(board)
    #         if board.check_pass():
    #             flag1=1
    #             if flag2==1:
    #                 break
    #         # print("stuck before white move "+str(board.get_move_count()))
    #         # board.display_board()
    #         flag2 = 0
    #         opponent.get_next_move(board)
    #         if board.check_pass():
    #             flag2=1
    #             if flag1==1:
    #                 break

    #     player.learn(board)

    # def play_white(self, board: Board, player: QLearner, opponent: Random_Player):
    #     while board.get_move_count()<24:
    #         # print("stuck before black move "+str(board.get_move_count()))
    #         # board.display_board()
    #         flag1 = 0
    #         opponent.get_next_move(board)
    #         if board.check_pass():
    #             flag1=1
    #             if flag2==1:
    #                 break
    #         # print("stuck before white move "+str(board.get_move_count()))
    #         # board.display_board()
    #         flag2 = 0
    #         player.get_next_move(board)
    #         if board.check_pass():
    #             flag2=1
    #             if flag1==1:
    #                 break

    #     player.learn(board)
   
    def update_q_table(self, player: QLearner):
        # wins = player.get_wins()
        # print(wins - self.wins)
        # self.wins = wins
        q_table = player.get_q_table()
        # json_table = json.dumps(q_table)
        # if player.player==1:
        #     with open("json_black.json","w") as fp:
        #         json.dump(json_table,fp)
        # if player.player==2:
        #     with open("json_white.json","w") as fp:
        #         json.dump(json_table,fp)
        if player.player==1:
            with open("black_q_table.txt", "wb") as fp:
                dump(q_table, fp, protocol=HIGHEST_PROTOCOL)
        else:
            with open("white_q_table.txt", "wb") as fp:
                dump(q_table, fp, protocol=HIGHEST_PROTOCOL)