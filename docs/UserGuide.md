# Panduan Pengguna

Panduan penggunaan aplikasi Sistem Manajemen Perpustakaan Digital.

---

## Memulai

### Menjalankan Aplikasi

```bash
python library_system/main.py
```

### Pertama Kali Menjalankan

Saat pertama kali menjalankan aplikasi, Anda perlu mendaftarkan akun staff:

1. Pilih opsi **2. Daftar Staff Baru (Pengaturan Awal)** dari menu login
2. Isi data staff:
   - **ID Staff**: ID unik (contoh: `P001`)
   - **Nama Lengkap**: Nama lengkap
   - **Kontak**: Nomor telepon
   - **Username**: Username untuk login
   - **Password**: Password (minimal 8 karakter)
3. Setelah registrasi berhasil, login dengan username dan password

---

## Menu Login

```
=================================================
                  MENU LOGIN
=================================================
1. Login
2. Daftar Staff Baru (Pengaturan Awal)
3. Keluar
-------------------------------------------------
Pilih menu:
```

Seluruh akses ke sistem memerlukan login terlebih dahulu.

---

## Menu Utama

Setelah login berhasil, menu utama akan tampil:

```
=================================================
                  MENU UTAMA
=================================================
Login sebagai: Admin User
-------------------------------------------------
1. Manajemen Buku
2. Manajemen Anggota
3. Peminjaman Buku
4. Pengembalian Buku
5. Laporan
6. Logout
7. Keluar
-------------------------------------------------
Pilih menu:
```

---

## Manajemen Buku

### Menu

```
=================================================
               MANAJEMEN BUKU
=================================================
1. Tambah Buku
2. Ubah Buku
3. Hapus Buku
4. Cari Buku
5. Daftar Semua Buku
0. Kembali ke Menu Utama
-------------------------------------------------
Pilih menu:
```

### Tambah Buku

Masukkan data buku yang akan ditambahkan:

```
ID Buku: B001
Judul: Python Programming
Penulis: John Doe
Penerbit: Tech Publisher
Tahun Terbit: 2023
Kategori: Programming
Stok: 5
```

Setiap ID buku harus unik. Stok tidak boleh negatif.

### Ubah Buku

Masukkan ID buku yang akan diedit. Field yang dikosongkan akan menggunakan nilai lama:

```
ID Buku yang akan diubah: B001

Saat ini: Python Programming oleh John Doe
Kosongkan untuk mempertahankan nilai lama
-------------------------------------------------
Judul Baru: Advanced Python
Penulis Baru:
Penerbit Baru:
Tahun Baru: 2024
Kategori Baru:
Stok Baru:
```

### Cari Buku

Cari buku berdasarkan judul, penulis, atau kategori:

```
Masukkan kata kunci (judul/penulis/kategori): Python
```

Hasil pencarian case-insensitive.

### Hapus Buku

Hapus buku dengan konfirmasi:

```
ID Buku yang akan dihapus: B001

Buku: Python Programming oleh John Doe
Apakah Anda yakin ingin menghapus buku ini? (y/t): y
```

Buku yang sedang dipinjam tidak dapat dihapus.

---

## Manajemen Anggota

### Menu

```
=================================================
             MANAJEMEN ANGGOTA
=================================================
1. Tambah Anggota
2. Ubah Anggota
3. Hapus Anggota
4. Cari Anggota
5. Daftar Semua Anggota
0. Kembali ke Menu Utama
-------------------------------------------------
Pilih menu:
```

### Tambah Anggota

```
ID Anggota: A001
Nama Lengkap: Alice Johnson
Kontak: 081234567890
Alamat: Jl. Merdeka No. 1
```

### Ubah Anggota

```
ID Anggota yang akan diubah: A001

Saat ini: Alice Johnson
Kosongkan untuk mempertahankan nilai lama
-------------------------------------------------
Nama Baru: Alice J.
Kontak Baru:
Alamat Baru:
```

### Hapus Anggota

Anggota yang masih memiliki pinjaman aktif tidak dapat dihapus.

---

## Peminjaman Buku

### Alur

1. Dari menu utama, pilih **3. Peminjaman Buku**
2. Masukkan ID anggota dan ID buku
3. Sistem akan memvalidasi:
   - Apakah anggota terdaftar
   - Apakah buku tersedia (stok > 0)
   - Apakah anggota belum mencapai batas maksimal (5 buku)

### Contoh Output

```
==================================================
              PEMINJAMAN BERHASIL
==================================================
ID Transaksi: a1b2c3d4-e5f6-7890-abcd-ef1234567890
Anggota: Alice Johnson
Buku: Python Programming
Tanggal Pinjam: 2026-07-03 14:30
Jatuh Tempo: 2026-07-10 14:30
Sisa Stok: 4
==================================================
```

### Aturan Bisnis

- Stok buku otomatis berkurang setelah peminjaman
- Jatuh tempo: 7 hari dari tanggal pinjam
- Anggota maksimal meminjam 5 buku
- Buku dengan stok 0 tidak dapat dipinjam
- Buku yang sudah dipinjam anggota tidak dapat dipinjam sampai dikembalikan

---

## Pengembalian Buku

### Alur

1. Dari menu utama, pilih **4. Pengembalian Buku**
2. Sistem akan menampilkan daftar peminjaman aktif
3. Masukkan ID Pinjaman lengkap dari transaksi yang akan dikembalikan

### Contoh Output

```
Peminjaman Aktif:
+-------------+-----------+----------+-------------+
| ID Pinjaman | Anggota   | Buku     | Jatuh Tempo |
+-------------+-----------+----------+-------------+
| a1b2c3d4…   | Alice J.  | Python…  | 2026-07-10  |
+-------------+-----------+----------+-------------+

Masukkan ID Pinjaman lengkap: a1b2c3d4-e5f6-7890-abcd-ef1234567890

==================================================
             PENGEMBALIAN BERHASIL
==================================================
Anggota: Alice J.
Buku: Python Programming
Tanggal Kembali: 2026-07-03 14:35
Keterlambatan: 0 hari
Denda: Rp 0
==================================================
```

### Perhitungan Denda

Jika pengembalian melebihi jatuh tempo, denda dihitung otomatis:

```
Keterlambatan: 3 hari
Denda: Rp 6,000
```

Rumus denda: `jumlah_hari_terlambat × Rp 2.000`

---

## Laporan

### Menu

```
==================================================
                  LAPORAN
==================================================
1. Semua Buku
2. Buku Tersedia
3. Buku Dipinjam
4. Anggota
5. Transaksi
6. Denda
7. Statistik
0. Kembali ke Menu Utama
-------------------------------------------------
Pilih menu:
```

### 1. Semua Buku

Menampilkan semua buku dengan status ketersediaan.

| id | judul | penulis | penerbit | tahun | kategori | stok | status |
|---|---|---|---|---|---|---|---|
| B001 | Python Programming | John Doe | Tech Pub | 2023 | Programming | 5 | Tersedia |

### 2. Buku Tersedia

Hanya buku dengan stok > 0.

### 3. Buku Dipinjam

Buku yang sedang dipinjam beserta jumlah peminjaman aktif.

### 4. Anggota

Semua anggota dengan jumlah pinjaman aktif.

### 5. Transaksi

Terdapat sub-menu untuk filter:

1. Semua Transaksi
2. Peminjaman Aktif
3. Transaksi Selesai

### 6. Denda

Laporan denda lengkap dengan total nominal.

### 7. Statistik

Ringkasan statistik perpustakaan:

```
==================================================
Total Buku: 10
Total Stok: 45
Total Anggota: 3
Peminjaman Aktif: 2
Transaksi Selesai: 5
Total Transaksi: 7
Total Denda: Rp 12,000
==================================================
```

---

## Logout

Pilih **6. Logout** dari menu utama untuk keluar dari sesi. Anda akan kembali ke menu login.

## Keluar

Pilih **7. Keluar** untuk menutup aplikasi sepenuhnya.

---

## Tips

- Gunakan ID yang konsisten dan mudah diingat (contoh: `B001`, `A001`, `P001`)
- Periksa stok buku sebelum melakukan peminjaman
- Gunakan fitur cari untuk mencari buku/anggota jika jumlahnya sudah banyak
- Cek laporan denda secara rutin untuk memonitor anggota yang terlambat
