import socket
import threading

class ReceiveMessages(threading.Thread):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket

    def run(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                if "server:" in message:
                    print(f"Received message from {message}")
        except Exception as e:
            print(f"Client handler error: {e}")
        finally:
            self.client_socket.close()

class SimpleTCPClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print(f"Connected to server {self.server_ip}:{self.server_port}")

            # Get client IP and port
            self.client_ip, self.client_port = self.client_socket.getsockname()

            receive_thread = ReceiveMessages(self.client_socket)
            receive_thread.start()

            while True:
                message = input()
                if message.lower() == 'exit':
                    break
                self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Communication error: {e}")
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    client = SimpleTCPClient('127.0.0.1', 6666)
    client.start()
