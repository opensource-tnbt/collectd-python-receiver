#import numpy as np
#import pandas as pa
#import seaborn as sb
import matplotlib
import matplotlib.pyplot as plt

def plotGraphs(dict_of_arrays):
    for tup_lists in dict_of_arrays:
        tup_list = dict_of_arrays[tup_lists]
        two_lists = map(list, zip(*tup_list))
        y_axis_list = two_lists[0]
        x_axis_list = two_lists[1]
        plt.plot(x_axis_list, y_axis_list)
        plt.xlabel("Time (Ticks)")
        plt.savefig(str(tup_lists)+'.png')
        #print tup_lists
        #print '\n'
        #print x_axis_list
        #print '\n'
        #print y_axis_list
        #print '\n'


#def moving_average(a, n=3):
#    ret = np.cumsum(a, dtype=float)
#    ret[n:] = ret[n:] - ret[:-n]
#    return ret[n - 1:] / n

