import matplotlib.pyplot as plt
import numpy as np
import random
import math
import pandas
import timeit
import re
import scipy
import itertools
from sklearn.model_selection import StratifiedKFold
from gmm_mml import GmmMml
from sklearn import datasets
import pickle
import copy
from pyeda.inter import *
#from graphviz import Source 
from pyeda.boolalg.expr import exprvar
from basic_functions import *
from IG_func import *
from Evaluate_boolean import *
from obds_func import *
from MintermCal import *
from RF import *
from bds_fun import *

trees = 100
Terms = 8
#Tree_no = 1
n_class = 2

# Load the saved result from the file
with open('CTRF/Output/dt5.pickle', 'rb') as file:
    dt = pickle.load(file)
# Load the saved result from the file
with open('CTRF/Output/test5.pickle', 'rb') as file:
    winetest = pickle.load(file)
with open('CTRF/Output/bf5.pickle', 'rb') as file:
    bf = pickle.load(file)
with open('CTRF/Output/eo5.pickle', 'rb') as file:
    mt = pickle.load(file)

pima = np.asarray(winetest)
[P,Q] = pima.shape
target = pima[:,-1]
pfeatures = pima[:,0:Q-1]


def has_empty_lists(list_of_lists):
    for sublist in list_of_lists:
        if isinstance(sublist, list) and len(sublist) == 0:
            return True
    return False

acc1,arg_dt = RF_Func.dt_predict(dt, winetest)
acc2,arg_dt1 = RF_Func.dtv_predict(dt, winetest)
acc3,arg, and1, or1 = bds_Func.predict(dt, bf, winetest)
acc4,arg1,and2, or2 = obds_Func.predict(dt, mt, winetest)


#print(and1-and2,and2-and3,or1-or2,or2-or3)
#print(len(class1_fm),len(class2_fm),len(class3_fm))

hist_node = []
hist_depth = []
hist_leaf = []
for d in range(trees):
    count = 0
    for x in range(0,len(dt[d][0])):
        if(not(dt[d][5][x])):
            count = count+1
    hist_leaf.append(count)
    hist_node.append(len(dt[d][0]))
    hist_depth.append(int(np.log2(max(dt[d][0]))))


#print(sum(hist_node)-sum(hist_leaf))


import csv
new_data = [acc1,acc2,acc3,acc4,and1, and2, or1,or2, sum(hist_node)-sum(hist_leaf)] 
#new_data = [acc1,acc2,acc3,acc5,and2, and3,or2,or3,size2,size3,depth2,depth3,card2,card3,sum(hist_node)-sum(hist_leaf),sum(bf_total),sum(var1)-sum(var2)]
file_path = 'CTRF/Output/file.csv'  # Replace this with the actual path to your CSV file
with open(file_path, 'a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(new_data)

