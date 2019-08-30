import os
import sys, timeit
sys.path.append('..')
import json
import numpy as np
from utils import upmu_helpers
from multiprocessing import Pool, Queue
import multiprocessing
import pandas as pd
import pika, itertools
import time,calendar
import socket
import json, hashlib
# make sure ES is up and running
import requests #pip install requests
from elasticsearch import Elasticsearch,helpers #pip install elasticsearch5
from DataInt import *


bc_app = DataInt()
# a function to get an entry for a dvice from rime range startime to endtime
# by default starts from 1475819580 (GMT: Friday, October 7, 2016 5:53:00 AM)
# got error a month before this date 
# ID of other mpmu device P3001065
def getDataCassandra(device_id_input='P3001199', starttime = 1475819580.0, endtime = 1475819640.0):
    program = "DataInt"  # fill in anything
    # Format the timestring so that cassandra understands it.
    times = []
    #this variable is not used
    line_day = 0
    times.append((program, line_day, float(starttime), float(endtime)))

    # Query cassandra to get data
    hostname = 'dash.lbl.gov' #candance.lbl.gov coltrane.lbl.gov the actuall databases, paralelize over these may give better result
    user = 'readonly'
    password = 'readonly'
    device_id = device_id_input #the device that you want to read from

    upmu_data = upmu_helpers.get_experiments_data(hostname, user, password, device_id, times, buf=0)
    if upmu_data.keys() == []:
        print("Error getting data")
        return False

    data_key = list(upmu_data[program].keys())[0] 
    data = upmu_data[program][data_key] 

    """
    #use this to do the add/verify opration in parallel per process
    re = bc_app.verify( data=str(data), datatype="string")
    if not re:
        print("not found")
    """


    return data # returns array of tuples  [ (timestamp, data ....), (timestamp, data ....)  ....]

# this method prepare args for parallel processes
# it reterns a generatoer for (device_id, starttime, endtime) 
def get_arg(endtime):
    device_id_input='P3001199'
    #start time (GMT: Friday, October 7, 2016 5:53:00 AM)
    starttime = 1475819580
    min = 60

    while starttime < endtime:
        starttime += min
        yield (device_id_input, starttime - min, starttime)

def _verify(value):
    re = bc_app.verify( data=str(value), datatype="string")
    if not re:
        print("not found")
        return False
    return True



def getCassandraDataPerHr(endtime=1475823180):

    # getDataCassandra() takes on avg 0.449 secs to get 1 min data. It reads from casandra
    # use the folloing to test
    # print(timeit.timeit("getDataCassandra()", setup="from __main__ import getDataCassandra", number=100 ))
    p = Pool(60)
    re = p.starmap_async(getDataCassandra, get_arg(endtime))
    re.wait()
    double_array = re.get() # [ [return from getDataCassandra call] , [..], [..], ...   ] the size is = len(get_arg())
    
    # this loop writes every min of data to file and agregates file names in 'filenames'
    # you can pss this names to the blockchain writing fuction with -f option
    """filenames = []
    for i in range(len(double_array)):
        fname = str(double_array[i][0][0])
        f = open("outputs/"+fname, 'a')
        f.write(str(double_array[i][0]))
        filenames.append(fname)
    """


    # or using this loop pass every min of data to the blockchain directly with -s option
    # use this for sequential add/verify oprations
    for i in range(len(double_array)):
        re = bc_app.add( data=str(double_array[i]), datatype="string")
        if re:
            print("add a min of record to blockchain")
        else:
            print("Error: " + double_array[i][0] + " is not added")

if __name__ == "__main__":
    #getCassandraDataPerDay()
    endtime = 1475823180 # for 60 min #1475905980 # one day    #time.time()
    getCassandraDataPerHr(endtime)

    # use this to measure the time taken by the given function
    #print(timeit.timeit("getCassandraDataPerHr()", setup="from __main__ import getCassandraDataPerHr", number=1))

