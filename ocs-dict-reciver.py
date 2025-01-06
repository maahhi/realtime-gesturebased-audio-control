from pythonosc import dispatcher
from pythonosc import osc_server
import json

# Define the IP and port to listen on
ip = "127.0.0.1"  # Localhost (or change to your local IP for external connections)
port = 8000       # Port must match what is set in Max MSP


# Function to store JSON strings in a file
def save_json_string(json_string, file_path="tempdata.json"):
    # remove all the next lines in the string
    json_string = json_string.replace("\n", "")

    with open(file_path, "a") as file:  # "a" mode to append each JSON string as a new line
        file.write(json_string + "\n")

#if tempdata.json exist, remove it
import os
if os.path.exists("tempdata.json"):
    os.remove("tempdata.json")


# Define a handler function to process incoming OSC messages
samples = []
def json_dict_handler(address, json_string):
    # Decode the JSON string back into a dictionary
    dictionary = json.loads(json_string)
    print("Received dictionary:", dictionary)
    save_json_string(json_string)


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



# Set up the dispatcher to map the OSC address to the handler
disp = dispatcher.Dispatcher()
disp.map("/dictData", json_dict_handler)  # Must match the OSC address set in Max
disp.map("/save", save_handler)  # Must match the OSC address set in Max

# Start the server to listen for incoming OSC messages
server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
print(f"Listening on {ip}:{port}")

# Keep the server running
server.serve_forever()
