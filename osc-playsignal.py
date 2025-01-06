from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient
import json
import numpy as np
import pickle

# Configuration
RECEIVE_IP = "127.0.0.1"  # IP to listen for incoming messages
RECEIVE_PORT = 8000       # Port to listen on
SEND_IP = "127.0.0.1"     # IP to send OSC messages to
SEND_PORT = 7400          # Port to send OSC messages to

# Initialize OSC client for sending messages
osc_client = SimpleUDPClient(SEND_IP, SEND_PORT)

# load the model and standardscaler
pos_class_gesture = 'right_hand_up'#'M_openhands'
filename = pos_class_gesture + '_mlp.sav'
model = pickle.load(open(filename, 'rb'))
filename = pos_class_gesture + '_scaler.sav'
scaler = pickle.load(open(filename, 'rb'))

# Callback function for incoming messages
def process_message(address, json_string):
    """
    Process incoming OSC messages and send a response.
    :param address: The OSC address of the message.
    :param args: Arguments of the OSC message.
    """
    global model, scaler
    pairs = ['shoulder', 'elbow', 'wrist', 'pinky', 'index', 'hip', 'knee', 'heel', 'foot_index']
    columns = ['nose'] + ['left_' + l for l in pairs] + ['right_' + r for r in pairs]
    #remove these items from columns
    removeitems = ['left_foot_index','left_heel','left_pinky',"left_index",'right_foot_index','right_heel','right_index','right_pinky']
    for item in removeitems:
        if item == 'left_foot_index':
            continue
        if item == 'right_foot_index':
            continue
        columns.remove(item)

    dictionary = json.loads(json_string)
    print(dictionary)
    raw_data = np.zeros(2*len(columns))
    new_features = np.zeros(2*4) # ['left_index_heel', 'left_pinky_index', 'right_index_heel', 'right_pinky_index']
    #index_heel = foot_index + heel
    #pinky_index = pinky + index

    for LRN in dictionary:
        for bodypart in dictionary[LRN]:
            if bodypart in removeitems:
                index = removeitems.index(bodypart)
                index = index//2
                new_features[2*index] = dictionary[LRN][bodypart]['x']
                new_features[2*index+1] = dictionary[LRN][bodypart]['y']
            if bodypart in columns:
                index = columns.index(bodypart)
                raw_data[2*index] = dictionary[LRN][bodypart]['x']
                raw_data[2*index+1] = dictionary[LRN][bodypart]['y']
    #devide all newfeatures by 2
    new_features = new_features/2
    #append new features to raw_data
    raw_data = np.append(raw_data,new_features)
    #print(raw_data)
    #scale the data
    raw_data = scaler.transform([raw_data])
    #predict the data
    prediction = model.predict(raw_data)
    print('prediction',prediction)

    #print("Trigger received, sending response...")
    if prediction[0] == 2:
        print("Sending signal")
        osc_client.send_message("/signal", prediction[0])


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
