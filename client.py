import socket # Mengimpor modul socket untuk koneksi jaringan
import sys    # Mengimpor modul sys untuk akses argumen baris perintah

def main():
    # Memeriksa jumlah argumen baris perintah yang diberikan
    if len(sys.argv) != 4:
        print('Usage: python client.py <SERVER_HOST> <SERVER_PORT> <FILENAME>')
        sys.exit(1) # Keluar jika penggunaan tidak benar

    # Mengambil host, port, dan nama file dari argumen baris perintah
    host, port, filename = sys.argv[1], int(sys.argv[2]), sys.argv[3]

    # Membuat baris permintaan HTTP GET
    request_line = f"GET /{filename} HTTP/1.1\r\n"
    # Membuat header HTTP, termasuk Host dan Connection: close
    headers = f"Host: {host}\r\nConnection: close\r\n\r\n"
    # Menggabungkan baris permintaan dan header menjadi permintaan HTTP lengkap
    request = request_line + headers

    # Membuat objek socket menggunakan protokol IPv4 (AF_INET) dan TCP (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port)) # Menghubungkan klien ke server (host, port)
        s.sendall(request.encode()) # Mengirim seluruh permintaan HTTP ke server (dalam bentuk bytes)

        response = b"" # Inisialisasi variabel untuk menyimpan respons dari server
        while True:
            data = s.recv(4096) # Menerima data dari server, maksimal 4096 bytes sekaligus
            if not data: # Jika tidak ada data lagi yang diterima (koneksi ditutup atau habis)
                break    # Keluar dari loop
            response += data # Menambahkan data yang diterima ke variabel response

    # Mencetak respons HTTP mentah (header + body) setelah didekode dari bytes menjadi string
    print(response.decode())

if __name__ == '__main__':
    main() # Memanggil fungsi main saat skrip dijalankan