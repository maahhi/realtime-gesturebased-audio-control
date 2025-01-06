import time

from pythonosc import osc_message_builder
from pythonosc import udp_client
#!pip install python-osc
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import pandas as pd
from mapping import use_model
import csv



def pass_to_model(samples, _mode='train'):
    return use_model(samples, mode=_mode)


# Function to send a response back to the client
def send_response_to_client(msg):
    client = udp_client.SimpleUDPClient('127.0.0.1', 1416)  # Replace with actual client IP and port
    msg = osc_message_builder.OscMessageBuilder(address="/response")
    msg.add_arg("This is a response message")
    message = msg.build()

    client.send(message)
    print("Response message sent back to the client")

#global template
#global samplestruct
#global sample
template = {"Relbow":{ "x":[], "y":[], "z":[]},
 "Rwrist":{ "x":[], "y":[], "z":[]},
 "Rshoulder":{ "x":[], "y":[], "z":[]},
 "Lelbow": { "x":[], "y":[], "z":[]},
 "Lwrist": { "x":[], "y":[], "z":[]},
 "Lshoulder": { "x":[], "y":[], "z":[]}}
samplestruct = template.copy()
all_samples = []
sample = []
df = pd.DataFrame()
if __name__ == '__main__':
    # used to quit osc_receiver
    ##################################################################
    ##################################################################
    ########### OSC MESSAGE HANDLERS #################################
    ##################################################################
    ##################################################################
    #  Values received from sliders or numboxes will be stored/updated
    #       in the dedicated lists: slider_values and num_box_values
    #       if you need more than 10 sliders, increase the length of
    #       the default lists in lines 101-102
    #
    #  The methods slider_message_handler and num_box_message_handler
    #       are in charge of updating the slider_values and num_box_values
    #       lists using the corresponding received osc messages

    quitFlag = False

    # Lists for storing slider and nbox values
    quitFlag = [quitFlag]

    # connection parameters
    ip = "127.0.0.1"
    receiving_from_port = 1415

    # dispatcher is used to assign a callback to a received osc message
    # in other words the dispatcher routes the osc message to the right action using the address provided
    dispatcher = Dispatcher()



    # define handler for messages starting with /nbox/[nbox_id]
    def num_box_message_handler(address, *args):
        global sample
        global samplestruct
        #print("address: ", address, "args: ", args)
        _, _, bodypart , xyz =address.split("/")
        #print("bodypart: ", bodypart, "xyz: ", xyz)
        cordination = args[0]
        print("cordination: ", cordination)
        sample.append(cordination)
        samplestruct[bodypart][xyz].append(cordination)
        #when its the test/use phase pass the sample struct to the machine learning model


    def quit_message_handler(address, *args):
        quitFlag[0] = True
        print(all_samples)
        print("QUITTING!")

    def new_sample(address, *args):
        print("new_sample_handler")
        global sample
        global samplestruct
        global all_samples
        if len(sample) >0 :
            print('sample will empty now')
            all_samples.append(samplestruct)
            # when its the test/use phase pass the sample struct to the machine learning model
            predict = pass_to_model(samplestruct,'test')
            print("predict: ", predict)
            send_response_to_client(predict)
            sample.clear()
            print('len sample',len(sample))
            pass





    # pass the handlers to the dispatcher
    dispatcher.map("/pos*", num_box_message_handler)
    dispatcher.map("/quit*", quit_message_handler)
    dispatcher.map("/newsample*", new_sample)



    # you can have a default_handler for messages that don't have dedicated handlers
    def default_handler(address, *args):
        print(f"No action taken for message {address}: {args}")
    dispatcher.set_default_handler(default_handler)

    # python-osc method for establishing the UDP communication with pd
    server = BlockingOSCUDPServer((ip, receiving_from_port), dispatcher)

    ##################################################################
    ##################################################################
    ########### MAIN CODE HERE #######################################
    ##################################################################
    ##################################################################

    while (quitFlag[0] is False):
        server.handle_request()
print(all_samples)
import json

# Assuming your object is called `data`
with open('data.json', 'w') as file:
    json.dump(all_samples, file)