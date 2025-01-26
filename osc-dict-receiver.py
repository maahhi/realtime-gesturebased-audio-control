from pythonosc import dispatcher
from pythonosc import osc_server
import json
import os
from util.json2dataseries import j2ds
import pandas as pd


# Function to store JSON strings in a file
def save_json_string(json_string, file_path="tempdata.json"):
    # remove all the next lines in the string
    json_string = json_string.replace("\n", "")
    with open(file_path, "a") as file:  # "a" mode to append each JSON string as a new line
        file.write(json_string + "\n")


# Define a handler function to process incoming OSC messages
samples = []
def json_dict_handler(address, json_string):
    # Decode the JSON string back into a dictionary
    dictionary = json.loads(json_string)
    print("Received dictionary:", dictionary)
    ds = j2ds(dictionary)
    print(ds)
    #save_json_string(json_string)
    samples.append(ds)



def save_handler(address, filepath):
    # if the filepath exist, append the temp file to filepath
    if os.path.exists(filepath+".json"):
        with open("tempdata.json", "r") as temp_file:
            with open(filepath+".json", "a") as file:
                for line in temp_file:
                    file.write(line)
        os.remove("tempdata.json")
    else:
        os.rename("tempdata.json", filepath+".json")

def save_csv(address, filepath):
    df = pd.DataFrame(samples)
    if os.path.exists(filepath + ".csv"):
        df.to_csv(filepath + ".csv", mode='a', header=False, index=False)
    else:
        df.to_csv(filepath+".csv", index=False)
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
    #disp.map("/save", save_handler)  # Must match the OSC address set in Max
    disp.map("/save", save_csv)

    # Start the server to listen for incoming OSC messages
    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    print(f"Listening on {ip}:{port}")

    # Keep the server running
    server.serve_forever()
