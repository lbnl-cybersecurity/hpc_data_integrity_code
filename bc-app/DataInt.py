#!/usr/bin/python3

import random, string, os, sys
from random import randint
import uuid, sys, argparse
import hashlib
from pathlib import Path
from App import *
sys.path.append('../')
from RandomString import * 


class DataInt:

	app = App()
	hash_function = hashlib.sha256()
	def __init__(self):
		#self.args = args
		pass

	def add(self, data=None, datatype="random"):

		# fuction to add the give data to the blockchain
		fuction_name = "addOriginalData"

		if datatype == "file" or datatype == "f":
			dataToAdd = self.hash_file(data)
		
		elif datatype == "string" or datatype == "s":
			
			self.hash_function.update(data.encode('utf-8'))
			dataToAdd = self.hash_function.hexdigest()

		elif datatype == "random" or datatype == "r":

			rs = RandomString()
			#get random file
			file = rs.simulate_orignal_data()
			dataToAdd = self.hash_file(file)

		elif datatype == "init" or datatype == "i":
		
			fuction_name = "initLedger"
			re = self.app.exec_init(fuction_name)
			self.final_info(re, "Pre-stored data added successfully")

		else: 
			print("Error: Unknown data type. The function add takes two args data and data type")

		Id = str(uuid.uuid4())	
		args = '{"Args":["'+fuction_name+'", "'+str(Id)+'", "'+str(dataToAdd)+ '"]}'
		re = self.app.exec_invoke(fuction_name, args)			
		self.final_info(re, "' "+ dataToAdd +"' added successfully")

		if re.returncode == 0:
			return True
		else:
			return False


	def verify(self, data, datatype="string"):

		#if not self.app.instantiate:
		#	print("The chain code is not instantiated. To see the help use --help")
		#	exit()

		if datatype == "file" or datatype == "f":
			dataToVerify = self.hash_file(data)

		elif datatype == "string" or datatype == "s":
			self.hash_function.update(data.encode('utf-8'))
			dataToVerify = self.hash_function.hexdigest()
		
		re = self.app.exec_query(dataToVerify)
		#re is type of subprocess.CompletedProcess
		#re.stdout have the following format
		#Query Result: [{"Record":{"hval":"VALUE-1","id":"VALUE-2"}}]

		#print("result of query: " + re.stdout)
		elements = re.stdout.split('"')
		#elements[9] ? will be ID and elements[9] will be hash value
		#if the return is emptyit may rais execption so catch the exception
		try:
			hval = elements[5]
		except IndexError:
			hval = ""
		if hval == str(dataToVerify):
			self.final_info(re, "The hash value is correct")
			return True
		else:
			#re.returncode is 0 (b.c the command is executed correctly) but the result is False, i.e don't match the input
			#re.returncode = -1
			self.final_info(re, "The hash value is not stored")
			return False

	def instantiate(self):
		
		re = self.app.exec_instantiate()
		self.final_info(re, "Chaincode instantiated")

	def create_channel(self):
		re = self.app.exec_create_channel() #os.environ["APP_CHANNEL"], os.environ["APP_CHANNEL_TX"])
		self.final_info(re, "Channel created")

	def join_channel(self):
		re = self.app.exec_join_channel()
		self.final_info(re, "Peers joined")

	def install_cc(self):
		re = self.app.exec_install_cc()
		self.final_info(re, "Chanin code installed")

	def setup_channel_and_cc(self):
		#First create channel
		re_create = self.create_channel()

		#add peers to the channel
		re_join = self.join_channel()

		#install smart contrat aka chaincode
		re_install = self.install_cc()

		#instantiate chaincode
		re_insta = self.instantiate()

		if re_create.returncode == 0 and re_join.returncode == 0 and re_install.returncode == 0 and re_insta.returncode == 0:
			return True
		else:
			return False

	#this function reads all the data at once, it is not optimal for large data
	def hash_file(self, file):
		if not Path(file).is_file():
			print("The input is not file or it doesn't exist ")
			return False
		#hash_function = hashlib.sha256()
		with open(file , 'rb') as f:
			data = f.read()
			self.hash_function.update(data)
		#return the hexadecimal digits of the hash result use .digest()	to get the byte format
		return self.hash_function.hexdigest()

	

	def final_info(self, re, msg):

		if re.returncode == 0:
			print("Command finished successfully: "+ msg)
		else:
			print("NOT Success")

	"""def add(self):
		file = self.args.f 
		rendomString = self.args.t
		init = self.args.i
		string = self.args.s

		#if not self.app.instantiate:
		#	print("The chain code is not instantiated. To see the help use --help")
		#	exit()

		if file or string: #file submited, hash the file and add it to the ledger
			
			fuction_name = "addOriginalData"
			Id = str(uuid.uuid4())

			if file:
				data = self.hash_file(file)
			else:
				self.hash_function.update(string.encode('utf-8'))
				data = self.hash_function.hexdigest() 
			args = '{"Args":["'+fuction_name+'", "'+str(Id)+'", "'+str(data)+ '"]}'
			re = self.app.exec_invoke(fuction_name, args)			
			self.final_info(re, "' "+ file +"' added successfully")

		elif rendomString: #add random string to the ledger

			fuction_name = "addOriginalData"
			Id = str(uuid.uuid4())
			
			#use this fake data simulatore
			rs = RandomString()
			#get random file
			file = rs.simulate_orignal_data()

			#hash the file
			data = self.hash_file(file)
			args = '{"Args":["'+fuction_name+'", "'+str(Id)+'", "'+str(data)+ '"]}'
			re = self.app.exec_invoke(fuction_name, args)			
			self.final_info(re, "' "+ file +"' added successfully")

		elif init: #add a pre-defined value to the ledger

			fuction_name = "initLedger"
			re = self.app.exec_init(fuction_name)
			self.final_info(re, "Pre-stored data added successfully")
		
		else:
			print("please specify file name to be added or use -t for random data or -i for predefined init data") """