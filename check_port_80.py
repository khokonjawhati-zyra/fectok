import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind(("0.0.0.0", 80))
    print("PORT_80_FREE")
    s.close()
except Exception as e:
    print(f"PORT_80_BLOCKED: {e}")
