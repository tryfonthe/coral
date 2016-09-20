__author__ = "Piotr Gawlowicz"
__copyright__ = "Copyright (c) 2015, Technische Universitat Berlin"
__version__ = "0.1.0"
__email__ = "gawlowicz@tkn.tu-berlin.de"

def write2Serial(controller):

	#do all needed imports here!!!
	import time
	import datetime
	
	while True:
		if not controller.is_stopped():#this is the LC
			gcMsg = controller.recv(timeout=2)
			if gcMsg: #gcMsg is an array of two fields tuples
				#msg2print = gcMsg["msgName"]#multifields messages
				print("LC: received from gc: {}".format(gcMsg) )
				
				
				
				#send to UART port 
		
		
		
								

				
				
			else:
				time2wait=5
				print(("LC: No msg. Wait: {}s".format(time2wait)))
				time.sleep(time2wait)
		else:
			print ("no GC contact...")
			time.sleep(5)
						
	#controller.stop()  
	#print(("LC: {}, Id: {} - STOPPED".format(controller.name, controller.id)))  
	
	
	
						
#Definition of Local Control Program
def readFromSerial(controller):
	#do all needed imports here!!!
	import time
	import datetime

	msgNum = 112

	@controller.set_default_callback()
	def default_callback(data):
		print(("\nLC: {}, Id: {} - STARTED".format(controller.name, controller.id)))

	print(("\nLC: {},Id: {}-STARTED".format(controller.name, controller.id)))
		
	while  True:
		if not controller.is_stopped():
			
			#wait for ser port to answer...
			#get an answer from the serial port

			msgTag="msgTag"
			msgBody=controller.id#"msgBody"
			
			if (msgTag=="msgTag"):	                
				controller.send_upstream({msgTag:msgBody})#send to GC
			else:
				time2wait=5 #can we wait via the thread ???
				print(("LC: No msg. Wait: {}s".format(time2wait)))
				time.sleep(time2wait)
		else:
			print ("no GC contact. Sleep for 5s...")
			time.sleep(5)
				
	controller.stop()  
	print(("LC: {}, Id: {} - STOPPED".format(controller.name, controller.id)))  
			
