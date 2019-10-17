import random
from search import *
import time


class EightPuzzle(Problem):

    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """
 
    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)
    
    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)
    
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """
        
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']       
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i+1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j]!= 0:
                    inversion += 1
        
        return inversion % 2 == 0
    
    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """
        # Don't include zero. The heuristic function never ever overestimate the true cost
        # but the default one does

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))


# Question 1: Helper Functions

def make_rand_8puzzle():
    import random
    
    state = [0,1,2,3,4,5,6,7,8]                     # default states
    
    random.shuffle(state)                           # random shuffle the states

    Eight_Puzzle = EightPuzzle(tuple(state))        
    while(Eight_Puzzle.check_solvability(state) == False):      # check solvability 
            random.shuffle(state)                   
            Eight_Puzzle = EightPuzzle(tuple(state))            # Eight_Puzzle is actually a object 

    
    return Eight_Puzzle




def display(state):
    i = 0

    for i in range(0,9):
        if state[i] == 0:
            print('*' , end = '')
            if (i+1) % 3 == 0:
                print('\n' , end = '')
            else:
                print(' ', end = '')
        else:
            print(state[i] , end = '')
            if (i+1) % 3 == 0:
                print('\n' , end = '')
            else:
                print(' ', end = '')
            





#******************************************************************************************************************




def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    total_pop = 0
    while frontier:
        node = frontier.pop()
        total_pop = total_pop + 1                # count how many element pop from frontier
        if problem.goal_test(node.state):
            return node, total_pop
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None, total_pop


def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


# https://www.andrew.cmu.edu/course/15-121/labs/HW-7%20Slide%20Puzzle/lab.html
def manhattan(node):
    state = node.state
    index_goal = {0:[2,2], 1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1]}
    index_state = {}
    index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    x, y = 0, 0
    
    for i in range(len(state)):
        index_state[state[i]] = index[i]
    
    mhd = 0

    # Don't include zero. The heuristic function never ever overestimate the true cost
    # but the default one does
    for i in range(1,9):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
    
    return mhd






# Question 2: Comparing Algorithms
# max of misplaced tile and Manhattan distance 
def max_h_manhattan(node):
    puzzle8 =  EightPuzzle(node.state)
    return max(manhattan(node) , puzzle8.h(node))

def running_time_test_8puzzle():

    eight_puzzle = make_rand_8puzzle()
    manh_astar = eight_puzzle
    max_of_both = eight_puzzle
    
    display(eight_puzzle.initial)
    start_time = time.time()
    result_astar , total_pop = astar_search(eight_puzzle)
    elapsed_time = time.time() - start_time

    print('A*-search using the misplaced tile heuristic')
    print(result_astar.solution())
    print('The length of solution is' , len(result_astar.solution()))
    print('The total number of pop is' , total_pop)
    print(f'The elapsed time (in seconds): {elapsed_time}')

    
    display(manh_astar.initial)
    start_time_manh = time.time()
    result_astar_man , total_pop_man = astar_search(manh_astar , h = manhattan)
    elapsed_time_manh = time.time() - start_time_manh

    print('A*-search using manhattan heuristic')
    print(result_astar_man.solution())
    print('The length of solution is' , len(result_astar_man.solution()))
    print('The total number of pop is' , total_pop_man)
    print(f'The elapsed time (in seconds): {elapsed_time_manh}')

    display(max_of_both.initial)
    start_time_max = time.time()
    result_astar_max , total_pop_max = astar_search(max_of_both, h = max_h_manhattan)
    elapsed_time_max = time.time() - start_time_max

    print('A*-search using the max of both heuristic')
    print(result_astar_max.solution())
    print('The length of solution is' , len(result_astar_max.solution()))
    print('The total number of pop is' , total_pop_max)
    print(f'The elapsed time (in seconds): {elapsed_time_max}')

def running_time_test_8puzzle_ten_time():
    for i in range(10):
        print('The' , i+1, 'times')
        running_time_test_8puzzle()

running_time_test_8puzzle_ten_time()


#******************************************************************************************************************

# Question 3: The Y-Puzzle
# Name of class Y puzzle is YPuzzle 
class YPuzzle(Problem):

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """

        self.goal = goal
        Problem.__init__(self, initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)


    def actions(self, state):
        
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """


        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 1:
            possible_actions.remove('UP')
            possible_actions.remove('RIGHT')
            possible_actions.remove('LEFT')
        if index_blank_square == 2:
            possible_actions.remove('LEFT')
        if index_blank_square == 3:
            possible_actions.remove('UP')
        if index_blank_square == 4:
            possible_actions.remove('RIGHT')
        if index_blank_square == 5:
            possible_actions.remove('LEFT')
            possible_actions.remove('DOWN')
        if index_blank_square == 7:
            possible_actions.remove('DOWN')
            possible_actions.remove('RIGHT')
        if index_blank_square == 8:
            possible_actions.remove('RIGHT')
            possible_actions.remove('DOWN')
            possible_actions.remove('LEFT')

        return possible_actions


    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank == 0:
            neighbor = blank + 2
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 1:
            neighbor = blank + 3
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 2:
            delta = {'UP':-2, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 3:  # unchange
            delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 4:  # unchange
            delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 5:  # unchange
            delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 6:
            delta = {'UP':-3, 'DOWN':2, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 7:  # unchange
            delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
        if blank == 8:
            delta = {'UP':-2, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
            neighbor = blank + delta[action]
            new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)


    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g and s != 0 for (s, g) in zip(node.state, self.goal))


    def check_solvability(self , state):
        """ Checks if the given state is solvable """

        blank = self.find_blank_square(state)

        if blank == 0:                                              # star in left unper situation 
            if state[1] != 2 or state[2] != 1 or state[8] != 7:     # 2 in index[1] , 1 in index[2] , 7 in index[8]
                return False
            inversion_blank_zero = 0
            for i in range(2,8):
                for j in range(i+1 , 8):
                    if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                        inversion_blank_zero += 1
            return inversion_blank_zero % 2 == 0

        if blank == 1:
            if state[0] != 1 or state[4] != 2 or state[8] != 7:
                return False
            inversion_blank_one = 0
            for i in range(2,8):
                for j in range(i+1, 8):
                    if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                        inversion_blank_one += 1
            return inversion_blank_one % 2 == 0


        if blank == 8:
            if state[0] != 1 or state[1] != 2 or state[6] != 7:
                return False
            inversion_blank_eight = 0
            for i in range(2, 8):
                for j in range(i+1, len(state)):
                    if (state[i] > state[j]) and state[i] not in [0, 7] and state[j] not in [0, 7]:
                        inversion_blank_eight += 1
            return inversion_blank_eight % 2 == 0

        if blank in range(2,8):
            if state[0] != 1 or state[1] != 2 or state[8] != 7:
                return False
            inversion = 0
            for i in range(2,8):
                for j in range(i+1 , 8):
                    if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                        inversion += 1
            return inversion % 2 == 0
        


def make_rand_Ypuzzle():
    import random
    
    state = [0,1,2,3,4,5,6,7,8]
    random.shuffle(state)

    Eight_Y_obj = YPuzzle(tuple(state))
    while(Eight_Y_obj.check_solvability(state) == False):
        random.shuffle(state)
        Eight_Y_obj = YPuzzle(tuple(state))
        
    return Eight_Y_obj


    
def display_Y(state):
    for i in range(9):
        if state[i] == 0:
            state[i] = '*'

    print(state[0], ' ', end = '')
    print(' ' , end = '')
    print(state[1])
    print(state[2], '', end = '')
    print(state[3], '', end = '')
    print(state[4])
    print(state[5], '', end = '')
    print(state[6], '', end = '')
    print(state[7])
    print('  ' , end = '')
    print(state[8], '', end = '')




#******************************************************************************************************************




# https://www.andrew.cmu.edu/course/15-121/labs/HW-7%20Slide%20Puzzle/lab.html
def manhattan_Ypuzzle(node):
    state = node.state
    index_goal = {0:[3,1], 1:[0,0], 2:[0,2], 3:[1,0], 4:[1,1], 5:[1,2], 6:[2,0], 7:[2,1], 8:[2,2]}
    index_state = {}
    index = [[0,0], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2], [3,1]]
    x, y = 0, 0
    
    for i in range(len(state)):
        index_state[state[i]] = index[i]
    
    mhd = 0


    for i in range(1,9):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd
    
    return mhd


# max of default h() fuction and manhattan h() function
def max_h_manhattan_Ypuzzle(node):
    puzzle8 =  YPuzzle(node.state)
    return max(manhattan_Ypuzzle(node) , puzzle8.h(node))



def f_default_Ypuzzle():
    
    solve_Ypuzzle = make_rand_Ypuzzle()
    
    
    start_time = time.time()
    result_Y , total_pop_Y = astar_search(solve_Ypuzzle)
    elapsed_time = time.time() - start_time

    display(solve_Ypuzzle.initial)

    print('Y_puzzle using the misplaced tile heuristic')
    print(result_Y.solution())
    print('The length of solution is' , len(result_Y.solution()))
    print('The total number of pop is' , total_pop_Y)
    print(f'The elapsed time (in seconds): {elapsed_time}')

    display(solve_Ypuzzle.initial)
    
    start_time_manh = time.time()
    result_manh_Y , total_pop_manh_Y = astar_search(solve_Ypuzzle , h = manhattan_Ypuzzle)
    elapsed_time_manh = time.time() - start_time_manh
    print('Y_puzzle using the manhattan heuristic')
    print(result_manh_Y.solution())
    print('The length of solution is' , len(result_manh_Y.solution()))
    print('The total number of pop is' , total_pop_manh_Y)
    print(f'The elapsed time (in seconds): {elapsed_time_manh}')

    display(solve_Ypuzzle.initial)
    
    start_time_max = time.time()
    result_manh_Y_max , total_pop_manh_Y_max = astar_search(solve_Ypuzzle , h = max_h_manhattan_Ypuzzle)
    elapsed_time_max = time.time() - start_time_max
    print('Y_puzzle using the max of both heuristic')
    print(result_manh_Y_max.solution())
    print('The length of solution is' , len(result_manh_Y_max.solution()))
    print('The total number of pop is' , total_pop_manh_Y_max)
    print(f'The elapsed time (in seconds): {elapsed_time_max}')

def running_ten_times_Y():
    for i in range(10):
        print('The' , i+1, 'times')
        f_default_Ypuzzle()


running_ten_times_Y()


    
'''
default_astar = make_rand_8puzzle()
manh_astar = default_astar
max_of_h_manhattan = default_astar

display(default_astar.initial)

result_default_astar , default_total_pop = astar_search(default_astar)
print(result_default_astar.solution())
print(default_total_pop)


result_manh_astar, manh_total_pop = astar_search(manh_astar, h = manhattan)
print(result_manh_astar.solution())
print(manh_total_pop)


def max_h_manhattan(node):
    puzzle8 =  EightPuzzle(node.state)
    return max(manhattan(node) , puzzle8.h(node))

result_max_h_manhattan , max_total_pop = astar_search(max_of_h_manhattan , h = max_h_manhattan)
print(result_max_h_manhattan.solution())
print(max_total_pop)
'''


'''
def f_default():
    start_time = time.time()

    default_astar = make_rand_8puzzle()
    display(default_astar.initial)
    result_default_astar , default_total_pop = astar_search(default_astar)
    elapsed_time = time.time() - start_time

    print('A*-search using the misplaced tile heuristic')
    print(result_default_astar.solution())
    print('The length of solution is' , len(result_default_astar.solution()))
    print('The total number of pop is' , default_total_pop)

    print(f'The elapsed time (in seconds): {elapsed_time}')

#f_default()

def f_Manhattan():
    start_time = time.time()

    state = [1,2,8,5,0,4,6,7,3]
    manh_astar = EightPuzzle(tuple(state))
    display(manh_astar.initial)
    result_manh_astar , manh_total_pop = astar_search(manh_astar , h = manhattan)
    elapsed_time = time.time() - start_time

    print('A*-search using the Manhattan distance heuristic')
    print(result_manh_astar.solution())
    print('The length of solution is' , len(result_manh_astar.solution()))
    print('The total number of pop is' , manh_total_pop)

    print(f'The elapsed time (in seconds): {elapsed_time}')

#f_Manhattan()
'''


'''
def f_default_Ypuzzle():
    start_time = time.time()

    solve_Ypuzzle = make_rand_Ypuzzle()
    result_Y , total_pop_Y = astar_search(solve_Ypuzzle)
    elapsed_time = time.time() - start_time

    print('Y_puzzle using the misplaced tile heuristic')
    print(result_Y.solution())
    print('The length of solution is' , len(result_Y.solution()))
    print('The total number of pop is' , total_pop_Y)

    print(f'The elapsed time (in seconds): {elapsed_time}')


def f_Manh_Ypuzzle():
    start_time = time.time()

    solve_Ypuzzle_manh = make_rand_Ypuzzle()
    result_manh_Y , total_pop_manh_Y = astar_search(solve_Ypuzzle_manh)
    elapsed_time = time.time() - start_time

    print('Y_puzzle using the misplaced tile heuristic')
    print(result_manh_Y.solution())
    print('The length of solution is' , len(result_manh_Y.solution()))
    print('The total number of pop is' , total_pop_manh_Y)

    print(f'The elapsed time (in seconds): {elapsed_time}')
'''


    

