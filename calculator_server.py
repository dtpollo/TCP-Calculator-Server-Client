import socket      # TCP socket communication
import json        # JSON parsing and serialization
from datetime import datetime  # Timestamping for logs

HOST = "0.0.0.0"   # Bind to all interfaces
PORT = <server_port>        # Listening port
LOG_FILE = "server_logs.txt"  # Log file path

def log(message):
    """Append timestamped log entry to file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def handle_request(data, client_ip):
    """
    Process client JSON request and return response.
    Expected format: {"a": num, "b": num, "operation": str, "name": str (optional)}
    Supported operations: add, sub, mul, div, get_logs
    """
    try:
        payload = json.loads(data)
        a, b, name = payload.get("a"), payload.get("b"), payload.get("name")
        op = payload.get("operation")

        if op is None:
            log(f"X {client_ip} → ERROR: Missing operation {payload}")
            return {"error": "Missing operation", "code": 400}

        if op == "get_logs":
            if name is None:
                log(f"X {client_ip} → ERROR: Missing name {payload}")
                return {"error": "Missing name", "code": 400}
            with open(LOG_FILE, "r") as f:
                logs = f.read()
            log(f"**** {name} - {client_ip} → OK: Logs retrieved ****")
            return {"code": 200, "logs": logs}

        if a is None or b is None:
            log(f"X {client_ip} → ERROR: Missing parameters {payload}")
            return {"error": "Missing parameters", "code": 400}

        if op not in ["add", "sub", "mul", "div"]:
            log(f"X {client_ip} → ERROR: Invalid operation {payload}")
            return {"error": "Invalid operation", "code": 422}

        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            log(f"X {client_ip} → ERROR: Invalid types {payload}")
            return {"error": "Invalid input", "code": 422}

        if op == "add":
            ans = a + b
        elif op == "sub":
            ans = a - b
        elif op == "mul":
            ans = a * b
        elif op == "div":
            if b == 0:
                log(f"X {client_ip} → ERROR: Division by zero {payload}")
                return {"error": "Division by zero", "code": 422}
            ans = round(a / b, 3)

        log(f"{client_ip} → OK: {op}({a},{b}) = {ans}")
        return {"result": ans, "code": 200}

    except json.JSONDecodeError:
        log(f"X {client_ip} → ERROR: Invalid JSON {data}")
        return {"error": "Invalid JSON", "code": 400}

# Server setup
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Calculator server running on {HOST}:{PORT}")

# Connection loop
while True:
    try:
        conn, addr = server_socket.accept()
        client_ip, client_port = addr
        log(f"==> Connected to {client_ip}:{client_port}")

        data = conn.recv(1024).decode()
        if not data:
            log(f"X {client_ip} → ERROR: No data received")
            conn.close()
            continue

        response = handle_request(data, client_ip)
        conn.send(json.dumps(response).encode())
        log(f"<== Disconnected from {client_ip}:{client_port}")
        log("\n ----------------------------------------\n")
        conn.close()

    except Exception as e:
        log(f"X ERROR: Connection handling failed {str(e)}")

