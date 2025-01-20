from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient
import json
import numpy as np
import pickle
from util.json2dataseries import j2ds

# Configuration
RECEIVE_IP = "127.0.0.1"  # IP to listen for incoming messages
RECEIVE_PORT = 8000       # Port to listen on
SEND_IP = "127.0.0.1"     # IP to send OSC messages to
SEND_PORT = 7400          # Port to send OSC messages to

# Initialize OSC client for sending messages
osc_client = SimpleUDPClient(SEND_IP, SEND_PORT)

# load the model and standardscaler
pos_class_gesture = ''#'M_openhands'
filename = '_mlp_demo2.sav'
print(filename)
model = pickle.load(open(filename, 'rb'))
filename = '_scaler_demo2.sav'
scaler = pickle.load(open(filename, 'rb'))

# Callback function for incoming messages
previous = 0
def process_message(address, json_string):
    """
    Process incoming OSC messages and send a response.
    :param address: The OSC address of the message.
    :param args: Arguments of the OSC message.
    """

    global previous
    dictionary = json.loads(json_string)
    raw_data = j2ds(dictionary)

    #scale the data
    raw_data = scaler.transform([raw_data])
    #predict the data
    #print("scaled", raw_data)
    prediction = model.predict(raw_data)
    print('prediction',prediction)

    #print("Trigger received, sending response...")
    if prediction[0] != previous:
        osc_client.send_message("/signal", prediction[0])
        previous = prediction[0]



# Set up the dispatcher for message handling
dispatcher = Dispatcher()
dispatcher.map("/dictData", process_message)  # Map all incoming messages to the callback function

# Create the server
server = osc_server.ThreadingOSCUDPServer((RECEIVE_IP, RECEIVE_PORT), dispatcher)

if __name__ == "__main__":
    print(f"Starting OSC server on {RECEIVE_IP}:{RECEIVE_PORT}")
    print(f"Sending responses to {SEND_IP}:{SEND_PORT}")
    try:
        # Start the server
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
