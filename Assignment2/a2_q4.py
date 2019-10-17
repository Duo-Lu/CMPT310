from csp import *
from a2_q1 import *
from a2_q2 import *
from a2_q3 import *
import random
import time


# modify the CSP class
class CSP(search.Problem):
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b

    In the textbook and in most mathematical definitions, the
    constraints are specified as explicit pairs of allowable values,
    but the formulation here is easier to express and more compact for
    most cases. (For example, the n-Queens problem can be represented
    in O(n) space using this notation, instead of O(N^4) for the
    explicit representation.) In terms of describing the CSP as a
    problem, that's all there is.

    However, the class also supports data structures and methods that help you
    solve CSPs by calling a search function on the CSP. Methods and slots are
    as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        assign(var, val, a)     Assign a[var] = val; do other bookkeeping
        unassign(var, a)        Do del a[var], plus other bookkeeping
        nconflicts(var, val, a) Return the number of other variables that
                                conflict with var=val
        curr_domains[var]       Slot: remaining consistent values for var
                                Used by constraint propagation routines.
    The following methods are used only by graph_search and tree_search:
        actions(state)          Return a list of actions
        result(state, action)   Return a successor of state
        goal_test(state)        Return true if all constraints satisfied
    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation
    """

    def __init__(self, variables, domains, neighbors, constraints):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0
        self.nuassigns = 0              # extra attribute for remembering unassign
        self.total_conflict = 0         # extra attribute for remembering conflict 

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]
            self.nuassigns = self.nuassigns + 1     # same as assign, when function calls, increase the unassign

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""
        # Subclasses may implement this more efficiently
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        conflict = count(conflict(v) for v in self.neighbors[var])
        self.total_conflict = self.total_conflict + conflict            # update the total_conflict 
        return conflict

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        # Subclasses can print in a prettier way, or display with a GUI
        print('CSP:', self, 'with assignment:', assignment)

    # These methods are for the tree and graph-search interface:

    def actions(self, state):
        """Return a list of applicable actions: nonconflicting
        assignments to an unassigned variable."""
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        """Perform an action and return the new state."""
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    # These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

    # This is for min_conflicts search

    def conflicted_vars(self, current):
        """Return a list of variables in current assignment that are in conflict"""
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]




def min_conflicts(csp, max_steps=100000):
    """Solve a CSP by stochastic hillclimbing on the number of conflicts."""
    #-------------------------------------------------------------------------------------------------------------------------------
    # Generate a complete assignment for all variables (probably with conflicts)
    # The actually step is min_conflicts_value, find a group that contain minimum conflict. If there is more than one group that contain
    # same conflict , not random shuffle people into random group, that can get optimal solution. So put people into front group
    csp.current = current = {}
    for var in csp.variables:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    #-------------------------------------------------------------------------------------------------------------------------------
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            return current
        var = random.choice(conflicted)
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    return None


identity = lambda x: x




def min_conflicts_value(csp, var, current):
    """Return the value that will give var the least number of conflicts.
    If there is a tie, choose a team that already have people , rather than random shuffle"""
    return argmin_tie(csp.domains[var],
                             key=lambda val: csp.nconflicts(var, val, current))


def argmin_tie(seq, key=identity):
    """Return a minimum element of seq; break ties """
    # not random shuffle people in a random group 
    return min(seq, key=key)


# ______________________________________________________________________________
# CSP Local search



graphs = [rand_graph(100, 0.1), rand_graph(100, 0.2), rand_graph(100, 0.3),
          rand_graph(100, 0.4), rand_graph(100, 0.5)]




def run_q4_modify(graph_given):
    graph = graph_given

    variable = []
    domain = {}
    neighbors = graph
    
    for key in graph:                                        # make variable list
        variable.append(key)

    for i in range(len(variable)):
        domain.setdefault(i , variable)

    # key step
    #--------------------------------------------------------------------------------------
    csp_obj = CSP(variable , domain , neighbors , constraints)

    assignment = min_conflicts(csp_obj)

    number_people_divided = num_teams(assignment)
    #--------------------------------------------------------------------------------------

    # print(assignment)                                      # Debug remove before submit 

    # print('number_people_divided:' , number_people_divided)# Debug remove before submit 

    check = check_teams(graph , assignment)
    
    # print(check)                                           # Debug remove before submit 

    # print('total_conflict:' , csp_obj.total_conflict)      # Debug remove before submit

    total_number_of_assign = csp_obj.nassigns                # extra variable for remember 
    total_number_of_unassign = csp_obj.nuassigns

    total_number_conflict = csp_obj.total_conflict

    return assignment , number_people_divided , total_number_of_assign , total_number_of_unassign , total_number_conflict




# actual run step but not very important
# Just visualiztion the results 
def run_q4():

    assignment = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}
    number_people_divided = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}
    time_ = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}
    total_number_of_assign = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}
    total_number_of_unassign = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}
    total_number_conflict = {0:[] , 1:[] , 2:[] , 3:[] , 4:[]}


    for i in range(5):
        for j in range(5):
            graph = graphs[i]
            # print('graph:', graph)
            
            start_time = time.time()
            assignment_ , number_people_divided_ , total_number_of_assign_ , total_number_of_unassign_ , total_number_conflict_ = run_q4_modify(graph)
            elapsed_time = time.time() - start_time
            assignment[i].append(assignment_)
            number_people_divided[i].append(number_people_divided_)
            time_[i].append(elapsed_time)
            total_number_of_assign[i].append(total_number_of_assign_)
            total_number_of_unassign[i].append(total_number_of_unassign_)
            total_number_conflict[i].append(total_number_conflict_)


            print('________________________________________________________________________________________________')
            
            print('The assignment is (exactly min solution)' , assignment_)
            print('The number of teams that the people are divided into' , number_people_divided_)
            print('________________________________________________________________________________________________')

            print(f'elapsed time (in seconds): {elapsed_time}')

            print('The total number of times CSP variables were assigned' , total_number_of_assign_)
            print('The total number of times CSP variables were unassigned' , total_number_of_unassign_)
            
            print('The total number of conflict until you find the optimal solution' , total_number_conflict_)


    print('\n\n\n')
    print('The number of teams that the people are divided into')
    for i in range(5):
        print(number_people_divided[i])

    print('The running time')
    for i in range(5):
        print(time_[i])

    print('The total number of times CSP variables were assigned')
    for i in range(5):
        print(total_number_of_assign[i])

    print('The total number of times CSP variables were unassigned')
    for i in range(5):
        print(total_number_of_unassign[i])

    print('The total number of conflict until you find the optimal solution')
    for i in range(5):
        print(total_number_conflict[i])


if __name__ == "__main__":
    run_q4()

















    
