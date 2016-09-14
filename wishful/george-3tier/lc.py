__author__ = "Piotr Gawlowicz"
__copyright__ = "Copyright (c) 2015, Technische Universitat Berlin"
__version__ = "0.1.0"
__email__ = "gawlowicz@tkn.tu-berlin.de"

#Definition of Local Control Program
def george_call(controller):
    #do all needed imports here!!!
    import time
    import datetime

    @controller.set_default_callback()
    def default_callback(data):
        print(("received data from gc: {}". data))
        up_message = "msg from lc 2 gc "
        controller.send_upstream({"george_num" :up_message})

    #control loop
    print(("\nprogram Name: {}, Id: {} - STARTED".format(controller.name, controller.id)))
    while not controller.is_stopped():
        gcMsg = controller.recv(timeout=1)
        if gcMsg:
            msg2print = gcMsg["gcRandInt"]
            print("received from gc : "+ msg2print)

            print ("wait for 1 sec and then send back a msg")
            time.sleep(1)

            up_message = "msg from lc 2 gc "
            controller.send_upstream({"george_num": up_message})

        else:
            print(("{} lc Waiting for 5 secs".format(datetime.datetime.now())))
            time.sleep(5)

    print(("Local Control Program - Name: {}, Id: {} - STOPPED".format(controller.name, controller.id)))
