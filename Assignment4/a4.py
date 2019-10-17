import math
import random

DEBUG = False

def display(state):
    i = 0
    print('-----------')
    for i in range(0,9):
        if state[i] == 0:
            print('  ' , end = '')
            print('|' , end = '')
            if (i+1) % 3 == 0:
                print('\n' , end = '')
                print('-----------')
            else:
                print(' ', end = '')
        else:
            if (state[i] == 1):
                print("o " , end = '')
                print("|" , end = '')
            if (state[i] == 2):
                print("x " , end = '')
                print("|" , end = '')
            if (i+1) % 3 == 0:
                print('\n' , end = '')
                print('-----------')
            else:
                print(' ', end = '')

            
#chess = [0 , 1,  2 , 1 , 0 , 1 , 1 , 0 , 2]
#display(chess)



def check_win(state):
    if (state[0] == state[1] and state[1] == state[2] and state[0] != 0):
        return True
    if (state[3] == state[4] and state[4] == state[5] and state[3] != 0):
        return True
    if (state[6] == state[7] and state[7] == state[8] and state[6] != 0):
        return True
    if (state[0] == state[3] and state[3] == state[6] and state[0] != 0):
        return True
    if (state[1] == state[4] and state[4] == state[7] and state[1] != 0):
        return True
    if (state[2] == state[5] and state[5] == state[8] and state[2] != 0):
        return True
    if (state[0] == state[4] and state[4] == state[8] and state[0] != 0):
        return True
    if (state[2] == state[4] and state[4] == state[6] and state[2] != 0):
        return True
    return False





def Pure_Monte_Carlo_Tree_Search(chess , user_use):
    # print("-------------------------------------------------------")
    # The availbale move for the whole chess board , compute every available move and compute the score for it
    # return the highest score
    if user_use == 1:
        user = 1
        computer = 2
    else:
        user = 2
        computer = 1

    move_score = {}
    chess_board = chess.copy()
    Available_move_whole_chess = []
    for i in range(len(chess_board)):
        if (chess[i] == 0):
            Available_move_whole_chess.append(i)
            move_score.setdefault(i , 0)
    # print(Available_move_whole_chess)               # FOR DEBUG
    # move_score = {0:0 , 1:0 , 2:0 , 3:0 , 4:0 , 5:0 , 6:0 , 7:0 , 8:0}
    length = len(Available_move_whole_chess)
    for available_index in Available_move_whole_chess:
        #print('available_index: ' , available_index)
        chess_board = chess.copy()
        # move_score = [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]
        move = available_index
        # print('move: ' , move)
        Available_move = Available_move_whole_chess.copy()
        Available_move.remove(move)
        
        # print('Available_move: ' , Available_move)
        #chess_board[move] = computer                                    # computer use x that's 2
        #temp_chess = chess_board.copy()
        #temp_chess[move] = user
        '''
        for direct_win in Available_move_whole_chess:
            temp_win_check = chess_board.copy()
            temp_win_check[direct_win] = computer
            if (check_win(temp_win_check)):
                chess_board[move] = computer
                return direct_win
        
        for direct_lose in Available_move_whole_chess:
            temp_chess = chess_board.copy()
            temp_chess[move] = user
            if (check_win(temp_chess)):
                return move
        '''
        chess_board[move] = computer 
        
        for random_play_many_times in range(1000):
            if (check_win(chess_board)):
                if user == 1:
                    move_score[move] += length                                        # if user o is win lose score
                else:
                    move_score[move] -= length 
                continue 

    
            # simulation two player
            chess_board_forloop = chess_board.copy()
            if (DEBUG): print('chess_board_forloop_outside: ' , chess_board_forloop) # FOR DEBUG
            Available_move_forloop = Available_move.copy()
            if (DEBUG): print('Available_move_forloop: ' , Available_move_forloop)   # FOR DEBUG
            length_Available_move = len(Available_move_forloop)

            
            for j in range(100):
                if (len(Available_move_forloop) <= 0):
                    break
                if (DEBUG): print('Available_move_forloop: ' , Available_move_forloop)
                random_move_one = random.choice(Available_move_forloop)             # random choose a move , actuall choose it index , move -> index
                if (DEBUG): print('random_move_one: ' , random_move_one)
                Available_move_forloop.remove(random_move_one)
                if (DEBUG): print("random_move: " , random_move_one)                # FOR DEBUG
                chess_board_forloop[random_move_one] = user                                    # simulate user o that's 1
                if (DEBUG): print("chess_board_forloop: ")                          # FOR DEBUG
                if (DEBUG): display(chess_board_forloop)
                if (check_win(chess_board_forloop)):
                    
                    if user == 1:
                        move_score[move] -= length - j                                      # if user o is win lose score
                    else:
                        move_score[move] += length - j  
                    break


                if (len(Available_move_forloop) <= 0):
                    break
                random_move_two = random.choice(Available_move_forloop)
                if (DEBUG): print('random_move_two: ' , random_move_two)            # FOR DEBUG
                Available_move_forloop.remove(random_move_two)
                if (DEBUG): print("random_move: " , random_move_two)                # FOR DEBUG
                chess_board_forloop[random_move_two] = computer                                 # simulate computer x that's 2
                if (DEBUG): print("chess_board: ")                                  # FOR DEBUG
                if (DEBUG): display(chess_board_forloop)                            # FOR DEBUG
                if (check_win(chess_board_forloop)):
                    
                    if user == 1:
                        move_score[move] += length - j                              # if computer x win plus score
                    else:
                        move_score[move] -= length - j  
                    break
                
                if (len(Available_move_forloop) == 0):
                    break
                if (DEBUG): print("move_score: " , move_score)                      # FOR DEBUG
            
        chess_board[move] = 0
    '''
    if sum(move_score) == 0 and len(Available_move_whole_chess) != 0:
        return Available_move_whole_chess[0]
    if sum(move_score) == 0:
        return None
    '''
    # print("move_score: " , move_score)

    '''
    for i in range(len(move_score)):
        if (abs(move_score[i]) == 100000):
            
            #print('Available_move_whole_chess:' , Available_move_whole_chess)
            for direct_win in Available_move_whole_chess:
                temp_win_check = chess_board.copy()
                #print('temp_win_check')
                #display(temp_win_check)
                temp_win_check[direct_win] = computer
                #print('temp_win_check')
                #display(temp_win_check)
                if (check_win(temp_win_check)):
                    #chess_board[move] = computer
                    #print('direct_win:' , move)
                    return move
        
            for direct_lose in Available_move_whole_chess:
                temp_chess = chess_board.copy()
                temp_chess[direct_lose] = user
                if (check_win(temp_chess)):
                    #print('move:' , move)
                    return direct_lose
            
            return i
    '''
    '''
    for i in range(len(move_score)):
        if (abs(move_score[i]) == 10000):
            #print('Available_move_whole_chess:' , Available_move_whole_chess)
            for return_win in Available_move_whole_chess:
                #print('direct_win:' , direct_win)
                #print('chess_board')
                #display(chess_board)
                temp_win_check = chess_board.copy()
                #print('temp_win_check')
                #display(temp_win_check)
                temp_win_check[return_win] = computer
                #print('temp_win_check')
                #display(temp_win_check)
                if (check_win(temp_win_check)):
                    #print('direct_win:' , direct_win)
                    return return_win

            for return_loss in Available_move_whole_chess:
                temp_loss_check = chess_board.copy()
                temp_loss_check[return_loss] = user
                if (check_win(temp_loss_check)):
                    return return_loss
        
    
    for i in range(len(move_score)):
        if (abs(move_score[i]) == 10000 and move_score[i] == -10000):
            return i
    '''
    '''
    for i in range(len(move_score)):
        if (move_score[i] > max_ and move_score[i] != 0):
            max_ = move_score[i]
            index = i
        elif(sum(move_score) == 0):
            return None 
    '''


    if not move_score:
        return None
    if user == 1:
        index = max(move_score, key = move_score.get)
    else:
        index = min(move_score, key = move_score.get)
    return index




def play_a_new_game():
    print("**      Tic-Tac-Toe      **")
    print("\n")
    
    print("Please choose whether you play in \"o\" (choose 1 and play first) or \"x\" (choose 2) : " , end = '')
    user_decision = input()
    while user_decision.isdigit() == False:
        print("Please enter a numer!!!!!!!!!")
        print("Enter again: " , end = '')
        user_decision = input()
    user_decision = int(user_decision)    
    #user_decision = 2
    while user_decision != 1 and user_decision != 2:
        print("Error , Please enter the correct number! : " , end = '')
        user_decision = int(input())
    

    chess = [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]

    if user_decision == 1:
        for i in range(5):
            
            player_decision = input("player please enter the step: ")
            while player_decision.isdigit() == False:
                print("Please enter a numer!!!!!!!!!")
                print("Enter again: " , end = '')
                player_decision = input()
            player_decision = int(player_decision)
            while player_decision > 9 or player_decision < 1:
                print("\nPlease enter number between 1-9!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                player_decision = int(input("player please enter the step: "))
            
            if chess[player_decision - 1] != 0:
                print("Error , Already has the \"o\" on it ")
            while chess[player_decision - 1] != 0:
                print("Re-enter your decision: ")
                player_decision = int(input("player please enter the step: "))
            chess[player_decision - 1] = 1
            display(chess)
            if (check_win(chess)):
                print("Player win!")
                return 
                break
            
            
            compute_think = Pure_Monte_Carlo_Tree_Search(chess , 1)
            if compute_think == None:
                break
            chess[compute_think] = 2
            display(chess)
            if (check_win(chess)):
                print("compute win!")
                return 
                break
            
            '''
            compute_think = Pure_Monte_Carlo_Tree_Search(chess , 2)
            if compute_think == None:
                break
            chess[compute_think] = 1
            display(chess)
            if (check_win(chess)):
                print("compute win!")
                return 
                break
            '''
            
    else:
        for i in range(5):
            compute_think = Pure_Monte_Carlo_Tree_Search(chess , 2)
            if compute_think == None:
                return 
                break
            chess[compute_think] = 1
            display(chess)
            if (check_win(chess)):
                for j in chess:
                    if chess[j] == 0:
                        chess[j] = 1
                print("compute win!")
                return 
                break
            
            count = 0
            for i in range(len(chess)):
                if (chess[i] == 0):
                    count += 1
            if (count == 0):
                print("It's draw!!!!!!!!")
                return 



            '''
            compute_think = Pure_Monte_Carlo_Tree_Search(chess , 1)
            if compute_think == None:
                return 
                break
            chess[compute_think] = 2
            display(chess)
            if (check_win(chess)):
                for j in chess:
                    if chess[j] == 0:
                        chess[j] = 2
                print("compute win!")
                return 
                break
            '''
            
            
            player_decision = input("player please enter the step: ")
            while player_decision.isdigit() == False:
                print("Please enter a numer!!!!!!!!!")
                print("Enter again: " , end = '')
                player_decision = input()
            player_decision = int(player_decision)
            while player_decision > 9 or player_decision < 1:
                print("\nPlease enter number between 1-9!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                player_decision = int(input("player please enter the step: "))
                
            if chess[player_decision - 1] != 0:
                print("Error , Already has the \"x\" on it ")
            while chess[player_decision - 1] != 0:
                print("Re-enter your decision: ")
                player_decision = int(input("player please enter the step: "))
            chess[player_decision - 1] = 2
            display(chess)
            if (check_win(chess)):
                print("Player win!")
                return 
                break
            
    
    print("It's draw!!!!!!!!")


if __name__ == "__main__":
    play_a_new_game()






























    




















