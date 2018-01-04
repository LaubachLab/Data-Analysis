# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 11:08:44 2015



Generates a list of bouts.
Bouts are defined as
    - a series of 3 or more licks
    - a span of time at least 0.3 seconds long
    - a span of time with at least a 0.5 second pause before the next bout


boutGenerator(Licks,min_break,min_dur,min_licks)
Licks = list of timecodes for each lick
min_break = interbout interval - minimum time between bouts (0.5 sec)
min_dur = minimum duration of bout (0.3 sec)
min_licks = minimum number of licks per bout (3 licks)

@author: Kyra S
"""
import numpy as np
import statistics as stats
        
#counts the number of licks in each bout
def countLicks(licks,starts,ends):
    counts = [[x for x in licks if x >= starts[i] and x <= ends[i]] for i in range(len(starts))]
    counts = [len(i) for i in counts]
    return counts
    
    
#removes licks that are less than or equal to the ILI
def CleanLicks(lst,ILI):
    lick_difference = np.diff(lst)
    bad_index = []
    for i in range(len(lst) - 1):
        if lick_difference[i] <= ILI:
            bad_index.append(i)
    bad_index.reverse()
    for i in bad_index:
        del lst[i+1]
    return lst

#generates a list of bouts with format
# [ START_TIME, END_TIME, BOUT_DURATION, #_LICKS ] 
def generate(Licks,min_break,min_dur,min_licks):
    #holder for bouts
    bouts = []
    #indices of where there is a gap between licks of at least %min_break
    index_End = np.where(np.diff(Licks)>=min_break)[0]
    #print("Breaks:",len(index_End),index_End)
    if(len(index_End) >= 1):
        #print(index_End)
        index_Start = [x + 1 for x in index_End]
        #list of times for bout start and bout end
        time_Start = [Licks[0]] + [Licks[i] for i in index_Start]
        time_End = [Licks[i] for i in index_End] + [Licks[-1]]
        
        #total number of bouts
        num_bouts = len(time_Start)
        #duration of bout
        duration = [time_End[i] - time_Start[i] for i in range(num_bouts)]
        #number of licks per bout
        lick_count = countLicks(Licks,time_Start,time_End)
        
        for i in range(num_bouts):
            if duration[i] >= min_dur and lick_count[i] >= min_licks:
                bouts.append([time_Start[i],time_End[i],duration[i],lick_count[i]])
        
    return bouts
    
    
def allILIs(lst):
    total=[]
    for i in range(len(lst)):
        for x in range(len(lst[i][3])):
            total.append(lst[i][3][x])
    return total