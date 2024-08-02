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
        self.is_running = True

    def start(self):
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(5)
        print(f"Server started on {self.server_ip}:{self.server_port}")
        threading.Thread(target=self.send_messages).start()
        try:
            while self.is_running:
                client_socket, client_address = self.server_socket.accept()
                self.clients[client_address] = client_socket
                handler = ClientHandler(client_socket, client_address, self)
                handler.start()
                print(f"Connection established with {client_address}")
                self.list_clients()
        except Exception as e:
            if self.is_running:
                print(f"Server error: {e}")
        finally:
            self.shutdown_server()

    def send_messages(self):
        while True:
            send = input("Do you want to send a message to a client? (y/n): \n").strip().lower()
            if send == 'y':
                if not self.clients:
                    print("No clients connected. Waiting for clients...")
                    continue
                self.list_clients()
                while True:
                    try:
                        client_idx = int(input("Select client index to send message: \n").strip())
                        client_address = list(self.clients.keys())[client_idx]
                        message = input("Enter message to send: ").strip()
                        self.send_to_client(message, client_address)
                        break
                    except (ValueError, IndexError):
                        print("Invalid client index. Please try again.")
            elif send == 'exit':
                self.is_running = False
                self.server_socket.close()
                break
            else:
                print("Invalid input. Please enter 'y' to send a message or 'exit' to close the server.")

    def send_to_client(self, message, client_address):
        client_socket = self.clients.get(client_address)
        if client_socket:
            try:
                client_socket.sendall(f"server: {message}".encode('utf-8'))
                print(f"Message sent to successfully")
            except Exception as e:
                print(f"Error sending message to {client_address}: {e}")

    def remove_client(self, client_socket, client_address):
        if client_address in self.clients and self.clients[client_address] == client_socket:
            del self.clients[client_address]
            print(f"Connection closed with {client_address}")
            self.list_clients()

    def list_clients(self):
        if self.clients:
            print("Connected clients:")
            for idx, client_address in enumerate(self.clients.keys()):
                print(f"{idx}: {client_address}")
        else:
            print("No clients connected.")

    def shutdown_server(self):
        print("Shutting down server.")
        for client_socket in self.clients.values():
            try:
                client_socket.close()
            except Exception as e:
                print(f"Error closing client socket: {e}")
        self.server_socket.close()

if __name__ == "__main__":
    server = MultiTCPServer('127.0.0.1', 6666)
    server.start()
