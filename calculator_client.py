# calculator_client.py

import socket       # Network communication
import json         # JSON serialization/deserialization

HOST = "<server_ip>"   # Server IP
PORT = <server_port> # Server port

# User input
a_input = input("Enter first number: ")
b_input = input("Enter second number: ")
op_input = input("Enter operation (add, sub, mul, div): ")
name = None

# Convert input to float or None
try:
    a = float(a_input) if a_input.strip() else None
    b = float(b_input) if b_input.strip() else None
    op = op_input.strip() if op_input.strip() else None
except ValueError:
    a = None
    b = None

# Prepare payload
payload = {"a": a, "b": b, "operation": op, "name": name}
payload_json = json.dumps(payload)  # Convert to JSON string

# Connect and send request
client_socket = socket.socket()    
try:
    client_socket.connect((HOST, PORT))
    client_socket.send(payload_json.encode())

    # Receive and parse response
    response_data = client_socket.recv(1024)
    response = json.loads(response_data.decode())

    # Display result or error
    if response.get("code") == 200:
        print(f"Result from server: {response['result']}")
    else:
        print(f"Error from server: {response.get('error')} (code {response.get('code')})")

except ConnectionRefusedError:
    print("Could not connect to the server. Is it running?")
