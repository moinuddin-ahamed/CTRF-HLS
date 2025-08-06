
import re
from pyeda.inter import *
#from graphviz import Source 
from pyeda.boolalg.expr import exprvar
import pickle
import numpy as np
from Evaluate_boolean import *

trees = 100
Terms = 8
#Tree_no = 1
n_class = 2

with open('CTRF/Output/test5.pickle', 'rb') as file:
    winetest = pickle.load(file)

pima = np.asarray(winetest)
[P,Q] = pima.shape
target = pima[:,-1]
pfeatures = pima[:,0:Q-1]
   
class bds_Func:
    
    def predict(dt, bf, winetest):
        correct = 0
        arg2 = []
        #winetest = wine1
        for v in range(len(winetest)):
            count_list = []
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
            count5 = 0
            count6 = 0
            count7 = 0
            count8 = 0
            count99 = 0
            count100 = 0
            count111 = 0
            count122 = 0
            #num_literals1 = 0
            #num_literals2 = 0
            class1_f = []
            class2_f = []
            class1_fm = []
            class2_fm = []
            var1 = []
            var2 = []
            for cc in range(0, Terms, 4):
                count = 0
                for d in range(0,trees-1,1):
                    #result = has_empty_lists(bf[d])
                    #if(result == False):
                    my_list = bf[d][cc]

                    my_list1 = dt[d][4]
                    #print(my_list1)
                    my_list2 = dt[d][5]
                    my_list3 = dt[d][0]
                    #my_list4 = [-0.00092,  0.01001]

                    list1 = my_list1
                    list2 = winetest[v][0:Q-1]

                    # Find the indices in list1 that correspond to indices in list2
                    indices1 = [i for i, x in enumerate(list1) if isinstance(x, int) and x < len(list2)]

                    # Create a new list with the values from list2 based on the indices in list1
                    new_list = [list2[list1[i]] if i in indices1 else x for i, x in enumerate(list1)]

                    indices = []

                    for i in range(len(my_list1)):
                        if not isinstance(my_list1[i], list) or my_list1[i]:
                            indices.append(i)
                    list_f = [my_list1[i] for i in indices]
                    list_v = [my_list2[i] for i in indices]
                    list_n = [my_list3[i] for i in indices]
                    list_r = [new_list[i] for i in indices]
                    #print(list_f)
                    #print(list_v)
                    #print(list_n)
                    #print(list_r)
                    bool_list = [x > y for x, y in zip(list_v, list_r)]
                    #print(bool_list)

                    # Example usage
                    #num = len(list_v)
                    #alphabets_str = get_alphabets_str(num)
                    #print(alphabets_str) # Output: 'abcde'

                    #alphabet_list = list(alphabets_str)
                    #alphabet_with_commas = ",".join(alphabet_list)
                    #print(alphabet_with_commas)

                    #alphabet_with_commas = map(exprvar, alphabets_str)

                    #if(mt[d][cc] != []):
                    #  my_list = mt[d][cc]

                    num = len(list_v)
                    variable_names = ['x[{}]'.format(i) for i in range(num)]
                    alphabet_with_commas = ",".join(variable_names)

                    alphabet_with_commas = map(exprvar, variable_names)

                    reversed_list = []
                    for lst in my_list:
                        if isinstance(lst, list):
                            reversed_inner_list = lst[::-1]
                            reversed_list.append(reversed_inner_list)

                    #print(reversed_list)

                    for sub_list in reversed_list:
                        for element in sub_list:
                            #print('')
                            pass
                    keys   = list_n
                    values = variable_names
                    my_dict = dict(zip(keys, values))

                    list1 = []
                    list2 = []
                    for my_list in reversed_list:
                        for element in my_list:
                            for i in range(len(my_list)-1):
                                if my_list[i+1] % 2 == 1: # if next element is odd
                                    #print("~" + my_dict[my_list[i]])
                                    literal = "~" + my_dict[my_list[i]]
                                else:
                                    #print(my_dict[my_list[i]])
                                    literal = my_dict[my_list[i]]

                                if i == 0:
                                    s = literal
                                else:
                                    s += " & " + literal
                        list1.append(expr(s)) # convert s to a Boolean expression using expr()
                        list2.append(s)

                    # Create a Boolean expression by taking the OR of all expressions in list1
                    f1 = Or(*list1)

                    # define the input expression as a string
                    expression = repr(f1)

                    # use regular expressions to extract the And clauses
                    and_clauses = re.findall("And\((.*?)\)", expression)

                    # split each And clause into a list of its components
                    and_lists = [clause.split(", ") for clause in and_clauses]

                    # print the resulting list of lists
                    #print(and_lists)
                    #print(list2)

                    lst = list2
                    new_lst1 = []
                    for s in lst:
                        literals = [literal.strip() for literal in s.split('&')]
                        new_lst1.append(literals)

                    #print(new_lst1)

                    values = bool_list
                    variable_names = variable_names
                    variable_dict = dict(zip(variable_names, values))

                    #print(variable_dict)

                    expression = new_lst1
                    variable_values = variable_dict
                    result = Evaluate_Boolean.evaluate_boolean_function(expression, variable_values)
                    #print(result)
                    #print(new_lst1)

                    expression = and_lists
                    variable_values = variable_dict
                    result = Evaluate_Boolean.evaluate_boolean_function(expression, variable_values)
                    if(result == True):
                        count = count+1
                    #print(result)
                    #print(and_lists)
                    #print('------')
                    #for clause in f1.cover:
                    #   num_literals1 += len(clause)
                    #for clause in fm.cover:
                    #    num_literals2 += len(clause)
                    f1 = f1.to_binary()
                    #fm = fm.to_binary()

                    #count1 =count1 + f1.size

                    #count3 =count3 + f1.depth

                    #count5 =count5 + f1.cardinality

                    #count7 =count7 + len(f1.inputs)

                    count99 =count99 + len(re.findall(r"\bAnd\b", str(f1)))

                    count111 = count111 + len(re.findall(r"\bOr\b", str(f1)))

                count_list.append(count)
                #print(count)

            max_index = count_list.index(max(count_list))
            #print(max_index)

            if(max_index == int(winetest[v][-1])):
                correct = correct+1
            arg2.append(max_index)
        #print(correct)
        print('-------------------------------------------')
        print('BDS:',correct/len(winetest))
        acc3 = correct/len(winetest)
        #print(f1)
        #print(len(re.findall(r"\bAnd\b", str(f1))))
        #print(len(re.findall(r"\bOr\b", str(f1))))
        print('-----------------------------')
        return acc3, arg2, count99, count111
