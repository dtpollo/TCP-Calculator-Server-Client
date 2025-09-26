import socket
import json

HOST = "3.144.148.247"
PORT = 8080

print("Enter operation parameters. Press Ctrl+C to exit.\n")

while True:
    try:
        # Entrada interactiva por campo
        a_input = input("Enter value for a: ").strip()
        b_input = input("Enter value for b: ").strip()
        op = input("Enter operation (add, sub, mul, div, get_logs): ").strip()
        name = input("Enter your name (optional, required for get_logs): ").strip()

        # Convertir a None si está vacío
        a = float(a_input) if a_input else None
        b = float(b_input) if b_input else None
        payload = {
            "a": a,
            "b": b,
            "operation": op if op else None,
            "name": name if name else None
        }

        # Enviar al servidor
        client_socket = socket.socket()
        client_socket.connect((HOST, PORT))
        client_socket.send(json.dumps(payload).encode())

        # Recibir respuesta completa
        data = b""
        while True:
            part = client_socket.recv(4096)
            if not part:
                break
            data += part

        response = json.loads(data.decode())
        print("🧾 Response:", response)

        # Guardar logs si se recibió correctamente
        if response.get("code") == 200 and "logs" in response:
            logs = response["logs"]
            if isinstance(logs, list):
                logs = "\n".join(logs)
            with open("logs_Troya.txt", "w", encoding="utf-8") as f:
                f.write(logs)
            print("Logs saved to logs_Troya.txt")

        client_socket.close()

    except ValueError:
        print("Invalid number format in a or b.")
    except json.JSONDecodeError:
        print("JSON decode error.")
    except ConnectionRefusedError:
        print("Could not connect to the server.")
        break
    except KeyboardInterrupt:
        print("\nSession terminated by user.")
        break
    except Exception as e:
        print("Unexpected error:", e)
