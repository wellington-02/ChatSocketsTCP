import socket
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

class MultiTCPServer:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.clients = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(5)
        print(f"Server started on {self.server_ip}:{self.server_port}")
        threading.Thread(target=self.send_messages).start()
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                self.clients[client_address] = client_socket
                handler = ClientHandler(client_socket, client_address, self)
                handler.start()
                print(f"Connection established with {client_address}")
                self.list_clients()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.server_socket.close()

    def send_messages(self):
        while True:
            self.list_clients()
            client_idx = input("Select client index to send message: ")
            try:
                client_idx = int(client_idx)
                client_address = list(self.clients.keys())[client_idx]
                message = input("Enter message to send: ")
                self.send_to_client(message, client_address)
            except (ValueError, IndexError):
                print("Invalid client index")

    def send_to_client(self, message, client_address):
        client_socket = self.clients.get(client_address)
        if client_socket:
            try:
                client_socket.sendall(f"server: {message}".encode('utf-8'))
                print(f"Message sent to {client_address}")
            except Exception as e:
                print(f"Error sending message to {client_address}: {e}")

    def broadcast(self, message, source_socket=None, source_address=None):
        for client_address, client_socket in self.clients.items():
            if client_socket != source_socket:
                try:
                    # Include the source address (IP, port) in the message
                    full_message = f"{source_address[0]}:{source_address[1]} - {message}" if source_address else message
                    client_socket.sendall(full_message.encode('utf-8'))
                except Exception as e:
                    print(f"Broadcast error: {e}")

    def remove_client(self, client_socket, client_address):
        if client_address in self.clients and self.clients[client_address] == client_socket:
            del self.clients[client_address]
            print(f"Connection closed with {client_address}")
            self.list_clients()

    def list_clients(self):
        print("Connected clients:")
        for idx, client_address in enumerate(self.clients.keys()):
            print(f"{idx}: {client_address}")

if __name__ == "__main__":
    server = MultiTCPServer('127.0.0.1', 6666)
    server.start()
