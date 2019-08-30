#!/usr/bin/python3

import os, subprocess
import shutil, docker
from variables import *


class App:

	EnvVars = None
	instantiate = False
	def __init__(self):
		self.EnvVars = variables()
		 

	def run_command(self, command):
		#TODO what if the App is called from outside of the container
		# check if currect execution is inside the container (i.e check if peer command exists)
		# if not get the name of the cli container, and append 'docker exec -it <container_id_or_name>' before the given command
		peer_command = shutil.which("peer") # returns the path if it exist or none if not

		if not peer_command: 
			# peer command not found so append the prifix 'docker exec -it <container_id_or_name>' to the command

			cli_container = self.get_container("cli")
			if not cli_container:
				# cli container not running
				# print error and exit
				print("CLI containner is not running")
				return None
			
			# if cli is running attache the prefix
			command = "docker exec -it " + cli_container+ " " + command

		#command to be executed, PIPE will help to read data from the process, universal new line makes the return value a string (the default is bytes sequence)
		re = subprocess.run([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
		if re.returncode != 0:
			print("The command exits with non zero return code: " + str(re.returncode))
			print("Error: " + re.stderr)
		else:
			return re				

	
	#method to add original data to the chain
	def exec_invoke(self, fuction_name, args):
		#export org and peer specific env vars
		self.EnvVars.set_env_org_peer(2, 1)
		#set some remaining env variables
		self.EnvVars.set_invoke_arg(args)
		command = 'peer chaincode invoke -o "' + self.EnvVars.ORDERER_URL+ '" -C "'+ self.EnvVars.APP_CHANNEL+'" -n "'+ self.EnvVars.CC_NAME+'" -c \''+ self.EnvVars.CC_INVOKE_ARGS +'\'  --tls '+ self.EnvVars.CORE_PEER_TLS_ENABLED +' --cafile '+ self.EnvVars.ORDERER_TLS_CA
		print(command)
		#os.system(command)
		return self.run_command(command)


 	#method to call initLedger method
	def exec_init(self, function_name="initLedger"):
		#self.EnvVars.set_env_general()
 		#initLedger requires no arg just pass the fuction name
		args = '{"Args":["'+function_name+'"]}'
		self.EnvVars.set_invoke_arg(args)
		self.EnvVars.set_env_org_peer(2, 1)
		command = 'peer chaincode invoke -o "' + self.EnvVars.ORDERER_URL+ '" -C "'+ self.EnvVars.APP_CHANNEL+'" -n "'+ self.EnvVars.CC_NAME+'" -c \''+ self.EnvVars.CC_INVOKE_ARGS +'\'  --tls '+ self.EnvVars.CORE_PEER_TLS_ENABLED +' --cafile '+ self.EnvVars.ORDERER_TLS_CA
		print(command)
		#os.system(command)
		return self.run_command(command)
		
	#method to call queryOriginalData method
	def exec_query(self, index):
		fuction_name = "queryByHashValue"
		args = '\'{"Args":["'+fuction_name+'", "'+str(index)+'"]}\''

		#export org and peer specific env vars
		self.EnvVars.set_env_org_peer(2, 1)
		self.EnvVars.set_query_arg(args)

		command = 'peer chaincode query -C "'+ self.EnvVars.APP_CHANNEL+'" -n "'+ self.EnvVars.CC_NAME+'" -c '+ self.EnvVars.CC_QUERY_ARGS
		print(command)
		#os.system(command)
		return self.run_command(command)
		
	#method to instantiate the chaincode
	def exec_instantiate(self):
		self.EnvVars.set_env_general()
		#export org and peer specific env vars
		self.EnvVars.set_env_org_peer(2, 1)
		#self.EnvVars.set_instantiate_arg(args)
		command = 'peer chaincode instantiate -o "' + self.EnvVars.ORDERER_URL+ '" -C "'+ self.EnvVars.APP_CHANNEL+'" -n "'+ self.EnvVars.CC_NAME+'"  -v '+ str(self.EnvVars.CC_INIT_VERSION)   +' -c '+ self.EnvVars.CC_INIT_ARGS +'  --tls '+ self.EnvVars.CORE_PEER_TLS_ENABLED +' --cafile '+ self.EnvVars.ORDERER_TLS_CA + ' -P "OR (\'Org1MSP.member\',\'Org2MSP.member\')"'
		print(command)
		#os.system(command)
		re = self.run_command(command)
		self.instantiate = True
		return re

	def exec_create_channel(self):
		#export all env vars 
		for k, v in self.EnvVars.__dict__.items():
			self.EnvVars.export_locals(k,v)

		name = os.environ["APP_CHANNEL"]
		ch_conf_tx = os.environ["APP_CHANNEL_TX"]
		self.EnvVars.set_env_org_peer(2, 1)

		if os.environ["CORE_PEER_TLS_ENABLED"] == 'false':
			command = "peer channel create -o " + self.EnvVars.ORDERER_URL+" -c "+ name +" -f " + self.EnvVars.CHANNEL_ARTIFACTS+"/" + ch_conf_tx+" --timeout "+ self.EnvVars.TIMEOUT
		else:
			command = "peer channel create -o " + self.EnvVars.ORDERER_URL +" -c "+ name +" -f " + self.EnvVars.CHANNEL_ARTIFACTS+"/" + ch_conf_tx +" --timeout "+ self.EnvVars.TIMEOUT + " --tls " + self.EnvVars.CORE_PEER_TLS_ENABLED +" --cafile "+ self.EnvVars.ORDERER_TLS_CA
		print(command)
		re = self.run_command(command)
		return re
	
	def exec_join_channel(self):
		re = None
		for org in range(self.EnvVars.ORGS):
			for peer in range(self.EnvVars.PEERS):
				self.EnvVars.set_env_org_peer(org+1, peer)
				command = "peer channel join -b "+self.EnvVars.APP_CHANNEL+".block"
				print(command)
				re = self.run_command(command)
				if re.returncode == 0:
					print("Peer "+ str(peer) + " of Org "+ str(org) +"joined")
		return re

	def exec_install_cc(self):

		re = None
		for org in range(self.EnvVars.ORGS):
			for peer in range(self.EnvVars.PEERS):
				self.EnvVars.set_env_org_peer(org+1, peer)
				command = 	"peer chaincode install -n "  + self.EnvVars.CC_NAME + " -v " + str(self.EnvVars.CC_INIT_VERSION)   + " -p " + self.EnvVars.CC_PATH
				print(command)
				re = self.run_command(command)
				if re.returncode == 0:
					print("Chaincode installed on Peer "+ str(peer) + " of Org "+ str(org))
		return re

	def get_container(self, prefix):
		name = None
		client = docker.from_env()
		containers = client.containers.list()
		for c in containers:
			if prefix in c.name:
				name = c.name
				return name
		return name


								
	
		

