'''
    Functions for accessing and downloading uPMU data from LBNL Cassandra DB
    PI: Sean P. Peisert
    Author: Bogdan Copos

    NOTICE: This computer software was prepared by The Regents of the
    University of California and Sean Peisert, hereinafter the Contractor,
    under Contract No. DE-AC02-05CH11231 with the Department of Energy
    (DOE). All rights in the computer software are reserved by DOE on
    behalf of the United States Government and the Contractor as provided
    in the Contract. You (NSA) are authorized to use this computer software for
    Governmental purposes but it is not to be released or distributed to
    the public. NEITHER THE GOVERNMENT NOR THE CONTRACTOR MAKES ANY
    WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES ANY LIABILITY FOR THE USE OF
    THIS SOFTWARE. This notice including this sentence must appear on any
    copies of this computer software.
'''

import sys
import os
import random
import datetime
import math
import time
import json

from collections import OrderedDict



### CASSANDRA IMPORTS
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra.query import dict_factory
from cassandra.auth import PlainTextAuthProvider
from utils import upmuDataProtobuf_pb2 #import *
from utils import upmuStructKeyValueListProtobuf_pb2 #import *
from protobuf_to_dict import protobuf_to_dict

# Uses step detection script by Thomas Kahn (source: https://github.com/thomasbkahn/step-detect/blob/master/step_detect.py)
#import step_detect

def connect_cassandra(host, username, password): 
  auth_provider = PlainTextAuthProvider(username=username, password=password)
  cluster = Cluster([host], auth_provider = auth_provider)
  session = cluster.connect()
  session.set_keyspace('upmu_devel')
  return session, cluster

def query_cassandra(start, end, session, device):   
  upmu_data = []
  
  start_day = int(start/(1000*24*60*60))
  end_day = int(end/(1000*24*60*60)) + 1
  days = ','.join(str(i) for i in range(start_day, end_day+1))
  query = "SELECT * FROM upmu_data WHERE DEVICE = '{0}' AND DAY IN ({1}) AND timestamp_msec >= {2} AND timestamp_msec < {3}".format(device, days, start, end)
  statement = SimpleStatement(query, fetch_size=100)
  for user_row in session.execute(statement):
    try:
      data = upmuDataProtobuf_pb2.upmuData()
      data.ParseFromString(user_row.data)  
      assert isinstance(data, upmuDataProtobuf_pb2.upmuData)
      pyobj =  protobuf_to_dict(data)
      secs = float(pyobj['timeStamp'])
      interval_msec = pyobj['sampleIntervalMsec']/1000

      for datum in pyobj['sample']:
        upmu_data.append((secs, datum['C1mag'], datum['C1angle'], datum['C2mag'], datum['C2angle'], datum['C3mag'], datum['C3angle'], datum['L1mag'], datum['L1angle'], datum['L2mag'], datum['L2angle'], datum['L3mag'], datum['L3angle'] ))
        secs += interval_msec

    except AttributeError:
      pass
  return upmu_data


def get_experiment_times(target_programs, log):
  times = []
  with open(log, 'r') as f:
    for line in f:
      parts = line.split()
      program = parts[-1].split('/')[-1]
      try:
        line_day = int(float(parts[0])/(24*60*60) - ( float(parts[0])/(24*60*60)%1 ))
      except ValueError:
        continue

      
      if len(target_programs) == 1 and target_programs[0] == 'all':
        times.append((program, line_day, float(parts[0]), float(parts[1])))
      else:
        for tp in target_programs:
          if tp in program.lower():
            times.append((program, line_day, float(parts[0]), float(parts[1])))
  return times


def get_experiments_data(host, username, password, device, times, buf):
  upmu_data = OrderedDict()
  session, cluster = connect_cassandra(host, username, password)
  for t in times:
    program, day, start, end = t
    if start == end:
      end = start + 1
    data = query_cassandra((int(start) - buf) * 1000 , (int(end) + buf) * 1000, session, device)
    if data:
      try:
        upmu_data[program][start] = data
      except KeyError:
        upmu_data[program] = OrderedDict()
        upmu_data[program][start] = data
  cluster.shutdown()
  return upmu_data

