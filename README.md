# 🌐 Tugas Besar Jaringan Komputer — Web Server TCP Socket

> Implementasi Web Server sederhana menggunakan **TCP Socket** pada Python, dengan dua pendekatan: **Single-Threaded** dan **Multi-Threaded**, beserta **HTTP Client** untuk pengujian.

---

## 📋 Daftar Isi

- [Deskripsi Proyek](#-deskripsi-proyek)
- [Arsitektur Sistem](#-arsitektur-sistem)
- [Struktur Direktori](#-struktur-direktori)
- [Prasyarat](#-prasyarat)
- [Cara Menjalankan](#-cara-menjalankan)
  - [1. Web Server Single-Threaded](#1-web-server-single-threaded)
  - [2. Web Server Multi-Threaded](#2-web-server-multi-threaded)
  - [3. HTTP Client](#3-http-client)
  - [4. Akses via Browser](#4-akses-via-browser)
- [Penjelasan Kode](#-penjelasan-kode)
  - [Web Server Single-Threaded](#web-server-single-threaded-web_server_singlepy)
  - [Web Server Multi-Threaded](#web-server-multi-threaded-web_server_multipy)
  - [HTTP Client](#http-client-clientpy)
- [Perbandingan Single-Threaded vs Multi-Threaded](#-perbandingan-single-threaded-vs-multi-threaded)
- [Diagram Alur](#-diagram-alur)
- [Pengujian](#-pengujian)
- [Anggota Kelompok](#-anggota-kelompok)
- [Lisensi](#-lisensi)

---

## 📖 Deskripsi Proyek

Proyek ini merupakan **Tugas Besar mata kuliah Jaringan Komputer** yang mengimplementasikan web server dari nol menggunakan **raw TCP socket** pada Python — tanpa menggunakan library HTTP bawaan seperti `http.server` atau framework seperti Flask/Django.

### Tujuan Pembelajaran

1. Memahami cara kerja protokol **HTTP** di atas **TCP**
2. Memahami mekanisme **socket programming** (bind, listen, accept, send, recv)
3. Membandingkan model server **single-threaded** vs **multi-threaded**
4. Memahami format **HTTP Request** dan **HTTP Response**

---

## 🏗 Arsitektur Sistem

```
┌─────────────────┐         HTTP Request          ┌─────────────────────┐
│                 │  ──────────────────────────►   │                     │
│   HTTP Client   │    GET /HelloWorld.html        │     Web Server      │
│  (client.py /   │                                │  (Single / Multi)   │
│    Browser)     │  ◄──────────────────────────   │                     │
│                 │       HTTP Response             │  Port 80 (TCP)      │
└─────────────────┘    200 OK + HTML Content        └─────────────────────┘
                                                           │
                                                           ▼
                                                   ┌───────────────┐
                                                   │ HelloWorld.html│
                                                   │  (Static File) │
                                                   └───────────────┘
```

---

## 📁 Struktur Direktori

```
tubes_jarkom/
├── web_server_single.py   # Web server single-threaded
├── web_server_multi.py    # Web server multi-threaded
├── client.py              # HTTP client untuk pengujian
├── latihan.py             # File latihan/eksperimen multi-threaded
├── HelloWorld.html        # Halaman HTML statis untuk disajikan
└── README.md              # Dokumentasi proyek (file ini)
```

| File | Deskripsi |
|------|-----------|
| `web_server_single.py` | Server yang menangani **satu klien pada satu waktu** secara berurutan (sekuensial) |
| `web_server_multi.py` | Server yang menangani **banyak klien secara bersamaan** menggunakan threading |
| `client.py` | Klien HTTP yang mengirim request GET dan menampilkan response mentah |
| `latihan.py` | Versi latihan dari multi-threaded server |
| `HelloWorld.html` | Halaman HTML statis yang disajikan oleh server |

---

## ⚙ Prasyarat

- **Python 3.6+** (disarankan Python 3.10+)
- Sistem operasi: Windows / Linux / macOS
- **Tidak memerlukan instalasi library tambahan** — hanya menggunakan modul bawaan Python (`socket`, `threading`, `time`, `sys`)

> ⚠️ **Catatan**: Menjalankan server pada port **80** memerlukan hak akses **Administrator** (Windows) atau **root** (Linux/macOS). Jika tidak ingin menggunakan hak akses khusus, ubah port ke angka di atas 1024 (misalnya `8080`).

---

## 🚀 Cara Menjalankan

### 1. Web Server Single-Threaded

```bash
# Windows (jalankan CMD/PowerShell sebagai Administrator)
python web_server_single.py

# Linux/macOS
sudo python3 web_server_single.py
```

**Output yang diharapkan:**
```
Server siap melayani pada port 80...
```

### 2. Web Server Multi-Threaded

```bash
# Windows (jalankan CMD/PowerShell sebagai Administrator)
python web_server_multi.py

# Linux/macOS
sudo python3 web_server_multi.py
```

**Output yang diharapkan:**
```
Server siap melayani pada port 80...
```

### 3. HTTP Client

Buka terminal **baru** (jangan menutup terminal server), lalu jalankan:

```bash
python client.py localhost 80 HelloWorld.html
```

**Format penggunaan:**
```
python client.py <SERVER_HOST> <SERVER_PORT> <FILENAME>
```

| Parameter | Deskripsi | Contoh |
|-----------|-----------|--------|
| `SERVER_HOST` | Alamat IP atau hostname server | `localhost`, `127.0.0.1`, `192.168.1.10` |
| `SERVER_PORT` | Port yang digunakan server | `80` |
| `FILENAME` | Nama file yang diminta | `HelloWorld.html` |

**Contoh output (berhasil):**
```
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
...
</html>
```

**Contoh output (file tidak ditemukan):**
```
HTTP/1.1 404 Not Found
Content-Type: text/html

<html><h1>404 Not Found</h1></html>
```

### 4. Akses via Browser

Setelah server berjalan, buka browser dan akses:

```
http://localhost/HelloWorld.html
```

atau jika menggunakan port selain 80:

```
http://localhost:8080/HelloWorld.html
```

---

## 📝 Penjelasan Kode

### Web Server Single-Threaded (`web_server_single.py`)

Server ini menangani koneksi klien **satu per satu secara berurutan**. Ketika satu klien sedang dilayani, klien lain harus menunggu hingga koneksi sebelumnya selesai.

**Alur Kerja:**

1. **Inisialisasi Socket** — Membuat TCP socket dan bind ke port 80
2. **Listen** — Menunggu koneksi masuk (queue = 1)
3. **Accept** — Menerima koneksi dari klien
4. **Parsing Request** — Menguraikan HTTP GET request untuk mendapatkan nama file
5. **Baca File** — Membuka dan membaca file yang diminta
6. **Kirim Response** — Mengirimkan HTTP header + konten file ke klien
7. **Tutup Koneksi** — Menutup socket setelah delay 5 detik
8. **Ulangi** — Kembali ke langkah 3 untuk menerima klien berikutnya

```python
# Kunci: handle_client() dipanggil secara SEKUENSIAL di main loop
handle_client(connectionSocket)  # Blocking — klien berikutnya harus menunggu
```

### Web Server Multi-Threaded (`web_server_multi.py`)

Server ini menangani **banyak koneksi klien secara bersamaan** menggunakan modul `threading`. Setiap koneksi baru ditangani oleh thread terpisah.

**Alur Kerja:**

1–4. Sama seperti single-threaded
5. **Buat Thread Baru** — Membuat thread terpisah untuk menangani klien
6. **Start Thread** — Thread baru berjalan secara paralel
7. **Main Loop Kembali Menunggu** — Main thread langsung kembali menerima koneksi baru

```python
# Kunci: Setiap klien ditangani oleh thread TERPISAH
client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
client_thread.start()  # Non-blocking — main loop langsung lanjut
```

### HTTP Client (`client.py`)

Client mengirimkan **HTTP GET request** ke server dan menampilkan response mentah (raw).

**Format Request yang Dikirim:**
```http
GET /HelloWorld.html HTTP/1.1
Host: localhost
Connection: close

```

---

## ⚖ Perbandingan Single-Threaded vs Multi-Threaded

| Aspek | Single-Threaded | Multi-Threaded |
|-------|:-:|:-:|
| **Koneksi bersamaan** | ❌ Satu | ✅ Banyak |
| **Antrian (backlog)** | 1 | 5 |
| **Blocking** | Ya — klien menunggu giliran | Tidak — setiap klien punya thread |
| **Kompleksitas kode** | Sederhana | Sedikit lebih kompleks |
| **Penggunaan resource** | Rendah | Lebih tinggi (1 thread / koneksi) |
| **Cocok untuk** | Pembelajaran, testing | Produksi ringan, multi-client |
| **Risiko** | Lambat jika banyak klien | Potensi race condition |

### Ilustrasi Perbedaan

**Single-Threaded (Sekuensial):**
```
Klien A ────[dilayani 5 detik]────► selesai
                                         Klien B ────[dilayani 5 detik]────► selesai
                                                                                  Klien C ────► ...
```

**Multi-Threaded (Paralel):**
```
Klien A ────[dilayani 5 detik]────► selesai
Klien B ────[dilayani 5 detik]────► selesai
Klien C ────[dilayani 5 detik]────► selesai
     ↑ Semua berjalan bersamaan
```

---

## 📊 Diagram Alur

### Alur Komunikasi Client-Server

```
Client                                          Server
  │                                                │
  │  ──── TCP SYN ──────────────────────────────►  │
  │  ◄─── TCP SYN-ACK ─────────────────────────── │  (3-Way Handshake)
  │  ──── TCP ACK ──────────────────────────────►  │
  │                                                │
  │  ──── GET /HelloWorld.html HTTP/1.1 ────────►  │  (HTTP Request)
  │                                                │
  │                                          [Baca file dari disk]
  │                                                │
  │  ◄─── HTTP/1.1 200 OK ─────────────────────── │  (HTTP Response Header)
  │  ◄─── <html>...</html> ────────────────────── │  (HTTP Response Body)
  │                                                │
  │  ◄─── TCP FIN ─────────────────────────────── │  (Tutup koneksi)
  │  ──── TCP ACK ──────────────────────────────►  │
  │                                                │
```

---

## 🧪 Pengujian

### Skenario 1: Request File yang Ada

```bash
python client.py localhost 80 HelloWorld.html
```
✅ **Expected**: Response `200 OK` dengan konten HTML

### Skenario 2: Request File yang Tidak Ada

```bash
python client.py localhost 80 tidakada.html
```
✅ **Expected**: Response `404 Not Found`

### Skenario 3: Banyak Klien Bersamaan (Multi-Threaded)

Buka 3 terminal terpisah dan jalankan secara bersamaan:
```bash
# Terminal 1
python client.py localhost 80 HelloWorld.html

# Terminal 2
python client.py localhost 80 HelloWorld.html

# Terminal 3
python client.py localhost 80 HelloWorld.html
```

✅ **Expected pada multi-threaded**: Ketiga klien dilayani secara paralel (selesai hampir bersamaan)  
⚠️ **Expected pada single-threaded**: Klien dilayani satu per satu (selesai secara berurutan, ~5 detik antar klien)

---

## 👥 Anggota Kelompok

| Nama |
|------|
| Abdullah |
| Roji |
| Ibnu |

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademis — Tugas Besar mata kuliah **Jaringan Komputer**.

© 2025 Abdullah, Roji, Ibnu
