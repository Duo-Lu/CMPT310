from a2_q2 import * 


def check_teams(graph , csp_sol):
    length = len(csp_sol)
    check_dic = {}

    # make teams
    # for example X = {0:0, 1:1, 2:1, 3:0}
    # make 0:[0 , 3] , 1: [1 , 2]
    for i in range(length):
        check_dic.setdefault(i , [])
        check_dic.setdefault(csp_sol[i] , []).append(i)

    length_check = len(check_dic)
    #print('check_list:' , check_dic)           # Debug remove before submit 


    # nestered loops check in teams whether it has friendship relations 
    for i in range(length_check):
        group_list =  check_dic[i]
        #print('group_list' , group_list)       # Debug remove before submit 
        #print(len(group_list))                 # Debug remove before submit 
        
        for i in range(len(group_list)):
            #print('i:' , i)                    # Debug remove before submit 
            j = i + 1
            
            for j in range(len(group_list)):
                #print('j:' , j)                # Debug remove before submit 
                if group_list[j] in graph[group_list[i]]:
                    return False
    return True
        

    return check_dic
