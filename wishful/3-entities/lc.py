__author__ = "Piotr Gawlowicz"
__copyright__ = "Copyright (c) 2015, Technische Universitat Berlin"
__version__ = "0.1.0"
__email__ = "gawlowicz@tkn.tu-berlin.de"

def testMe():
    print ("testMe:")
    
#Definition of Local Control Program
def lcsend(controller):
    #do all needed imports here!!!
    import time
    import datetime

    msgNum = 112

    @controller.set_default_callback()
    def default_callback(data):
        print(("\nLC: {}, Id: {} - STARTED".format(controller.name, controller.id)))

    print(("\nLC: {},Id: {}-STARTED".format(controller.name, controller.id)))
        
    while  True:
        if not controller.is_stopped(): #and msgNUm<300):
            gcMsg = controller.recv(timeout=2)
            if gcMsg: #gcMsg is an array of two fields tuples
                #msg2print = gcMsg["msgName"]#multifields messages
                print("LC: received from gc: {}".format(gcMsg) )
                
                #send to UART port 
                
                #do this with threads ?????????????
                # so you can send 3 msgs togheter    
                up_message = "LC-->GC"
                controller.send_upstream({"george_num" :up_message})
            else:
                time2wait=5
                print(("LC: No msg. Wait: {}s".format(time2wait)))
                time.sleep(time2wait)
        else:
            print ("lc is not started...")
            time.sleep(5)
            #break
                
    controller.stop()  
    print(("LC: {}, Id: {} - STOPPED".format(controller.name, controller.id)))  
            
