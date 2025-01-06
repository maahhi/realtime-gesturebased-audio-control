from pythonosc.udp_client import SimpleUDPClient
import time

# OSC server settings
max_msp_ip = "127.0.0.1"  # Replace with the IP address of the machine running Max MSP
max_msp_port = 7400       # Replace with the port that Max MSP is listening on

# Initialize the OSC client
osc_client = SimpleUDPClient(max_msp_ip, max_msp_port)

def send_signal(address, value):
    """
    Sends a signal to Max MSP using OSC.
    :param address: The OSC address (e.g., "/signal").
    :param value: The value to send.
    """
    osc_client.send_message(address, value)
    print(f"Sent message to {address} with value {value}")

if __name__ == "__main__":
    try:
        print("Starting OSC client. Press Ctrl+C to stop.")
        while True:
            # Example: Sending a signal every second
            send_signal("/signal", 1.0)  # Replace "/signal" with your desired OSC address
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer stopped.")
