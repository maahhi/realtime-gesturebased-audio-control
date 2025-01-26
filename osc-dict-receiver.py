from pythonosc import dispatcher
from pythonosc import osc_server
import json
import os
from util.json2dataseries import j2ds
import pandas as pd


samples = [] # This variable is global as it is used both json_dict_handler and save_csv 


def json_dict_handler(address, json_string):
    '''
    This function is a handler for the server that adds data to the gloabl sample list

    :param address: the endpoint that the message is sent to. (not used)
    :param json_string: the body gesture sent from MaxMSP in string format
    '''
    # Decode the JSON string back into a dictionary
    dictionary = json.loads(json_string)
    print("Received dictionary:", dictionary)
    ds = j2ds(dictionary)
    print(ds)
    samples.append(ds)


def save_csv(address, file_path):
    '''
    This function is a handler that saves all the items in global list 'sample'. The function clears the 
    sample list after a successful save.
    :param address: the endpoint that the message is sent to. (not used)
    :param file_path: the file_path is sent without the extention so .csv will be concatinated to the path_file.
    '''
    df = pd.DataFrame(samples)
    if os.path.exists(file_path + ".csv"):
        df.to_csv(file_path + ".csv", mode='a', header=False, index=False)
    else:
        df.to_csv(file_path+".csv", index=False)
    samples.clear()


if __name__ == "__main__":
    # Define the IP and port to listen on
    ip = "127.0.0.1"  # Localhost (or change to your local IP for external connections)
    port = 8000       # Port must match what is set in Max MSP

    if os.path.exists("tempdata.json"):
        os.remove("tempdata.json")
    # Set up the dispatcher to map the OSC address to the handler
    disp = dispatcher.Dispatcher()
    disp.map("/dictData", json_dict_handler)  # Must match the OSC address set in Max
    disp.map("/save", save_csv)

    # Start the server to listen for incoming OSC messages
    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    print(f"Listening on {ip}:{port}")

    # Keep the server running
    server.serve_forever()
