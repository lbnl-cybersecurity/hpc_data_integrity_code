import os
import sys, timeit
sys.path.append('..')
import json
import numpy as np
from utils import upmu_helpers
from multiprocessing import Pool, Queue
import pandas as pd
import pika
import time,calendar
import socket


# make sure ES is up and running
import requests #pip install requests
from elasticsearch import Elasticsearch,helpers #pip install elasticsearch5
#from elasticsearch import helpers #not used anymore
def CheckESup():
    res = requests.get('http://flash.lbl.gov:9201')
    if(res.status_code == 200):
        print("Conencted to Elasticsearch")
        return True
    else:
        print("Error connecting to Elasticsearch")
        return False


def GetAllIndexES():
    es = Elasticsearch(["flash.lbl.gov"], port=9201)

    indices = es.indices.get_alias("*")
    #print("all index:", sorted(indices))
    return sorted(indices)


def getdataES(indexname='upmu-unwrapped_phase-2017.10.07'):


    es = Elasticsearch(["flash.lbl.gov"], port=9201)


    indices=es.indices.get_alias("*")
    #print("all index:", sorted(indices))
    print("TODO: Pick index ***********************")

    try:
        page = es.search(
            index=indexname, #enter index here
            #doc_type='logs', #can make some extra refinements if needed.
            scroll='2m', #keep the index alive for 2 min
            #search_type='scan', #depeciated, just leave commented
            size=10000, #100 items at a time
            body={
                "query": {"match_all": {}}# Your query's body
            })
        sid = page['_scroll_id']
        scroll_size = page['hits']['total']

        print(type(page))
        exit()

        # Start scrolling
        while (scroll_size > 0):

            #print "Scrolling..."
            page = es.scroll(scroll_id=sid, scroll='2m')

            sid = page['_scroll_id'] # Update the scroll ID
            scroll_size = len(page['hits']['hits'])  # Get the number of results that we returned in the last scroll
            print("Got " + str(scroll_size) + " items")
            if (scroll_size!=0):
                processedataES(page)

    except(KeyboardInterrupt):
        pass

def processedataES(page): #called with 100 items at a time (or less if less are available)
    
    print(type(page['hits']))  # here is your data
    print(page.keys())
    print("TODO: DO PROCESSING ***********************")

#starttime = 1502101580.0 + 86400, endtime = 1502101600.0 
"""def getDataCassandra(device_id_input='P3001199', starttime = 1502101580.0, endtime = 1502187980.0):
    program = "whatever"  # fill in anything

    # Format the timestring so that cassandra understands it.
    times = []
    try:
        line_day = int(float(starttime) / (24 * 60 * 60) - (float(endtime) / (24 * 60 * 60) % 1))
    except ValueError:
        print("ValueError")
    times.append((program, line_day, float(starttime), float(endtime)))
    print("line day " + str(line_day))
    # Query cassandra to get data
    hostname = 'dash.lbl.gov'
    user = 'readonly'
    password = 'readonly'
    device_id = device_id_input #the device that you want to read from
    print("*** Getting data from cassandra *** for " + str(line_day))
    upmu_data = upmu_helpers.get_experiments_data(hostname, user, password, device_id, times, buf=0)
    if upmu_data.keys() == []:
        print("Error getting data")


    #Format the data, optional
    db_query_cols = ['timestamp', 'C1mag', 'C1angle', 'C2mag',
                     'C2angle', 'C3mag', 'C3angle',
                     'L1mag', 'L1angle', 'L2mag',
                     'L2angle', 'L3mag', 'L3angle']
    data = {}
    print("Formating data for program {}...".format(program))
    #print(type(upmu_data))
    data_key = upmu_data[program].keys()[0]
    
    print(len(upmu_data[program].values()[0]))
    
    data[program] = pd.DataFrame(np.asarray(upmu_data[program][data_key]))
    rows, cols = data[program].shape
    print("after dataframe "+ str(len(data[program])))
    # print(str(rows) + " " + str(cols))
    data[program]['target'] = program
    data[program].columns = db_query_cols + ['target']
    df_all_day1 = pd.concat([data[k] for k in data.keys()])

    print(type(df_all_day1)) """

    #here you got your data.


def processedataCassandra(df_all_day1):

    print("TODO: DO PROCESSING ***********************")






#Sent result to rabbit

def SendResultToRabbit(json_annotation,user='ciaran',password='powerdata'):

    # json_annotation = {
    #     '@timestamp': str(time.time()) + 'Z',
    #     'ANN_AUTHOR': 'LBNL_RGentz',
    #     'ANN_VER': '0.1',
    #     'ANN_GROUP': 'Standard',
    #     'ANN_NAME': 'annotation_name',
    #     'ANN_TYPE': 'BL',
    #     'ANN_SUBCLASS': '1',
    #     'ANN_DESC': 'Ciarans Aweseome Code',
    #     'ANN_DATASOURCE_UUID': device_id,
    #     'ANN_COMPUTATION_SITE': socket.gethostbyname(socket.gethostname()),
    #     'ANN_SENSOR_LOCATION': '',
    #     'ANN_Severity': '0',
    #     'ANN_PHASE': '0',
    #     'elastic_index': 'upmu',
    #     'elastic_type': 'ciarans',
    #     'ANN_TIME_INTERVAL': {
    #         'STARTTIME_UTC': str(starttime),
    #         'ENDTIME_UTC': str(endtime),
    #     },
    # }
    # print(json.dumps(json_annotation))

    credentials = pika.PlainCredentials( user,password )
    parameters = pika.ConnectionParameters('dash.lbl.gov',
                                           5672,
                                           '/',
                                           credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    #This code to receive
    # channel.queue_declare(queue="testmelissa2", durable=True, exclusive=False, auto_delete=True)
    # channel.queue_bind(queue='testmelissa2', exchange='ha-raw', routing_key="raw.P3001199.#")
    # channel.basic_consume(processedataRabbitMQ, 'testmelissa2')
    # print ("waiting for data, plese be patient for 1 minute")
    # try:
    #    channel.start_consuming()
    # except KeyboardInterrupt:
    #    channel.stop_consuming()


    rabbitmessage = json.dumps(json_annotation)
    # rabbitmessage= json.dump()
    channel.queue_declare(queue="hello", durable=True, exclusive=False, auto_delete=False)
    channel.queue_bind(queue='hello', exchange='rainer', routing_key="hello#")
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=rabbitmessage)

    connection.close()

def detDataRabbit(user='ciaran', password='powerdata',queuename="testciaran",exchangeinput='ha-raw', routing_key_input="raw.P3001199.#"):

    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters('dash.lbl.gov',
                                           5672,
                                           '/',
                                           credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queuename, durable=True, exclusive=False, auto_delete=True)
    channel.queue_bind(queue=queuename, exchange= exchangeinput, routing_key=routing_key_input)
    channel.basic_consume(processedataRabbit, queuename)
    print ("connected to rabbit; waiting for data, please be patient for up to 1 minute")
    try:
       channel.start_consuming()
    except KeyboardInterrupt:
       channel.stop_consuming()


def processedataRabbit(channel, method_frame, header_frame, body):
    channel.basic_ack(delivery_tag=method_frame.delivery_tag) #confirm receiving of message
    print(method_frame.delivery_tag)
    print(body)
    print()


# a function to get an entry for a dvice from rime range startime to endtime
# by default starts from 1475819580 (GMT: Friday, October 7, 2016 5:53:00 AM)
# got error a month before this date
def getDataCassandra(device_id_input='P3001199', starttime = 1475819580.0, endtime = 1475819640.0):
    program = "whatever"  # fill in anything

    # Format the timestring so that cassandra understands it.
    times = []
    #this variable is not used
    line_day = 0
    times.append((program, line_day, float(starttime), float(endtime)))

    # Query cassandra to get data
    hostname = 'dash.lbl.gov'
    user = 'readonly'
    password = 'readonly'
    device_id = device_id_input #the device that you want to read from
    print("*** Getting data from cassandra *** for " + str(line_day))
    upmu_data = upmu_helpers.get_experiments_data(hostname, user, password, device_id, times, buf=0)
    if upmu_data.keys() == []:
        print("Error getting data")
        return False
    #print(upmu_data.keys())
    #print(type(upmu_data.values()[0]))
    #print(len(upmu_data.values()[0].values()[0]))
    # the return value has this format {"key" : "program", "value" : [{"key":starttime, "value":[...] }]  }
    return list(upmu_data.values())



#
def getCassandraDataPerDay():

    #start time (GMT: Friday, October 7, 2016 5:53:00 AM)
    starttime = 1475819580
    endtime = time.time()
    min = 60 # read per min
    arg = []
    # getDataCassandra() takes on avg 0.449 secs to get 1 min data. It reads from casandra
    # use the folloing to test
    # print(timeit.timeit("getDataCassandra()", setup="from __main__ import getDataCassandra", number=100 ))

    """while starttime < endtime:
        st = starttime
        et = starttime + min """

    queue = Queue()

    re=getDataCassandra(starttime=starttime, endtime=starttime+min)

    """for i in range(60):
        arg.append((starttime, starttime+min))
        starttime += min

    with Pool(60) as p:
         re = p.map_async(getDataCassandra, arg) """
         
    #with  queue.get() as q:
    print(type(re))


#CheckESup() #just if you wanna check connectivity
"""ind = GetAllIndexES()
j = 0
for i in ind:
    print("index is:" + i)
    getdataES(i)
    j +=1
    if j > 2:
        exit()"""


getDataCassandra()
#getCassandraDataPerDay()

# using pool.map this print a total time of 15.159855778998462 which shows that it taks 1.515 sec to get 1 min data
# using pool.map_async() prints 2.0405810520023806 which is 0.204... sec to get 1 min of data. But the return is a type pool.AsyncResult should call .get() to get the return
#print(timeit.timeit("getCassandraDataPerDay()", setup="from __main__ import getCassandraDataPerDay", number=1))
print("finished")
