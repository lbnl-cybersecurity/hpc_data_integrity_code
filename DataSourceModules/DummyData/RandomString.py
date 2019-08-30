#!/usr/bin/python3

import random, string, os, uuid
from random import randint

class RandomString:
    
    #folder used to store the generated random data 
    output_folder="output"
    def __init__(self):
        pass


    #generate random  string of length 'length'
    def randomword(self, length):
        ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        return ''.join(random.choice(ALPHABET) for i in range(length))

    #function to generate random data returns [ID, payload]
    def simulate_orignal_data(self, length=randint(8,10) ):
        
        payload = self.randomword(length)
        #write the string to file 
        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder)
        f= open(self.output_folder+"/"+payload+".txt","w+")
        f.write(payload)
        f.close()
        file_name = self.output_folder+"/"+payload+".txt"
        return file_name

    """// OutputData represents an output of a computation
    type OutputData struct {
        Id        string `json:"id"`
        Input     string `json:"input"`
        Hval      string `json:"hval"`
        Processed System `json:"system"`
    }"""

    def simulate_output_data(self, length=randint(8,10)):

        Id = str(uuid.uuid4())
        Input = "some ID" #this can represent an ID of the input data / transaction id of the input data in the blockchain
        payload = self.randomword(length)
        return payload 