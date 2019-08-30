#!/usr/bin/python3
 
import argparse, sys
from pathlib import Path
from DataInt import *
sys.path.append('../')

parser = argparse.ArgumentParser(description='Tool to detect integrity failure')

parser.add_argument('action', metavar='Action', help=' it can be  either "add" , "verify", "instantiate" or createChannel. This will indicate the action to be performed')
parser.add_argument('-f', '--file', metavar='File name', help='This file will be used to perform the specified action (i.e will be added to the chain or checked if it is still correct).')
parser.add_argument('-r', '--random', action='store_true', help='this will genrate random string to store in the chain')
parser.add_argument('-i', action='store_true', help='this will add a predefined values to the chain. the values are defined inside "initLedger" function')
parser.add_argument('-s', '--string', metavar='String', help='The string will be used to perform the specified action (i.e will be added to the chain or checked if it is still correct).')


		
if __name__ == "__main__":

	
	args = parser.parse_args()
	DI = DataInt()

	action = args.action

	if action == "add":
		
		file = args.f 
		randomString = args.r
		init = args.i
		string = args.s

		if file:
			# call add with data, datatype
			DI.add(file, "file")

		elif string:
			DI.add(string, "string")

		elif randomString:
			DI.add(datatype="random")

		elif init:
			DI.add(datatype="init")
		
		else:
			print("Error: Unknown data type to add. for more info see --hlep")

	elif action == "verify":
		file = args.f
		string = args.s

		if file:
			DI.verify(file, "file")
		
		elif string:
			DI.verify(string, "string")

		else:
			print("Error: Unknown data type to verify. for more info see --hlep")

	elif action == "instantiate":
		DI.instantiate()

	elif action == "createChannel":
		DI.create_channel()

	elif action == "joinChannel":
		DI.join_channel()

	elif action == "install":
		DI.install_cc()

	elif action == "setup":
		DI.setup_channel_and_cc()
		
#call the invoke
#for i in range(100):
#        exec_invoke()