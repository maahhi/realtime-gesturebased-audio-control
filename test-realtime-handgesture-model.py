# open osc connection to receive messages
from pythonosc import dispatcher
from pythonosc import osc_server
import json

# Define the IP and port to listen on
ip = "127.0.0.1"  # Localhost (or change to your local IP for external connections)
port = 8000       # Port must match what is set in Max MSP


#load the model and standard scaler
import joblib

mlpmodel = joblib.load('mlp.pkl')
scaler = joblib.load('scaler.pkl')

import datetime
# Define a handler function to process incoming OSC messages
quitFlag = False
samples = 0

first_call = True
first_call_time = None

def quit_message_handler(address, *args):
    global quitFlag
    quitFlag = True
    #get timestamp
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    # time difference between first and now
    print('samples',samples)
    print('time difference',now - first_call_time)
    print('rate',samples/(now - first_call_time).total_seconds())
    print("QUITTING!")

def json_dict_handler(address, json_string):
    global first_call
    global first_call_time
    global samples
    samples += 1
    if first_call:
        first_call = False
        first_call_time = datetime.datetime.now()

    # Decode the JSON string back into a dictionary
    dictionary = json.loads(json_string)
    #print("Received dictionary:", dictionary)
    #make a X sample
    X = []
    print('.')
    #print('keys',len(dictionary.keys()))
    if len(dictionary.keys()) > 0:
        RLvalues = dictionary[list(dictionary.keys())[0]]
        #print('keys', len(RLvalues.keys()))
        for k in list(RLvalues.keys()):
            if k == 'Gestures':
                continue
            X.append(RLvalues[k]['x'])
            X.append(RLvalues[k]['y'])
        #print(X)
        #scale the X sample
        X = scaler.transform([X])
        #predict the gesture
        predict = mlpmodel.predict(X)
        #print the value as following 'Closed_Fist':0,'Open_Palm':1,'None':2,
        #print("predict: ", predict)
        if predict == 1:
            print("++++++++++++++++++++++++++++++++Open_Palm")






# Set up the dispatcher to map the OSC address to the handler
disp = dispatcher.Dispatcher()
disp.map("/dictData", json_dict_handler)  # Must match the OSC address set in Max
disp.map("/quit*", quit_message_handler)

# Start the server to listen for incoming OSC messages
server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
print(f"Listening on {ip}:{port}")

while not quitFlag:
    server.handle_request()
# Keep the server running
#server.serve_forever()

