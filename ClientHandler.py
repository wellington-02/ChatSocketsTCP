import threading


class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address, server):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.server = server

    def run(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received message from {self.client_address}: {message}")
                self.server.broadcast(message, self.client_socket, self.client_address)
        except Exception as e:
            print(f"Client handler error: {e}")
        finally:
            self.client_socket.close()
            self.server.remove_client(self.client_socket, self.client_address)