import socket
import json
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8080
LOG_FILE = "server_logs.txt"

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def handle_request(payload, client_ip):
    a, b, name = payload.get("a"), payload.get("b"), payload.get("name")
    op = payload.get("operation")

    if op == "get_logs":
        if not name:
            return {"error": "Missing name", "code": 400}
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = f.read()
        log(f"**** {name} - {client_ip} → OK: Logs retrieved ****")
        return {"code": 200, "logs": logs}

    if a is None or b is None:
        return {"error": "Operands must be numbers", "code": 422}

    if op not in ["add", "sub", "mul", "div"]:
        return {"error": "Invalid operation", "code": 422}

    try:
        a = float(a)
        b = float(b)
    except (ValueError, TypeError):
        return {"error": "Operands must be numbers", "code": 422}

    if op == "add":
        ans = a + b
    elif op == "sub":
        ans = a - b
    elif op == "mul":
        ans = a * b
    elif op == "div":
        if b == 0:
            return {"error": "Division by zero", "code": 422}
        ans = round(a / b, 3)

    log(f"{client_ip} → OK: {op}({a},{b}) = {ans}")
    return {"result": ans, "code": 200}


# --- Server setup ---
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Calculator server running on {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    client_ip, client_port = addr
    log(f"==> Connected to {client_ip}:{client_port}")

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                log(f"X {client_ip} → Client disconnected")
                break

            try:
                data_str = data.decode().strip()
                if not data_str:
                    payload = {"a": None, "b": None, "operation": None, "name": None}
                else:
                    payload = json.loads(data_str)

                response = handle_request(payload, client_ip)
                conn.send(json.dumps(response).encode())

            except json.JSONDecodeError as e:
                log(f"X {client_ip} → Invalid JSON: {str(e)}")
                conn.send(json.dumps({"error": "Invalid JSON", "code": 400}).encode())
            except Exception as e:
                log(f"X {client_ip} → Internal error: {str(e)}")
                try:
                    conn.send(json.dumps({"error": "Internal server error", "code": 500}).encode())
                except:
                    break

    finally:
        log(f"<== Disconnected from {client_ip}:{client_port}")
        conn.close()
        log("\n----------------------------------------\n")
