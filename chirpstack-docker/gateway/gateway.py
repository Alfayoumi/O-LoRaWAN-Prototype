import socket
import json
import time
import struct
import random
import subprocess  # For running system commands

# Gateway MAC address (must be 8 bytes / 16 hex characters)
GATEWAY_MAC = 'AA:BB:CC:DD:EE:FF:00:01'  # Example 8-byte MAC address

# ChirpStack Gateway Bridge IP and port (UDP for Semtech protocol)
BRIDGE_IP = 'chirpstack-gateway-bridge'
BRIDGE_PORT = 1700


# Function to create a UDP socket
def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return sock


# Function to send PUSH_DATA to the ChirpStack Gateway Bridge
def send_push_data(sock):
    token = random.randint(0, 65535)

    status = json.dumps({
        "stat": {
            "time": time.strftime('%Y-%m-%d %H:%M:%S GMT', time.gmtime()),
            "lati": 52.5200,
            "long": 13.4050,
            "alti": 34,
            "rxnb": 10,
            "rxok": 10,
            "rxfw": 10,
            "ackr": 100.0,
            "dwnb": 5,
            "txnb": 5
        }
    })

    packet = struct.pack('!BHB', 2, token, 0) + bytes.fromhex(GATEWAY_MAC.replace(':', '')) + status.encode('utf-8')
    sock.sendto(packet, (BRIDGE_IP, BRIDGE_PORT))
    print(f"Sent PUSH_DATA: {status}")


# Function to send PULL_DATA to request downlink messages
def send_pull_data(sock):
    token = random.randint(0, 65535)
    packet = struct.pack('!BHB', 2, token, 2) + bytes.fromhex(GATEWAY_MAC.replace(':', ''))
    sock.sendto(packet, (BRIDGE_IP, BRIDGE_PORT))
    print("Sent PULL_DATA")


# Function to simulate UL traffic with iperf
def simulate_ul_traffic():
    while True:
        # Generate a random throughput value between 1M and 10M
        throughput = random.randint(1, 10)
        duration = random.randint(1, 2)  # Random duration between 1 and 2 seconds

        # Construct the iperf command
        command = f"sudo ip netns exec ue1 iperf -c 10.45.1.1 -u -b {throughput}M -i 1 -t {duration}"
        print(f"Running command: {command}")

        # Execute the command
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running iperf command: {e}")

        # Wait before next simulation
        time.sleep(5)


# Main function to simulate the gateway behavior
def main():
    sock = create_socket()  # Create a UDP socket

    # Start UL traffic simulation in a separate thread
    import threading
    ul_thread = threading.Thread(target=simulate_ul_traffic)
    ul_thread.daemon = True  # Ensure the thread exits when the main program exits
    ul_thread.start()

    while True:
        send_push_data(sock)
        # send_pull_data(sock)
        time.sleep(10)


if __name__ == "__main__":
    main()
