
from basic_functions import *
import timeit
import numpy as np


trees = 100
Terms = 8
#Tree_no = 1
n_class = 2

class RF_Func : 
    def dt_predict(dt, winetest):
        arg_dt = []
        arg_dtp = []
        correct = 0
        acc1 = 0
        #winetest = wine1
        for t in range(len(winetest)):
            post = []
            for d in range(trees):
                for n in range(len(dt[d][0])):
                    if(dt[d][5][n]):
                        if(winetest[t][dt[d][4][n]]>dt[d][5][n]):
                            if(dt[d][2][n]):
                                if(not(dt[d][5][dt[d][2][n]])):
                                    temp = dt[d][2][n]
                                    post.append(dt[d][8][temp])
                                    break
                        else:
                            if(dt[d][3][n]):
                                if(not(dt[d][5][dt[d][3][n]])):
                                    temp = dt[d][3][n]
                                    post.append(dt[d][8][temp])
                                    break
            
            dic = basic_functions.class_counts(winetest)
            labels = list(dic.keys())
            labels.sort()

            sum_p = [ [] for i in range(len(labels)) ]
            leaf_p = []
            leaf_c = []
            for n in range(len(post)):
                leaf_p.append(post[n][0])
                leaf_c.append(post[n][1])

            for p in range(len(post)):
                for q in range(len(leaf_c[p])):
                    for r in range(len(labels)):
                        if(labels[r] == leaf_c[p][q]):
                            sum_p[r].append(leaf_p[p][q])
            #print(sum(sum_p[0])/50,sum(sum_p[1])/50,sum(sum_p[2])/50,sum(sum_p[3])/50,sum(sum_p[4])/50)
            #print(sum(sum_p[0])/50+sum(sum_p[1])/50+sum(sum_p[2])/50+sum(sum_p[3])/50+sum(sum_p[4])/50)
            max_class = []
            for l in range(len(labels)):
                max_class.append(sum(sum_p[l])/trees)
            #print(max_class)
            arg_max = np.argmax(max_class)
            #print(max_class[arg_max])

            #print(winetest[t])
            arg_dt.append(arg_max)
            arg_dtp.append(max_class[arg_max])
            del sum_p,leaf_p,leaf_c,post

        #   for t in range(len(winetest)):
            if(int(winetest[t][-1]) == arg_dt[t]):
        #         print(int(winetest[t][-1]),arg[t])
                correct = correct+1
        #         print(correct)
        #     else:
        #         print(int(winetest[t][-1]),arg[t])
        #     stop_test = timeit.default_timer()

        acc1 = correct/len(winetest)
        print('-------------------------------------------')
        print('RF:',acc1)
        print('-------------------------------------------')
        return acc1, arg_dt


    def dtv_predict(dt, winetest):
        arg_dt1 = []
        correct = 0
        acc2 =0
        #winetest = wine1
        for t in range(len(winetest)):
            post = []
            for d in range(trees):
        #             start_test = timeit.default_timer()
                for n in range(len(dt[d][0])):
                    if(dt[d][5][n]):
                        if(winetest[t][dt[d][4][n]]>dt[d][5][n]):
                            if(dt[d][2][n]):
                                if(not(dt[d][5][dt[d][2][n]])):
                                    temp = dt[d][2][n]
                                    post.append(dt[d][8][temp])
                                    break
                        else:
                            if(dt[d][3][n]):
                                if(not(dt[d][5][dt[d][3][n]])):
                                    temp = dt[d][3][n]
                                    post.append(dt[d][8][temp])
                                    break
            start_test = timeit.default_timer()
            dic = basic_functions.class_counts(winetest)
            labels = list(dic.keys())
            labels.sort()

            sum_p = [ [] for i in range(len(labels)) ]
            leaf_p = []
            leaf_c = []
            for n in range(len(post)):
                leaf_p.append(post[n][0])
                leaf_c.append(post[n][1])

            for p in range(len(post)):
                for q in range(len(leaf_c[p])):
                    for r in range(len(labels)):
                        if(labels[r] == leaf_c[p][q]):
                            sum_p[r].append(leaf_p[p][q])
            #print(sum_p)
            #break
            #print(sum(sum_p[0])/50,sum(sum_p[1])/50,sum(sum_p[2])/50,sum(sum_p[3])/50,sum(sum_p[4])/50)
            #print(sum(sum_p[0])/50+sum(sum_p[1])/50+sum(sum_p[2])/50+sum(sum_p[3])/50+sum(sum_p[4])/50)
            max_class = []
            for l in range(len(labels)):
                max_class.append(sum(sum_p[l])/trees)
            #print(max_class)
            arg_max = np.argmax(max_class)
            #print(arg_max)
            vote = []
            for d in range(len(post)):
                class_max_index = np.argmax(post[d][0])
                #print(class_max_index)
                vote.append(class_max_index)

            find_max_class = []
            for d in range(len(post)):
            #print(post[d][1][vote[d]])
                find_max_class.append(post[d][1][vote[d]])

            #most_frequent(find_max_class)
            #print(winetest[t])
            arg_dt1.append(basic_functions.most_frequent(find_max_class))
            del sum_p,leaf_p,leaf_c,post

        #   for t in range(len(winetest)):
            if(int(winetest[t][-1]) == arg_dt1[t]):
        #         print(int(winetest[t][-1]),arg[t])
                correct = correct+1
            #stop_test = timeit.default_timer()
            #avg_test_time = avg_test_time + (stop_test - start_test)

        #         print(correct)
        #     else:
        #         print(int(winetest[t][-1]),arg[t])
        #     stop_test = timeit.default_timer()

        acc2 = correct/len(winetest)
        print('-------------------------------------------')
        print('RF-V:',acc2)
        #print('Table Time: ', avg_test_time)
        print('-------------------------------------------')
        return acc2, arg_dt1