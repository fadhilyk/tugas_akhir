# Software Design Document (SDD)

# Sistem Manajemen Perpustakaan Digital

Language:
Python 3.12+

Paradigm:
Object Oriented Programming

---

# 1. Project Structure

library_system/

    main.py

    models/
        pengguna.py
        anggota.py
        petugas.py
        buku.py
        peminjaman.py
        denda.py

    services/
        library_service.py
        auth_service.py
        report_service.py

    storage/
        database.py

    utils/
        validator.py
        helper.py

    data/
        buku.json
        anggota.json
        transaksi.json

---

# 2. Architecture

Presentation Layer

↓

Service Layer

↓

Repository/Data Layer

↓

JSON Storage

---

# 3. Class Design

## Abstract Class

Pengguna

Properties

- id
- nama
- kontak

Methods

- tampilkan_info()

---

## Class Anggota

Inheritance:

Pengguna

Properties

- daftar_pinjaman

Methods

- pinjam()
- kembali()

---

## Class Petugas

Inheritance:

Pengguna

Methods

- tambah_buku()
- edit_buku()
- hapus_buku()
- proses_peminjaman()
- proses_pengembalian()

---

## Class Buku

Properties

- id
- judul
- penulis
- penerbit
- tahun
- kategori
- stok

Methods

- tersedia()
- kurangi_stok()
- tambah_stok()

---

## Class Peminjaman

Properties

- id
- anggota
- buku
- tanggal_pinjam
- jatuh_tempo
- tanggal_kembali
- status

Methods

- hitung_denda()
- selesai()

---

## Class Denda

Properties

- nominal
- status_pembayaran

Methods

- hitung()

---

## Class Perpustakaan

Properties

- daftar_buku
- daftar_anggota
- daftar_transaksi

Methods

- tambah_buku()
- edit_buku()
- hapus_buku()
- tambah_anggota()
- edit_anggota()
- hapus_anggota()
- pinjam_buku()
- kembalikan_buku()
- cari_buku()
- cari_anggota()

---

## Class Laporan

Methods

- laporan_buku()
- laporan_anggota()
- laporan_transaksi()
- laporan_denda()

---

# 4. Relationships

Pengguna

├── Anggota

└── Petugas

Perpustakaan

├── Buku

├── Anggota

├── Peminjaman

└── Laporan

Peminjaman

├── Buku

├── Anggota

└── Denda

---

# 5. Data Storage

Format:

JSON

Files:

buku.json

anggota.json

transaksi.json

petugas.json

---

# 6. Exception Handling

Handle:

- Buku tidak ditemukan
- Anggota tidak ditemukan
- Buku habis
- Data duplikat
- Login gagal
- File JSON rusak
- File tidak ditemukan

---

# 7. Validation

Validasi:

- ID unik
- Nama tidak boleh kosong
- Stok >= 0
- Tahun berupa integer
- Nomor telepon valid
- Password minimal 8 karakter

---

# 8. Future Improvements

- GUI menggunakan Tkinter
- Database SQLite
- Export PDF
- Export Excel
- Barcode Scanner
- QR Code
- REST API menggunakan FastAPI
- Web Dashboard
- Multi User
- Role Based Access Control

---

# 9. Coding Standard

- Mengikuti PEP8
- Type Hint
- Docstring
- SOLID Principle
- Separation of Concerns
- Dependency Injection sederhana

---

# 10. Recommended Libraries

Standard Library

- datetime
- json
- pathlib
- hashlib
- uuid
- abc
- typing
- dataclasses

Optional

- rich
- tabulate
- colorama

---

# 11. Agent Instructions

Code Generation Rules

- Gunakan Python 3.12+
- Gunakan Object Oriented Programming
- Gunakan Abstract Class
- Gunakan Inheritance
- Gunakan Encapsulation
- Gunakan Polymorphism
- Gunakan Type Hint
- Pisahkan setiap class ke file masing-masing
- Gunakan JSON sebagai database
- Semua operasi CRUD melalui service layer
- Semua input harus divalidasi
- Tambahkan docstring pada seluruh class dan method
- Tambahkan unit test jika memungkinkan