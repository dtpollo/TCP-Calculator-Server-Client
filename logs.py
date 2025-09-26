import socket      # TCP client socket
import json        # JSON serialization

HOST = "3.144.148.247"   # Server IP
PORT = 8080 # Server port

# Optional identifier for logging
a = None
b = None
name = input("Enter your name: ").strip()

# Construct log request payload
payload = {"a": a, "b": b, "operation": "get_logs", "name": name}
payload_json = json.dumps(payload)

# Establish connection and send request
client_socket = socket.socket()
try:
    client_socket.connect((HOST, PORT))
    client_socket.send(payload_json.encode())

    # Receive response (up to 64 KB)
    response_data = client_socket.recv(65536)
    response = json.loads(response_data.decode())

    # Save logs if response is successful
    if response.get("code") == 200:
        logs = response.get("logs")
        with open("logs_Troya.txt", "w") as f:
            f.write(logs)
        print("Logs have been saved to logs_Troya.txt")
    else:
        print(f"Error: {response.get('error')} (code {response.get('code')})")

except ConnectionRefusedError:
    print("Could not connect to the server. Is it running?")
finally:
    client_socket.close()
