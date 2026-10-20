from socket import * # Mengimpor semua fungsi dari modul socket untuk jaringan
import threading     # Mengimpor modul threading untuk mendukung konkurensi (multitasking)
import time          # Mengimpor modul time untuk fungsi penundaan (delay)

# Fungsi untuk menangani setiap koneksi klien secara terpisah
def handle_client(connectionSocket, addr):
    try:
        # Membaca data dari buffer socket klien (maks 1024 bytes) dan mendekodenya dari bytes ke string
        message = connectionSocket.recv(1024).decode()
        # Menguraikan pesan HTTP GET untuk mendapatkan nama file yang diminta
        # Contoh: "GET /HelloWorld.html HTTP/1.1" -> "HelloWorld.html"
        filename = message.split()[1][1:]

        try:
            # Membuka dan membaca konten file yang diminta dalam mode baca ('r')
            with open(filename, 'r') as f:
                outputdata = f.read()

            # Membuat header respons HTTP 200 OK (berhasil)
            header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
            connectionSocket.send(header.encode()) # Mengirim header ke klien (dalam bentuk bytes)

            # Mengirim konten file ke klien, karakter per karakter
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode()) # Mengirim baris kosong tambahan sebagai penutup body HTTP
        except IOError: # Menangkap kesalahan jika file tidak ditemukan atau masalah I/O lainnya
            # Membuat header respons HTTP 404 Not Found
            header = 'HTTP/1.1 404 Not Found\r\n\r\n'
            connectionSocket.send(header.encode()) # Mengirim header 404 ke klien
            # Mengirim pesan HTML 404 Not Found sebagai body respons
            connectionSocket.send("<html><h1>404 Not Found</h1></html>\r\n".encode())

    finally:
        time.sleep(5) # Memberi penundaan 5 detik sebelum menutup koneksi (untuk tujuan demonstrasi)
        connectionSocket.close() # Menutup socket koneksi dengan klien
        print("Koneksi ditutup.") # Mencetak pesan bahwa koneksi telah ditutup

def main():
    serverPort = 80 # Mendefinisikan nomor port server (port HTTP standar)
    serverSocket = socket(AF_INET, SOCK_STREAM) # Membuat objek socket: AF_INET (IPv4), SOCK_STREAM (TCP)
    # Mengikat socket ke alamat IP lokal apa pun ('') dan port yang ditentukan
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)  # Memulai mendengarkan koneksi masuk, dengan antrean maksimum 5 koneksi
    print(f'Server siap melayani pada port {serverPort}...') # Mencetak pesan status server

    while True: # Loop tak terbatas untuk terus menerima koneksi klien
        # Menerima koneksi baru dari klien; mengembalikan socket koneksi dan alamat klien (IP, port)
        connectionSocket, addr = serverSocket.accept()
        # Mencetak pesan bahwa koneksi terdeteksi, hanya menampilkan port sumber klien
        print(f"Koneksi masuk terdeteksi. (Port Client: {addr[1]})")
        # Membuat thread baru untuk menangani permintaan klien ini secara bersamaan
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        client_thread.start()  # Memulai eksekusi thread baru

if __name__ == '__main__':
    main() # Memanggil fungsi main saat skrip dijalankan