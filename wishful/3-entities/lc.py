__author__ = "George Violettas, Tryfon Theodorou"
__copyright__ = "Copyright (c) 2016, University of Macedonia, Greece"
__version__ = "1.0.0"
__email__ = "georgevio@gmail.com, tryfonthe@gmail.com"


#Definition of Local Control Program
def coral_lc(controller):
    #do all needed imports here!!!
	import time
	import datetime
	from write2anyPort import writeThis
	from readFromSerial import StartRead, readPort,StartReadThread
	from getPTSports import get1stpts

	# Remember: this method is called automatically when this "program" is called by the GC
	@controller.set_default_callback()
	def default_callback(cmd, data):
		print(("{} DEFAULT CALLBACK : Cmd: {}, Returns: {}".format(datetime.datetime.now(), cmd, data)))
		print ("Reading from serial port: "+ptsPort)
		print("this is the set_default_callback method print...")

		# example of a UPI call logic
		#result = controller.radio.iface("wlan0").get_channel()


# ????????????????????????????????????????????????????????????????????????????????????????

# how do we call this ??????????
# for the moment, it is NOT WORKING !!!!!
#====== Reading from UART (Serial port) and send it to GC ==========================
		#answer=readPort(ptsPort, 115200)
		#if  answer:
		#	print ("Sending to GC:"+str(answer) )
		#	controller.send_upstream({"myChannel":answer})    
#==================================================================================			    


#====== Serial Port Discovery (Contiki, Cooja, etc.) =================================
	times2print=1
	portOk = False
	while not portOk:
		try:
			ptsPort=get1stpts()
			portOk=True
		except Exception as e:
			if times2print%40==0 or times2print==1: # just prints less error messages
				print ("\nUART Problem: "+str(e))
				print("Will retry every 5 secs, 4 ever")
			time.sleep(5) 
			times2print+=1
#====================================================================================

	# BE CAREFUL: This message sould be printed ONLY ONCE (One thread only...)
	print(("\nLC- Name: {}, Id: {} - STARTED".format(controller.name, controller.id)))
		
	# Controlling the on screen waiting messages to print only once...
	printMsgWaiting = True #just filtering too many waiting messages
	printUARTAnswer = True

#====== Reading from UART (Serial port) and send it to GC ==========================			
	try:
		print("waiting tor read something started")
		StartReadThread(ptsPort, 115200, controller)	
	except Exception as e:
		print ("UART read error: "+str(e))
#====================================================================================
	 
	#control loop
	while not controller.is_stopped():

#====== Waiting to receive from GC (4 ever): this is a non blocking call ===========
		receivedMsg = controller.recv(timeout=1)
		if receivedMsg:
			Msg = receivedMsg["Msg"]         
			print ("\nOOOUPS ! A MESSAGE JUST ARRIVED FROM GC: " + str(Msg))
#===================================================================================

#=========== Write to UART - Serial  Port============================================ 
			try:
				writeThis(ptsPort,115200, str(Msg) ) 
			except Exception as e:
				print ("UART problem: "+str(e) )
#====================================================================================
	 
	 
			printMsgWaiting =True
		else:
			if printMsgWaiting: # just prints less error messages
				print("LC: Waiting for message from GC")# It will print this only once
				printMsgWaiting = False 


      		   
	print(("Local Control Program - Name: {}, Id: {} - STOPPED".format(controller.name, controller.id)))
