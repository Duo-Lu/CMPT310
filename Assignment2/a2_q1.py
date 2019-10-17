from csp import *
import random


def rand_graph(number_node , probability):

    # The empty dictionary
    graph_dic = {}
    # set the default value -> empty list to dictionary 
    for i in range(number_node):
        graph_dic.setdefault(i , [])


    for i in range(number_node - 1):            # Because j reached number_node - 1, i is no necessary touch the number_node - 1
        for j in range(i , number_node):
            if i != j:                          # same thing like i + 1
                r = random.random()
                if r <= probability:            # if the random number(0 , 1) fall in given probability, we assigned each other
                    graph_dic.setdefault(i , []).append(j)
                    graph_dic.setdefault(j , []).append(i)


    # old method 
    # Remove the duplicate
#    for i in range(number_node):
        #print(graph_dic[i])
#        graph_dic[i] = list(set(graph_dic[i]))

    return graph_dic












