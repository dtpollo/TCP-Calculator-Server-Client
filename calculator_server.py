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

def handle_request(data, client_ip):
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
            with open(LOG_FILE, "r", encoding="utf-8") as f:
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
# Connection loop
while True:
    conn, addr = server_socket.accept()
    client_ip, client_port = addr
    log(f"==> Connected to {client_ip}:{client_port}")

    try:
        # Bucle por cliente: múltiples operaciones
        while True:
            try:
                data = conn.recv(4096).decode()
                if not data:
                    log(f"X {client_ip} → Client disconnected")
                    break

                response = handle_request(data, client_ip)
                conn.send(json.dumps(response).encode())

            except json.JSONDecodeError as e:
                # JSON inválido: enviar error pero no cerrar la conexión
                log(f"X {client_ip} → Invalid JSON: {str(e)}")
                error_response = {"error": "Invalid JSON", "code": 400}
                conn.send(json.dumps(error_response).encode())
            except Exception as e:
                # Otros errores: registrar y enviar mensaje al cliente
                log(f"X {client_ip} → Internal error: {str(e)}")
                error_response = {"error": "Internal server error", "code": 500}
                try:
                    conn.send(json.dumps(error_response).encode())
                except:
                    break  # si no se puede enviar, salimos del bucle

    except Exception as e:
        log(f"X ERROR: Connection handling failed {str(e)}")
    finally:
        log(f"<== Disconnected from {client_ip}:{client_port}")
        log("\n ----------------------------------------\n")
        conn.close()
