import random
import math
import os
import time 


def rand_graph(number_node , probability):

    # The empty dictionary
    graph_dic = {}
    # set the default value -> empty list to dictionary 
    for i in range(number_node):
        graph_dic.setdefault(i+1 , [])


    for i in range(1, number_node):             # Because j reached number_node - 1, i is no necessary touch the number_node - 1, modify for minisat problem 
        for j in range(i , number_node + 1):
            if i != j:                          # same thing like i + 1
                r = random.random()
                if r <= probability:            # if the random number(0 , 1) fall in given probability, we assigned each other
                    graph_dic.setdefault(i , []).append(j)
                    graph_dic.setdefault(j , []).append(i)

    return graph_dic



# given a list, only one variable can exist in the list
# For example A B C   ->  -A -B 0
#                         -A -C 0
#                         -B -C 0
#                         A B C 0
def exactly_one(info_list , filename = "output_icebreaker.txt"):
    file = open(filename , "a+")
    length = len(info_list)

    for i in range(length):
        for j in range(i+1 , length):
            # print(info_list[i] * -1 , info_list[j] * -1 , 0)              # Debug

            # write in file 
            file.write(str(info_list[i] * -1))
            file.write(' ')
            file.write(str(info_list[j] * -1))
            file.write(' ')
            file.write(str(0))
            file.write('\n')

    # write A B C 0
    for i in range(length):
        # print(info_list[i] , end='')                                      # Debug
        file.write(str(info_list[i]))
        file.write(' ')
        # print(' ' , end='')                                               # Debug

    # print(0)                                                              # Debug
    file.write(str(0))
    file.write('\n')

    file.close()



# k teams and n people in one team, total k * n variable
# [[1,2,3,4]
#  [1,2,3,4]
#  [1,2,3,4]]
# k for 3 and n for 4 
def make_friend_list(graph , k):
    # print(graph)                                                      # Debug
    length = len(graph)

    graph_list = []
    
    # itev = 1
    for i in range(k):
        n_list = []
        for j in range(1 , length + 1):
            n_list.append(j)
            # itev += 1

        graph_list.append(n_list)
    return graph_list


'''
graph_ = rand_graph(100 , 0.1)
b = make_friend_list(graph_, 10)                                    # Debug
print(b)
'''



# Each column must have one and only one people in it and so make a list for function exactly_one
# [[1 , 101 , 201 .... 901]  ... [901 , 902 , ... , 909] ]
def make_exactly_column_group(graph, k):
    length = len(graph)

    column_list = []
    for i in range(length):
        append_list = []
        for j in range(i + 1 , k * length + 1, length):
            append_list.append(j)

        column_list.append(append_list)
    
    return column_list



'''
graph_ = rand_graph(100 , 0.1)
a = make_exactly_column_group(graph_, 10)                           # Debug
print(a)
'''





def check_constrain(graph , get_list , times_n , filename = "output_icebreaker.txt"):
    file = open(filename , "a+")
    
    cluster = 0
    for item in get_list:
        # print('----------------------------' , item)
        temp_friend = graph[item]
        # print(item)
        for j in get_list:
            for item_friend in temp_friend:
                if j == item_friend and item <= item_friend:
                    cluster += 2

                    # print( (item + times_n ) * -1  ,  (item_friend + times_n ) * -1 , 0)
                    file.write(str((item + times_n ) * -1))
                    file.write(' ')
                    file.write(str( (item_friend + times_n ) * -1) )
                    file.write(' ')
                    file.write(str(0))
                    file.write('\n')

    file.close()
                    
    return cluster 





def calculate_clause(graph , get_list):
    cluster = 0
    for item in get_list:
        temp_friend = graph[item]
        for j in get_list:
            for item_friend in temp_friend:
                if j == item_friend and item <= item_friend:
                    cluster += 1
    return cluster 






def make_ice_breaker_sat(graph , k):
    file = open("output_icebreaker.txt" , "w")
    total_cluster = 0
    length = len(graph)
    sol_graph = make_friend_list(graph , k)
    exactly_one_graph = make_exactly_column_group(graph , k)

    #print(sol_graph)                                         # Debug
    #print('\n')                                              # Debug
    #print(exactly_one_graph)                                 # Debug

    for i in range(k):
        total_cluster += calculate_clause(graph , sol_graph[i])

    total_cluster += int ( ( k * (k - 1) / 2 + 1 ) * length ) 
    
    # print('c' , str(length) + '-ice_breaker' , 'problem')
    file.write('c ')
    file.write(str(length))
    file.write('-ice_breaker problem')
    file.write('\n')

    # print('p' , 'cnf' , length * k , total_cluster)
    file.write('p cnf ')
    file.write(str(length * k))
    file.write(' ')
    file.write(str(total_cluster))
    file.write('\n')
    file.close()
    
    for i in range(k):
        times_n = i * length
        total_cluster += check_constrain(graph , sol_graph[i] , times_n)


    for i in range(length):
        exactly_one(exactly_one_graph[i])
    file.close()
    
    to_string_file = open("output_icebreaker.txt" , "r")
    string = to_string_file.read()
    to_string_file.close()
    return string 




def check_satisfiable(file_name):
    file = open(file_name , "r")
    f = file.readlines()
    for sat in f:
        if sat == "SAT\n":
            return True
        else:
            return False






def convert_sol_to_string(file_name):
    '''
    Transfer the solution to string , help function for draw_queen_sat_sol()
    '''
    file_convert = open(file_name , "r")
    string_sol = ""
    for word in file_convert:
            string_sol += word

    file_convert.close()
    return string_sol






def find_min_teams(graph):

    for i in range(1 , len(graph) + 1):
        print("Now testing... k =" , i)
        make_ice_breaker_sat(graph , i)

        os.system('minisat output_icebreaker.txt out_ice_breaker')

        sol = convert_sol_to_string("out_ice_breaker")
        # print(sol)

        
        if sol == "UNSAT\n":
            continue
        
        else:
            for word in sol.split():
                if word != "SAT" and word != 0:
                    if abs(int(word)) == int(word):
                        return i

            
        

if __name__ == "__main__":
    number_of_N = int(input("Please enter the number of N: "))
    p = float(input("Please enter the probability: "))
    for i in range(10):
        graph_ = rand_graph(number_of_N , p)
        # print(graph_)
        start_time = time.time()
        a = find_min_teams(graph_)
        elapsed_time = time.time() - start_time
        
        print(a , "minimum number of teams")
        print(elapsed_time , "time to find minimum teams")

    # string = make_ice_breaker_sat(rand_graph(10 , 0.1) , 3)
    # print(string )
    '''
    graph_ = rand_graph(30 , 0.1)
    # print('----------------------------------' , graph_)
    file = open("output_icebreaker.txt" , "w")

    # g={0: [7, 22, 24, 28, 32, 35, 42, 49, 54, 68, 88, 99], 1: [5, 7, 24, 42, 47, 62, 71, 95], 2: [6, 11, 12, 21, 25, 32, 36, 48, 55, 75, 79, 86], 3: [8, 31, 47, 59, 73, 80, 84, 90, 93, 96], 4: [10, 11, 29, 42, 63, 71, 74, 94], 5: [1, 18, 26, 55, 58, 67, 69, 74, 75, 85, 90, 96, 98], 6: [2, 10, 14, 26, 30, 49, 54, 79, 94], 7: [0, 1, 22, 27, 39, 40, 52, 58, 68, 69, 72, 82, 99], 8: [3, 20, 27, 69, 72, 76, 80, 91], 9: [25, 38, 41, 56, 57, 58, 59, 69, 71, 99], 10: [4, 6, 17, 21, 25, 45, 50, 61, 64, 78], 11: [2, 4, 28, 52, 82], 12: [2, 14, 32, 42, 52, 73, 75, 82], 13: [18, 32, 45, 46, 48, 50, 54, 72, 85, 90, 93], 14: [6, 12, 18, 30, 31, 40, 54, 56, 63, 69, 72, 75, 78, 79, 90, 99], 15: [29, 48, 51, 53, 68, 86, 90, 91, 97], 16: [38, 52, 56, 77, 78, 82, 84, 89, 95, 97], 17: [10, 23, 24, 27, 28, 30, 35, 43, 45, 55, 88, 92, 95, 97], 18: [5, 13, 14, 22, 23, 36, 64, 68, 70, 71, 89], 19: [20, 21, 28, 30, 31, 35, 44, 45, 49, 62, 76, 78, 83], 20: [8, 19, 25, 30, 31, 44, 48, 74, 93, 96], 21: [2, 10, 19, 38, 46, 70, 72, 78, 95, 99], 22: [0, 7, 18, 52, 55, 74, 80, 85, 92, 96, 99], 23: [17, 18, 39, 47, 65, 73, 88, 90, 96], 24: [0, 1, 17, 26, 30, 39, 41, 66, 85], 25: [2, 9, 10, 20, 27, 28, 42, 43, 68, 82, 94, 97], 26: [5, 6, 24, 47, 52, 64, 69, 88, 91, 99], 27: [7, 8, 17, 25, 35, 44, 49, 51, 53, 58, 63, 73, 74, 76, 80, 88, 90, 92, 94], 28: [0, 11, 17, 19, 25, 35, 47, 52, 55, 57, 62, 92], 29: [4, 15, 39, 44, 51, 71], 30: [6, 14, 17, 19, 20, 24, 43, 55, 58, 65, 71, 77, 87, 90], 31: [3, 14, 19, 20, 39, 43, 51, 74, 77, 80, 82], 32: [0, 2, 12, 13, 78, 80, 84, 89], 33: [37, 38, 39, 47, 53, 64, 77], 34: [39, 41, 60, 74, 83, 88], 35: [0, 17, 19, 27, 28, 37, 42, 70, 87, 88], 36: [2, 18, 40, 50, 66, 72, 73, 76, 81], 37: [33, 35, 66, 84], 38: [9, 16, 21, 33, 56, 87], 39: [7, 23, 24, 29, 31, 33, 34, 50, 59, 61, 67, 69, 73, 75, 92], 40: [7, 14, 36, 62, 71, 77, 80, 97], 41: [9, 24, 34, 50, 69, 72, 74, 76], 42: [0, 1, 4, 12, 25, 35, 55, 70, 94, 96], 43: [17, 25, 30, 31, 52, 53, 75, 93, 94, 98], 44: [19, 20, 27, 29, 57, 65, 69, 75, 93], 45: [10, 13, 17, 19, 47, 48, 50, 58, 81, 87, 88, 92, 94, 97], 46: [13, 21, 47, 48, 56, 64, 68, 70, 72, 83, 92], 47: [1, 3, 23, 26, 28, 33, 45, 46, 65, 74, 93], 48: [2, 13, 15, 20, 45, 46, 50, 54, 57, 62, 64, 74], 49: [0, 6, 19, 27, 56, 79, 84, 91, 94], 50: [10, 13, 36, 39, 41, 45, 48, 51, 75, 86], 51: [15, 27, 29, 31, 50, 55, 61, 65], 52: [7, 11, 12, 16, 22, 26, 28, 43, 65, 70, 75], 53: [15, 27, 33, 43, 55, 78, 88, 91, 96], 54: [0, 6, 13, 14, 48, 63, 82, 84], 55: [2, 5, 17, 22, 28, 30, 42, 51, 53, 62, 65, 67, 76, 77, 88, 99], 56: [9, 14, 16, 38, 46, 49, 62, 66, 75, 94, 97], 57: [9, 28, 44, 48, 67, 68, 74, 79, 84, 90, 95, 98], 58: [5, 7, 9, 27, 30, 45, 78, 85], 59: [3, 9, 39, 64, 86, 94, 98], 60: [34, 74, 97, 98, 99], 61: [10, 39, 51, 72, 83], 62: [1, 19, 28, 40, 48, 55, 56, 70, 71, 87, 90, 95, 97, 98], 63: [4, 14, 27, 54, 71, 75, 86, 95], 64: [10, 18, 26, 33, 46, 48, 59, 65, 69, 76, 90, 91], 65: [23, 30, 44, 47, 51, 52, 55, 64, 79, 86], 66: [24, 36, 37, 56, 77, 82, 91], 67: [5, 39, 55, 57, 77, 95], 68: [0, 7, 15, 18, 25, 46, 57, 73, 77, 81, 96, 99], 69: [5, 7, 8, 9, 14, 26, 39, 41, 44, 64, 78], 70: [18, 21, 35, 42, 46, 52, 62, 71], 71: [1, 4, 9, 18, 29, 30, 40, 62, 63, 70, 75, 88], 72: [7, 8, 13, 14, 21, 36, 41, 46, 61, 73, 94, 99], 73: [3, 12, 23, 27, 36, 39, 68, 72, 78, 81, 83, 85], 74: [4, 5, 20, 22, 27, 31, 34, 41, 47, 48, 57, 60, 82, 84, 97], 75: [2, 5, 12, 14, 39, 43, 44, 50, 52, 56, 63, 71, 82, 83, 84, 90, 92], 76: [8, 19, 27, 36, 41, 55, 64, 81], 77: [16, 30, 31, 33, 40, 55, 66, 67, 68, 78, 91, 93], 78: [10, 14, 16, 19, 21, 32, 53, 58, 69, 73, 77, 84, 88], 79: [2, 6, 14, 49, 57, 65, 81, 89, 90, 92, 97], 80: [3, 8, 22, 27, 31, 32, 40, 83, 88, 96], 81: [36, 45, 68, 73, 76, 79], 82: [7, 11, 12, 16, 25, 31, 54, 66, 74, 75, 89, 95, 99], 83: [19, 34, 46, 61, 73, 75, 80], 84: [3, 16, 32, 37, 49, 54, 57, 74, 75, 78, 86, 89, 93, 99], 85: [5, 13, 22, 24, 58, 73], 86: [2, 15, 50, 59, 63, 65, 84], 87: [30, 35, 38, 45, 62, 92], 88: [0, 17, 23, 26, 27, 34, 35, 45, 53, 55, 71, 78, 80, 94], 89: [16, 18, 32, 79, 82, 84, 90, 91, 96], 90: [3, 5, 13, 14, 15, 23, 27, 30, 57, 62, 64, 75, 79, 89], 91: [8, 15, 26, 49, 53, 64, 66, 77, 89, 92, 95], 92: [17, 22, 27, 28, 39, 45, 46, 75, 79, 87, 91, 97, 99], 93: [3, 13, 20, 43, 44, 47, 77, 84], 94: [4, 6, 25, 27, 42, 43, 45, 49, 56, 59, 72, 88], 95: [1, 16, 17, 21, 57, 62, 63, 67, 82, 91], 96: [3, 5, 20, 22, 23, 42, 53, 68, 80, 89], 97: [15, 16, 17, 25, 40, 45, 56, 60, 62, 74, 79, 92, 98], 98: [5, 43, 57, 59, 60, 62, 97], 99: [0, 7, 9, 14, 21, 22, 26, 55, 60, 68, 72, 82, 84, 92]}
    # graph_an = {}

    # print(g)
    #for i in range(100):
    #    graph_an.setdefault(i+1 , [])


    
    for i in range(100):
        graph_an.setdefault(i+1 , g[i])
        
    for i in range(1 , 101):
        temp_list = graph_an[i]
        length = len(temp_list)
        for j in range(length):
            temp_list[j] = temp_list[j] + 1
        # print('--------' , temp_list)
        graph_an[i] = temp_list
    

    
    # print('\n')
    # print('graph an-------------------------------------------------' , graph_an)
    
    make_ice_breaker_sat(graph_ , 10)
    
    file.close()
    '''


























