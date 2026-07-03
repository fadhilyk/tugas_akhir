# Product Requirements Document (PRD)

# Sistem Manajemen Perpustakaan Digital

Version: 1.0

Language:
- Python 3.12+

---

# 1. Overview

Sistem Manajemen Perpustakaan Digital merupakan aplikasi desktop/CLI berbasis Python yang digunakan untuk mengelola seluruh aktivitas perpustakaan secara digital.

Sistem memungkinkan petugas untuk:

- Mengelola data buku
- Mengelola data anggota
- Melakukan transaksi peminjaman
- Melakukan pengembalian
- Menghasilkan laporan

---

# 2. Goals

Tujuan sistem:

- Mengurangi pencatatan manual
- Mempermudah pencarian buku
- Mempermudah transaksi peminjaman
- Mengetahui stok buku secara realtime
- Menyimpan histori transaksi

---

# 3. Target User

### Petugas

Dapat:

- Login
- CRUD Buku
- CRUD Anggota
- Melakukan peminjaman
- Melakukan pengembalian
- Melihat laporan

### Anggota

Dapat:

- Melihat daftar buku
- Melihat status pinjaman

---

# 4. Functional Requirements

## FR-01 Login

Petugas dapat login menggunakan username dan password.

---

## FR-02 Kelola Buku

Petugas dapat:

- Tambah buku
- Edit buku
- Hapus buku
- Cari buku
- Lihat seluruh buku

Atribut buku:

- id
- judul
- penulis
- penerbit
- tahun
- kategori
- stok

---

## FR-03 Kelola Anggota

Petugas dapat:

- Tambah anggota
- Edit anggota
- Hapus anggota
- Cari anggota

Atribut:

- id
- nama
- alamat
- nomor telepon

---

## FR-04 Peminjaman

Petugas memilih:

- anggota
- buku

Kemudian sistem:

- mengurangi stok
- membuat transaksi
- menyimpan tanggal pinjam
- menghitung jatuh tempo

---

## FR-05 Pengembalian

Saat buku dikembalikan sistem:

- menambah stok
- menghitung keterlambatan
- menghitung denda
- memperbarui status transaksi

---

## FR-06 Riwayat

Menampilkan seluruh transaksi.

Filter:

- anggota
- buku
- tanggal

---

## FR-07 Laporan

Laporan:

- Daftar buku
- Daftar anggota
- Buku tersedia
- Buku dipinjam
- Riwayat transaksi
- Denda

---

# 5. Non Functional Requirements

## Performance

- Respon < 2 detik
- Mendukung minimal 10.000 data buku

## Reliability

- Tidak boleh kehilangan data
- Validasi seluruh input

## Maintainability

- Menggunakan OOP
- Mudah ditambahkan fitur

## Security

- Password di-hash
- Validasi input
- Error handling

---

# 6. Business Rules

- Satu buku dapat dipinjam apabila stok > 0
- Anggota tidak boleh meminjam lebih dari 5 buku
- Lama pinjam 7 hari
- Denda Rp2000/hari keterlambatan
- Buku yang belum dikembalikan tidak dapat dipinjam kembali

---

# 7. Success Criteria

Sistem dianggap berhasil apabila:

- Seluruh CRUD berjalan
- Peminjaman berhasil
- Pengembalian berhasil
- Denda dihitung otomatis
- Laporan dapat ditampilkan