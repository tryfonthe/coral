#!/usr/bin/python

import serial, glob
import getPTSports

ttyFound = []
usbFound = []
ptsFound = []

ttyPorts = []
usbPorts = []
ptsPorts = []


def getttyPorts():
    for tty in glob.glob('/dev/tty*'): 
        ttyFound.append(tty)
    probePort(ttyFound, ttyPorts)
    if ttyPorts:
		return ttyPorts # ATTENTION: returning ALL tty ports. NEEDS BIIIIIIG CONSIDERATION
    else:
    	pass 

#search ONLY USB ports..... (e.g. look for zolertia )
def getUSBPort():    
    for usb in glob.glob('/dev/ttyUSB*'): 
        usbFound.append(usb)
	probePort(usbFound, usbPorts)
	if usbPorts[1]:
	    return usbPorts[1] # ATTENTION: returning USB1 where zolertia was found. THIS NEEDS BIIIIIIG CONSIDERATION
    else:
        pass 

#search ONLY tty ports ... (cooja simulated serial2pty)
#ATTENTION: Returns a list
def getptsPorts():
    for pts in getPTSports.getAllpts():
    	print ( port + " found" )
        ptsFound.append(pts)
	probePort(ptsFound, ptsPorts)
	return ptsPorts # ATTENTION: returning many pty ports.!!!


#call this internaly to find all active ports of a specific type   
def probePort(portList, activePorts):        
	for port in portList:
		try:
			s = serial.Serial(port)
			s.close()
			activePorts.append(port)
			print ( port + " appended" )
		except Exception: 
			pass

def printAll():
	print ("Printing all ports found, if any:" + "\n" )
	for t in ttyPorts:
		print ("ttyPorts: " + str(t) )
	for p in usbPorts:
		print ("usbPorts: " + str(p) )
	for pt in usbPorts:
		print ("ptsPorts: " + str(pt) )

if __name__ == '__main__':
	printAll()
    
