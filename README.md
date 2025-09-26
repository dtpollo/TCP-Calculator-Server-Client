# 🧮 Calculator TCP Server & Client

## 🌐 Overview
Simple TCP-based calculator server and client in Python.  
Supports basic arithmetic operations, logging, and remote log retrieval for instructors.

## ⚡ Features
- 🖥️ TCP server listens on configurable IP and port  
- ➕➖✖️➗ Operations: `add`, `sub`, `mul`, `div`  
- 🚫 Handles division by zero and invalid inputs  
- 📝 Logs all client requests with timestamps and IPs  
- 👨‍🏫 Instructor can request logs using a special client script  
- 🔄 Client can perform multiple operations per session

## 📂 Files
- `calculator_server.py` – TCP server  
- `calculator_client.py` – Arithmetic client  
- `logs.py` – Special client to retrieve server logs

## 🛠️ Usage

### Server
```bash
python3 calculator_server.py
