from socket import *
import time
import threading

def handle_client(connectionSocket, addr):
    try:
        message = connectionSocket.recv(1024).decode()
        
        filename = message.split()[1][1:]
        
        try:
            with open(filename, 'r') as f:
                outputdata = f.read()
                
            header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
            connectionSocket.send(header.encode())
                
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
        except IOError:
            header = 'HTTP/1.1 404 Not Found\r\n\r\n'
            connectionSocket.send(header.encode())
            connectionSocket.send("<html><h1>404 Not Found</h1></html>\r\n".encode())
            
    finally:
        time.sleep(5)
        connectionSocket.close()
        print("Koneksi ditutup.")
            
def main():
    serverPort = 80
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)
    print(f"Server berjalan di port {serverPort}...")
    
    while True:
        connectionSocket, addr = serverSocket.accept()
        print(f"Koneksi masuk terdeteksi. (Port Client = {addr[1]})")
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        client_thread.start()
        
if __name__ == '__main__':
    main()