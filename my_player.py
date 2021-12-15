import numpy as np
from alpha_beta import Alpha_Beta

if __name__=='__main__':

    #Read Input
    with open("C:/Users/suviy/OneDrive/Desktop/CSCI 561 - Artificial Intelligence/Homework/HW2/mywork/inputs/input3.txt", "r") as input_file:
        input = input_file.read().splitlines() 

    player_color = int(input[0])
    previous_game_state = np.zeros((5,5)).astype(int)
    current_game_state = np.zeros((5,5)).astype(int)

    r=0
    for row in input[1:6]:
        c=0
        for stone in row:
            previous_game_state[r,c] = int(stone)
            c+=1
        r+=1

    r=0
    for row in input[6:]:
        c=0
        for stone in row:
            current_game_state[r,c] = int(stone)
            c+=1
        r+=1
    
    alpha_beta = Alpha_Beta(player_color,previous_game_state,current_game_state)
    #Finds the best next move
    next_move = alpha_beta.get_next_move()
    
    #Write the next move in an output file
    with open("C:/Users/suviy/OneDrive/Desktop/CSCI 561 - Artificial Intelligence/Homework/HW2/mywork/output.txt", "w") as fp:
        if next_move=="PASS":
            fp.writelines("PASS")
        else:
            fp.writelines(str(next_move[0])+","+str(next_move[1]))