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

from lc import write2Serial, readFromSerial
from threading import Thread
import threading
import printThread
import time

__author__ = "Piotr Gawlowicz, Mikolaj Chwalisz"
__copyright__ = "Copyright (c) 2015, Technische Universität Berlin"
__version__ = "0.1.0"
__email__ = "{gawlowicz, chwalisz}@tkn.tu-berlin.de"


log = logging.getLogger('wishful_agent.main')
controller = wishful_controller.Controller()
nodes = []



@controller.new_node_callback()
def new_node(node):
    nodes.append(node)
    print("GC: New node appeared:")
    print(node)


@controller.node_exit_callback()
def node_exit(node, reason):
    if node in nodes:
        nodes.remove(node);
    print("NodeExit : NodeID : {} Reason : {}".format(node.id, reason))


@controller.set_default_callback()
def default_callback(group, node, cmd, data):
    print("GC: DEFAULT CALLBACK : Group: {}, NodeName: {}, Cmd: {}, Returns: {}".format(group, node.name, cmd, data))


# need to SERIOUSLY RESEARCH ON THIS
@controller.add_callback(upis.net.get_info_of_connected_devices)
def get_info_of_connected_devices_reponse(group, node, data):
    global log
    log.info("get_info_of_connected_devices_reponse : Group:{}, NodeName:{}, msg:{}".format(group, node.name, data))
    
    
    
def write2node (node,msgTag, msgBody):
	#print("GC: Node:" + str(node.name) )
	msg={msgTag:msgBody}
	lc_name="lc_"+str(node.name)	
	lc_name = controller.node(node).hc.start_local_control_program(program=write2Serial )  
	
	
	
	
def readFromNode (node):
	#print("GC: Node:" + str(node.name) )
	
	target = controller.node(node).hc.start_local_control_program(program=readFromSerial) 

		#print("GC: {} lc started. ID: {}".format(datetime.datetime.now().time(), lc.id))	

		#lc.send({msgName:lc_name})
	
	msg = target.recv(timeout=2)
	if msg:
		print ("GC: Msg from id:"+str(target.id)+":{}".format(msg) )
		
		msgG=[{"msgTag"}]
		
		#send the received msgG to Java
		
		
	else:
		print ("GC: No msg...")#.format(datetime.datetime.now()))
		
		
		#retVal = lcpDescriptor.close()
		#print("{} Local Control Progam ID: {} was {}".format(datetime.datetime.now(), lcpDescriptor.id, retVal))

def main(args):
	log.debug(args)

	config_file_path = args['--config']
	config = None
	with open(config_file_path, 'r') as f:
		config = yaml.load(f)

	controller.load_config(config)
	controller.start()
	
	msgIter = 1000#just a global var for testing

	#control loop
	while True:
		
		#threading.active_count()
		print("\nActive Threads:{}".format(threading.active_count() ) )
		if nodes:
			for n in nodes:
				
				
				msgTag=n.name
				msgBody=n.name
				
				write2node (n,msgTag, msgBody)
				
				readFromNode(n)
				
				#lc="lc_"+n.name
				#n.name=threading.Thread(target=readFromNode,args=(n,) )
				#n.name.start()
				#print("Connected nodes:",[str(n.name)]
				#readFromNode(n)

				msgIter+=1
				print ("iter:"+str(msgIter) )
			
			gevent.sleep(5)
		else:
			print ("No node yet. Wait 5 secs...")
		gevent.sleep(5)


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
