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

#from local_control_program import my_local_control_program

#import ./coral/wishful/hierarchical_control/local_control_program #import george_local_program

from lc import lcsend
from lcReceive import  lcrec

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


	
def talk2node(node,msgName,msgIter):
	#print("GC: Node:" + str(node.name) )
	lc = controller.node(nodes[0]).hc.start_local_control_program(program=lcsend)

	#print("GC: {} lc started. ID: {}".format(datetime.datetime.now().time(), lc.id))
	
	#print ("GC: started def: talk2node" )
	print("GC :--> LC, No:{}".format(msgIter) )
	#gcMsg = "GC-->LC, No:{}".format(msgIter)

	lc.send({msgName:2})
	
	#print ("GC: started def: oneReceive")
	msg = lc.recv(timeout=2)
	if msg:
		print ("GC: Msg from lc:{}".format(msg) )
		msgG=[{"george_num"}]
		#send the received msg to Java
	else:
		print ("GC: No msg...")#.format(datetime.datetime.now()))
		

def main(args):
	log.debug(args)

	config_file_path = args['--config']
	config = None
	with open(config_file_path, 'r') as f:
		config = yaml.load(f)

	controller.load_config(config)
	controller.start()
	
	msgNum = 0
	msgIter = 1000

	#control loop
	while True:
		print("\n")
		if nodes:
			
			talk2node(nodes[0],"msgName", msgIter )
			#print("GC: msgNum No:{}".format(msgIter)  )
			msgIter+=1
			
			#getNodeMsg(nodes[0],msgNum)
			#print("msgIter No:{}".format(msgNum) ) 
			msgNum+=1
	
			#print("Connected nodes", [str(node.name) for node in nodes])
			#lcpDescriptor = controller.node(nodes[0]).hc.start_local_control_program(program=george_call)
			#print("{} Local Control Progam Started, ID: {}".format(datetime.datetime.now(), lcpDescriptor.id))
			#gcMsg = "msg from gc No "+str(msgNum)
			#print("Sending gcRandInt: "+gcMsg)
			#lcpDescriptor.send({"gcRandInt":gcMsg})

			#msg = lcpDescriptor.recv(timeout=1)
			#if msg:
			#	print ("Message from lc"+str(msg) )
			#	msgNum = msgNum + 1
			#	break
			#else:
			#	print ("{} no msg received".format(datetime.datetime.now()))

			#retVal = lcpDescriptor.close()
			#print("{} Local Control Progam ID: {} was {}".format(datetime.datetime.now(), lcpDescriptor.id, retVal))
			gevent.sleep(10)
		else:
			print ("no node connected yet... sleeping for 10 secs...")
		gevent.sleep(10)


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
