import socket
import os
import threading


class HTTPServer:
    HOST = "localhost"
    PORT = 8888
    DOCUMENT_ROOT = "./templates"

    def __init__(self):
        self.host = self.HOST
        self.port = self.PORT
        self.document_root = self.DOCUMENT_ROOT

    def handle_request(self, client_socket):
        try:
            request_data = client_socket.recv(1024).decode("utf-8")
            request_lines = request_data.splitlines()
            if request_lines:
                request_line = request_lines[0]
                method, path, _ = request_line.split()
                if method in ["GET", "HEAD"]:
                    if path == "/":
                        path = "/index.html"
                    file_path = os.path.join(self.document_root, path.lstrip("/"))
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            content = f.read()
                        response = (
                            "HTTP/1.1 200 OK\r\n"
                            f"Content-Length: {len(content)}\r\n"
                            "Content-Type: text/html\r\n"
                            "Connection: close\r\n\r\n"
                        ).encode("utf-8")
                        client_socket.sendall(response)
                        if method == "GET":
                            client_socket.sendall(content)
                    else:
                        response = (
                            "HTTP/1.1 404 Not Found\r\n"
                            "Content-Length: 0\r\n"
                            "Connection: close\r\n\r\n"
                        ).encode("utf-8")
                        client_socket.sendall(response)
        except Exception as e:
            print(f"Error handling request: {e}")
        finally:
            client_socket.close()

    def client_handler(self, client_socket):
        thread = threading.Thread(target=self.handle_request, args=(client_socket,))
        thread.start()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(100)
            print(f"Server started on {self.host}:{self.port}")
            while True:
                client_socket, addr = server_socket.accept()
                print(f"New connection from {addr}")
                self.client_handler(client_socket)
        except Exception as err:
            print(f"Error starting server: {err}")
        finally:
            server_socket.close()


if __name__ == "__main__":
    server = HTTPServer()
    server.start_server()
