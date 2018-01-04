# -*- coding: utf-8 -*-
"""
MED_to_TEC.py

Converts MedPC file into list of [time,event] codes (TEC)

Requires the following DISKVARS:
DIM A=9900, B=3

Requires Time-Event pairs to be saved as:
TIME.00EVENT
For example, an event 1 at exactly 536 seconds from start will be recorded as 
268000.001
Currently, the system clocks at 2ms, so time codes are divided by 500 
to convert them to seconds.
Events are converted to integers.
The final product for this event is 
[536,1]

Created Jan 5 15:23 2015
Last Edited Feb 8 11:47 2016 

Author: Kyra Swanson
"""
import numpy as np
import re

#convert time to seconds (BTIME at 2ms, 500/sec) (old files timeslice = 200)
timeslice = 500

#convert a .med file into a readable format 
def convert(fileName):
    start_flag = 'A'
    stop_flag = 'B'
    #open file
    fid = open(fileName)
    #store lines in list
    lines = fid.readlines()
    fid.close()
    #find A: flag
    start_index = 0
    stop_index = 0
    for i, j in enumerate(lines):
        if j[0] == start_flag:
            start_index = i + 1
        if j[0] == stop_flag:
            stop_index = i         
    lines = lines[start_index:stop_index]
    #clean lines
    for i, item in enumerate(lines):
        lines[i] = cleanLines(item)
    
    #break lines, store time,event in list Time_Event
    Time_Event = breakLine(lines)
#    TEC = np.asarray(Time_Event)
    return Time_Event
    
#cuts off beginning marker, ending new lines, replaces space divisions with ,
def cleanLines(item):
   # print(item)
    try:
        start = item.index(":") + 1
        item = item[start:]
        item = item.replace("\n","")
        item = item.split()
    except ValueError:
        return "0"
    return item

    
#separates the time code and the event code
def breakLine(lines):
    Time_Event = []
    for item in lines:
        for el in item:
            temp = el.split(".")
            if temp[0] != "0":
                temp[0] = float(temp[0])/timeslice
                temp[1] = int(temp[1])
                Time_Event.append(temp)
    return Time_Event
    
def breakLick(lines):
    Time_Event = []
    for item in lines:
        for el in item:
            el = float(el)
            if el != 0:
                temp = el/timeslice
                Time_Event.append(temp)
    return Time_Event

    
def extract_Licks(fileName):
    start_flag = 'L'
    #open file
    fid = open(fileName)
    #store lines in list
    lines = fid.readlines()
    fid.close()
    #find A: flag
    start_index = 0
    stop_index = 0
    for i, j in enumerate(lines):
        if j[0] == start_flag:
            start_index = i + 1 
    lines = lines[start_index:]
    
    #clean lines
    for i, item in enumerate(lines):
        lines[i] = cleanLines(item)
       
    #break lines, store time,event in list Time_Event
    Time_Event = breakLick(lines)
    #print(Time_Event)
    
 #   TEC = np.asarray(Time_Event)
    return Time_Event
        
    

#****************************************************************************    
#   PULLING OUT DATA    
    
#returns times for a given code    
def findTimes(EV,code):
    return [val[0] for (i,val) in enumerate(EV) if val[1] == code]    
#returns a list of events within windows marked by a second event
#returns a list of the following:
# [0] start time of window
# [1] end time of window (.5 sec)
# [2] number of events within window
# [3] interval between event

def findWindows(count_event,window_event,duration):
    windows = []
    for i in window_event:
        start = i
        end = start + duration
        num_events = sum(1 for time in count_event if time >= start and time < end)
        events_in_window = [val for (i,val) in enumerate(count_event) if val>=start and val < end]
        difference = [x for x in np.diff(events_in_window)]
        windows.append([start, end, num_events, difference])
    return windows
    
#Returns the value for a given variable
def findVariable(fileName,variable):
    fid = open(fileName)
    lines = fid.readlines()
    fid.close()
    
    for i,j in enumerate(lines):
        if j[0] == variable:
            answer = lines[i]
    
    answer = answer[:-5]
            
    start = re.search("\d", answer).start()
    return int(answer[start:])    
    





