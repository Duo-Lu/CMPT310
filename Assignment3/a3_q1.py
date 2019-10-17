import os
import math


def calculate_clause(N):
    number = 0
    number += N * (N - 1) * N + 2 * N

    dig_number = 0
    n = N
    while n >= 2:
        i = n * (n - 1) / 2
        dig_number += i
        n -= 1

    n = N - 1
    while n >= 2:
        i = n * (n - 1) / 2
        dig_number += i
        n -= 1

    dig_number = dig_number * 2

    return int(number + dig_number)


    
def make_n_queen_row(N):
    queen_list = []
    row_list = []
    row = 0
    col = 0
    for row in range(N * N):
        row_list.append(row + 1)
        if (row+1) % N == 0 and row != 0:
            queen_list.append(row_list)
            row_list = []

    return queen_list




def make_n_queen_col(N):
    queen_list = []
    row_list = []
    for row in range(N):
        row_list = []
        for col in range(N * N):
            if col % N == row:
                row_list.append(col + 1)
        queen_list.append(row_list)

    return queen_list




def make_n_queen_dig(N):
    row_list = make_n_queen_row(N)[0]
    col_list_org = make_n_queen_col(N)[0]
    col_list_last = make_n_queen_col(N)[N-1]
    del col_list_org[-1]
    del col_list_org[0]
    del col_list_last[-1]
    del col_list_last[0]
    col_list_last = col_list_last[::-1]
    
    
    queen_list = []
    for i in range(N - 1):
        row_list = []
        for j in range(i+1 , N * N + 1  , N + 1):
            if len(row_list) >= N - i:
                break
            row_list.append(j)
            
        queen_list.append(row_list)

    for item in col_list_org:
        col_list = []
        for j in range(item , N * N , N + 1):
            col_list.append(j)

        queen_list.append(col_list)
    
    i = N
    while i > 1:
        i -= 1
        row_list = []
        for j in range(i+1 , N * N + 1  , N - 1):
            if len(row_list) >= i + 1:
                break
            row_list.append(j)
            
        queen_list.append(row_list)

    for item in col_list_last:
        col_list = []
        for j in range(item , N * N , N - 1):
            col_list.append(j)

        queen_list.append(col_list)

            
    return queen_list
    




def exactly_one(info_list , filename = "output.txt"):
    file = open(filename , 'a+')
    length = len(info_list)
    
    # print(info_list)
    
    for i in range(length):
        for j in range(i+1 , length):
            # print(info_list[i] * -1 , info_list[j] * -1 , 0)      # DEBUG
        
            file.write(str(info_list[i] * -1))
            file.write(' ')
            file.write(str(info_list[j] * -1))
            file.write(' ')
            file.write(str(0))
            file.write('\n')
            

    for i in range(length):
        # print(info_list[i] , end='')                              # DEBUG
        file.write(str(info_list[i]))
        file.write(' ')
        # print(' ' , end='')                                       # DEBUG

    # print(0)                                                      # DEBUG
    file.write(str(0))
    file.write('\n')

    file.close()





def at_most_one(info_list , filename = "output.txt"):
    file = open(filename , "a+")
    length = len(info_list)

    for i in range(length):
        for j in range(i+1 , length):
            # print(info_list[i] * -1 , info_list[j] * -1 , 0)
            
            file.write(str(info_list[i] * -1))
            file.write(' ')
            file.write(str(info_list[j] * -1))
            file.write(' ')
            file.write(str(0))
            file.write('\n')
    file.close()




    
def make_queen_sat(N):
    file = open("output.txt" , "w")
    variable = N * N
    clause = calculate_clause(N)        # calculate the number of clause
    # print("Number of clause" , clause)
    # print('c' , str(N) + '-queens' , 'problem')           DEBUG
    
    file.write('c ')
    file.write(str(N))
    file.write('-queens problem')
    file.write('\n')
    
    # print('p' , 'cnf' , variable , clause)                DEBUG
    
    file.write('p cnf ')
    file.write(str(variable))
    file.write(' ')
    file.write(str(clause))
    file.write('\n')
    file.close()

    row_queen = make_n_queen_row(N)     # make a 2-D array for rows
    col_queen = make_n_queen_col(N)     # make a 2-D array for columns
    dig_queen = make_n_queen_dig(N)     # make a 2-D array for digs
    # print(row_queen)
    # print(col_queen)
    # print(dig_queen)
    for item in row_queen:          
        exactly_one(item)   


    for item in col_queen:
        exactly_one(item)


    for item in dig_queen:
        at_most_one(item)


    to_string_file = open("output.txt" , "r")
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






def draw_queen_sat_sol(sol):
    info_sol = ""
    check_word = "UNSAT"
    if check_word in sol:
        print("no solution")
        return False

    last_word = ""
    for word in sol.split():
        if word != "SAT" and word != '0':
            # print(word)               # DEBUG
            info_sol += word
            info_sol += ' '
            last_word = word 

    # print(info_sol)                   # DEBUG
    # print("------------" , last_word) # DEBUG

    # Remember when to switch the line 
    switch_line_num = int(math.sqrt(abs(int(last_word))))
    
    if switch_line_num > 40:
        print("too big: N must be less than 40")
        return
    
    count = 0
    for word in info_sol.split():
        if count % switch_line_num == 0 and count != 0:      # code for switch the line
            print('\n' , end = '')   
            print('\n' , end = '' , file = file_sol)         # file = file_sol to write into solution.txt                
        count += 1
        if abs(int(word)) != int(word):                      # if the number is negative , print dot 
            print('. ' , end = '')
            print('. ' , end = '' , file = file_sol)
        else:
            print('Q ' , end = '')
            print('Q ' , end = '' , file = file_sol)

    print("\n")
        


        
'''
check = convert_sol_to_string("out")      DEBUG
draw_queen_sat_sol(check)                 
'''




if __name__ == "__main__":
    # file = open("output.txt" , "w")

    # user input the number
    number_queens = 0
    print("Please enter the numbers of queens: " , end = '')
    number_queens = int(input())

    # to make cluase and output the text file
    string_output = make_queen_sat(number_queens)
    print(string_output)

    # file.close()
    
    # automaticaly run the minisat use the os.system
    os.system('minisat output.txt out')

    # open the file for display the solution 
    file_sol = open("queens_solution.txt" , "w")

    check = convert_sol_to_string("out")
    # print(check)                          # DEBUG
    draw_queen_sat_sol(check)

    file_sol.close()
    











