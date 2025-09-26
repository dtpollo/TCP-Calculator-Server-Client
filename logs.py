import socket      # TCP socket communication
import json        # JSON serialization

HOST = "<server_ip>"  # Server IP address
PORT = <server_port>  # Server port

# Prepare log request payload
a = None
b = None
name = input("Enter your name: ").strip()
payload = {"a": a, "b": b, "operation": "get_logs", "name": name}
payload_json = json.dumps(payload)

# Connect to server and send request
client_socket = socket.socket()
try:
    client_socket.connect((HOST, PORT))
    client_socket.send(payload_json.encode())

    # 🔹 Receive all data fragments until server closes connection
    data = b""
    while True:
        part = client_socket.recv(4096)
        if not part:
            break
        data += part

    # Parse JSON response
    response = json.loads(data.decode())
    print("DEBUG parsed JSON:", response)

    # Save logs if response is successful
    if response.get("code") == 200:
        logs = response.get("logs")

        # Convert list to string if necessary
        if isinstance(logs, list):
            logs = "\n".join(logs)

        with open("logs_Troya.txt", "w", encoding="utf-8") as f:
            f.write(logs)

        print("Logs have been saved to logs_Troya.txt")
    else:
        print(f"Error: {response.get('error')} (code {response.get('code')})")

except ConnectionRefusedError:
    print("Could not connect to the server. Is it running?")
except json.JSONDecodeError as e:
    print("JSON decode error:", e)
finally:
    client_socket.close()
