#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
wishful_controller_simple.py: First implementation of WiSHFUL controller

Usage:
   wishful_controller_simple.py [options] [-q | -v]

Options:
   --logfile name      Name of the logfile
   --config configFile Config file path

Example:
   ./wishful_simple_local_controller -v --config ./config.yaml 

Other options:
   -h, --help          show this help message and exit
   -q, --quiet         print less text
   -v, --verbose       print more text
   --version           show version and exit
"""

import sys
import datetime
import logging
import random
import wishful_controller
import gevent
import yaml
import wishful_upis as upis
import json
import time
import socket
import json

#from lc import write2Serial, readFromSerial
from lc import coral_lc
from threading import Thread
import threading



__author__ = "Piotr Gawlowicz, Mikolaj Chwalisz"
__copyright__ = "Copyright (c) 2015, Technische Universität Berlin"
__version__ = "0.1.0"
__email__ = "{gawlowicz, chwalisz}@tkn.tu-berlin.de"


#connection to Java Socket Server Status
conJSS=False


#========= Java Socks Client ====================================================
def javaSSConnection():
	global conJSS
	global sockClient

	# Server IP or name and port
	HOST = "localhost"
	PORT = 8999
	# Connect to the port on the server provided by the caller if you wish
	server_address=(HOST, PORT)

	#reset the connection if it exists...
	try:
		if sockClient:
			sockClient.close()
	except Exception as e:
		print("sockClient closing error:"+str(e) )

	# Create a TCP/IP socket
	sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	
	while not conJSS:
		try:
			print ("Trying to connect to JSS: " + HOST +":" + str(PORT) )
			sockClient.connect(server_address)
			#connection is NON-Blocking. If else the program halts in sockClient.recv()
			sockClient.setblocking(0) 
			print("\n...Connected to Java Socket Server (JSS)...") 
			conJSS=True
		except:# ??? Do we need to GC to wait 4 ever for the Java Server?
			print("No Java Server, waiting 5 secs...")
			time.sleep(5)
#=== it will wait here 4 ever until Java Socks Server (JSS) is found ============


log = logging.getLogger('wishful_agent.main')
controller = wishful_controller.Controller()
nodes = []
lcs = ""
lcList= []

@controller.new_node_callback()
def new_node(node):
	nodes.append(node)
	print("GC: New node appeared. Node.id=:"+node.id)

@controller.node_exit_callback()
def node_exit(node, reason):
	if node in nodes:
		nPos= nodes.index(node)
		print("Node leaving index:"+str(nPos) )
		del lcList[nPos] # remove the lc object
		nodes.remove(node);
		#lcList.remove(nodes.index(node) )
	print("NodeExit : NodeID : {} Reason : {}".format(node.id, reason))

# To Do: How to call this ???
@controller.set_default_callback()
def default_callback(group, node, cmd, data):
    print("GC: DEFAULT CALLBACK : Group: {}, NodeName: {}, Cmd: {}, Returns: {}".format(group, node.name, cmd, data))


# need to SERIOUSLY RESEARCH ON THIS
@controller.add_callback(upis.net.get_info_of_connected_devices)
def get_info_of_connected_devices_reponse(group, node, data):
    global log
    log.info("get_info_of_connected_devices_reponse : Group:{}, NodeName:{}, msg:{}".format(group, node.name, data))
    print ("get_info_of_connected_devices_reponse : Group:{}, NodeName:{}, msg:{}".format(group, node.name, data))
    

def main(args):
	global lcs, conJSS
	log.debug(args)

	config_file_path = args['--config']
	config = None
	with open(config_file_path, 'r') as f:
		config = yaml.load(f)

	controller.load_config(config) #load the yaml config file
	controller.start() #start the Global Controller (GC)

	

	
	msgTag="CtrlMsg" # ??? JSON logic. Not implemented yet
	
	printWaitNodesMsg=True # Just to control the on screen messages...
	
#=== it will remain here 4 ever until JSS appears===================
	javaSSConnection()
	
	#testing connection with JSS. Can be safely ommited
	sockClient.sendall(bytes ("Just testing. Ignore"+"\n", 'UTF-8') )
	print("\nSent a test msg to JSS\n")
		
	#control loop
	while conJSS:
		if nodes: # All the following will happen ONLY if at least one node exists
			for n in nodes:
				#eachNodePos=nodes.index(n) # position in nodes, of each node
				eachNodePos=0 # ?????
#========= Create an lc if it does not exist, and put in lc_array_position==node_array_pos ===
				try:
					lcList[eachNodePos] # if the particular lc exists, don't create it again

#=========== Waiting to receive from ANY lc (if any) ==========================
					msg = lcList[eachNodePos].recv(timeout=1)	

					if msg:
						j=json.loads( str(msg) )
						#lc_node=j['']
						print ("GC: Received msg from LC_id:"+str(lc.id))# +", msg: "+j )

						#msgG=[{"myChannel"}] #????? JSON Logic NOT implemented yet
						#msg={msgG}
#==============================================================================

						
#========== Send the received msgG to JSS ======================================
						try:
							sockClient.sendall( bytes(str(j),'UTF-8' ) )
							#sockClient.sendall(bytes("lc.id:"+str(lc.id)+" "+msgString+"\n",'UTF-8') ) 
							print ("msg sent to JSS: " + str(j) )
						except Exception as e:
							print("Error sending to JSS:"+str(e) )
							print("\nJSS disappeared :-(, try to reconnect")	
							#if the connection was reset close the connection and reconnect
							#javaSSConnection() # it does not work ???
							#conJSS=False
							#pass
#===============================================================================
						
				except IndexError: #so it creates ONLY one instance of lc 4 each node
					try:
						lc = controller.node(n).hc.start_local_control_program(program=coral_lc )
						lcList.insert(eachNodePos,lc)    # add it to the lc list SPECIFIC n index				
						print("Created new LC in: lcList["+str(eachNodePos)+"]")
					except Exception as e:
						print("lc creating error: "+str(e))
#===============================================================================================
			
#======== Waiting for JSS to send something (sockClient is set to non blocking) ====================
			socksMsg=""
			current=""
			try:
				current = sockClient.recv(1024) #waiting for the Socks Server to send something
			except Exception as e:
				pass
				#print ("sockClient: "+str(e) )	#annoying repeated message because of time-outs
				
			if current:# if something was received from JSS
				data=json.loads(current.decode('utf-8') ) # Everything is sent in JSON format
				lc_node=data["LC"] # specific node to sent the message to
				lc_msg=data["Msg"]
#========== the particular node(s) will come from JSS ==============
				#nPos =0 #= nodes[n]  # ????? THe JSS message is suppose to set the n number !!!
				#node =nodes.index(node.id) #?????
				#node = nodes[0]
#===================================================================

				print("\nHURRAY! I got a message from JSS...\n")
				print ("to LC:"+lc_node+", Msg: "+lc_msg)

#================ Send the message to the particular lc ============					
				try:
					if (lc_node=="ALL"): # Broadcast message
						for length in range(0, len(lcList) ):
							lcList[length].send({"Msg":lc_msg})
					else: # only specific node
						lcList[int(lc_node)].send({"Msg":lc_msg}) #only send if JSS sent something
					
					current = "" # just clear contents for next iteration
				except Exception as e:
					print ("Error sending:"+str(e) ) #repeated annoying message	
#==================================================================
				

#===================================================================================================			

			#gevent.sleep(5)
		else: #if nodes
			if printWaitNodesMsg:
				print ("\nNo node yet. Probing every 5 secs...")
				printWaitNodesMsg= False # it will print the above message only once...
		gevent.sleep(5)
	
	javaSSConnection() 
			
	#controller.stop()  
	#print(("GC: {} - STOPPED".format(controller.name)))  
	

if __name__ == "__main__":
	try:
		from docopt import docopt
	except:
		print("""
		Please install docopt using:
			pip install docopt==0.6.1
		For more refer to:
		https://github.com/docopt/docopt
		""")
		raise

	args = docopt(__doc__, version=__version__)

	log_level = logging.INFO  # default
	if args['--verbose']:
		log_level = logging.DEBUG
	elif args['--quiet']:
		log_level = logging.ERROR

logfile = None
if args['--logfile']:
	logfile = args['--logfile']

logging.basicConfig(filename=logfile, level=log_level,
	format='%(asctime)s - %(name)s.%(funcName)s() - %(levelname)s - %(message)s')

try:
	main(args)
except KeyboardInterrupt:
	log.debug("Controller exits")
finally:
	log.debug("Exit")
	controller.stop()
