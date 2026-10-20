from socket import * # Mengimpor semua fungsi dari modul socket untuk jaringan
import time          # Mengimpor modul time untuk fungsi penundaan (delay)

def handle_client(connectionSocket):
    try:
        # Membaca data dari buffer socket klien (maks 1024 bytes) dan mendekodenya dari bytes ke string
        message = connectionSocket.recv(1024).decode()
        # Menguraikan pesan HTTP GET untuk mendapatkan nama file yang diminta
        # Contoh: "GET /HelloWorld.html HTTP/1.1" -> "HelloWorld.html"
        filename = message.split()[1][1:]

        try:
            # Membuka dan membaca konten file yang diminta dalam mode baca ('r')
            with open(filename, 'r') as f:
                content = f.read()

            # Membuat header respons HTTP 200 OK (berhasil)
            header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
            connectionSocket.send(header.encode()) # Mengirim header ke klien (dalam bentuk bytes)

            # Mengirim konten file ke klien, karakter per karakter
            for i in range(0, len(content)):
                connectionSocket.send(content[i].encode())
            connectionSocket.send("\r\n".encode()) # Mengirim baris kosong tambahan sebagai penutup body HTTP
        except FileNotFoundError: # Menangkap kesalahan jika file tidak ditemukan
            # Membuat header respons HTTP 404 Not Found
            header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n'
            connectionSocket.send(header.encode()) # Mengirim header 404 ke klien
            # Mengirim pesan HTML 404 Not Found sebagai body respons
            connectionSocket.send("<html><h1>404 Not Found</h1></html>\r\n".encode())

    finally:
        time.sleep(5) # Memberi penundaan 5 detik sebelum menutup koneksi
        connectionSocket.close() # Menutup socket koneksi dengan klien
        print("Koneksi ditutup.") # Mencetak pesan bahwa koneksi telah ditutup

def main():
    SERVER_PORT = 80 # Mendefinisikan nomor port server (port HTTP standar)
    serverSocket = socket(AF_INET, SOCK_STREAM) # Membuat objek socket: AF_INET (IPv4), SOCK_STREAM (TCP)
    # Mengikat socket ke alamat IP lokal apa pun ('') dan port yang ditentukan
    serverSocket.bind(('', SERVER_PORT))
    serverSocket.listen(1) # Memulai mendengarkan koneksi masuk, dengan antrean maksimum 1 koneksi

    print(f"Server siap melayani pada port {SERVER_PORT}...") # Mencetak pesan status server

    while True: # Loop tak terbatas untuk terus menerima koneksi klien
        # Menerima koneksi baru dari klien; mengembalikan socket koneksi dan alamat klien (IP, port)
        connectionSocket, addr = serverSocket.accept()
        # Mencetak pesan bahwa koneksi terdeteksi, hanya menampilkan port sumber klien
        print(f"Koneksi masuk terdeteksi. (Port Client: {addr[1]})")
        handle_client(connectionSocket) # Memanggil fungsi untuk menangani koneksi klien yang baru

if __name__ == '__main__':
    main() # Memanggil fungsi main saat skrip dijalankan