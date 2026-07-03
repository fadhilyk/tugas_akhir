# User Guide

Panduan penggunaan aplikasi Sistem Manajemen Perpustakaan Digital.

---

## Getting Started

### Running the Application

```bash
python library_system/main.py
```

### First Run

Saat pertama kali menjalankan aplikasi, Anda perlu mendaftarkan akun staff:

1. Pilih opsi **2. Register New Staff** dari menu login
2. Isi data staff:
   - **Staff ID**: ID unik (contoh: `P001`)
   - **Full Name**: Nama lengkap
   - **Contact**: Nomor telepon
   - **Username**: Username untuk login
   - **Password**: Password (minimal 8 karakter)
3. Setelah registrasi berhasil, login dengan username dan password

---

## Login Menu

```
=================================================
                  LOGIN MENU
=================================================
1. Login
2. Register New Staff (First Time Setup)
3. Exit
-------------------------------------------------
Choose option:
```

Seluruh akses ke sistem memerlukan login terlebih dahulu.

---

## Main Menu

Setelah login berhasil, menu utama akan tampil:

```
=================================================
                  MAIN MENU
=================================================
Logged in as: Admin User
-------------------------------------------------
1. Book Management
2. Member Management
3. Borrow Book
4. Return Book
5. Reports
6. Logout
7. Exit
-------------------------------------------------
Choose option:
```

---

## Book Management

### Menu

```
=================================================
              BOOK MANAGEMENT
=================================================
1. Add Book
2. Edit Book
3. Delete Book
4. Search Book
5. List All Books
0. Back to Main Menu
-------------------------------------------------
Choose option:
```

### Add Book

Masukkan data buku yang akan ditambahkan:

```
Book ID: B001
Title: Python Programming
Author: John Doe
Publisher: Tech Publisher
Publication Year: 2023
Category: Programming
Stock: 5
```

Setiap ID buku harus unik. Stok tidak boleh negatif.

### Edit Book

Masukkan ID buku yang akan diedit. Field yang dikosongkan akan menggunakan nilai lama:

```
Book ID to edit: B001

Current: Python Programming by John Doe
Leave blank to keep current value
-------------------------------------------------
New Title: Advanced Python
New Author:
New Publisher:
New Year: 2024
New Category:
New Stock:
```

### Search Book

Cari buku berdasarkan judul, penulis, atau kategori:

```
Enter search keyword (title/author/category): Python
```

Hasil pencarian case-insensitive.

### Delete Book

Hapus buku dengan konfirmasi:

```
Book ID to delete: B001

Book: Python Programming by John Doe
Are you sure you want to delete this book? (y/n): y
```

Buku yang sedang dipinjam tidak dapat dihapus.

---

## Member Management

### Menu

```
=================================================
             MEMBER MANAGEMENT
=================================================
1. Add Member
2. Edit Member
3. Delete Member
4. Search Member
5. List All Members
0. Back to Main Menu
-------------------------------------------------
Choose option:
```

### Add Member

```
Member ID: A001
Full Name: Alice Johnson
Contact: 081234567890
Address: Jl. Merdeka No. 1
```

### Edit Member

```
Member ID to edit: A001

Current: Alice Johnson
Leave blank to keep current value
-------------------------------------------------
New Name: Alice J.
New Contact:
New Address:
```

### Delete Member

Anggota yang masih memiliki pinjaman aktif tidak dapat dihapus.

---

## Borrow Book

### Flow

1. Dari menu utama, pilih **3. Borrow Book**
2. Masukkan ID anggota dan ID buku
3. Sistem akan memvalidasi:
   - Apakah anggota terdaftar
   - Apakah buku tersedia (stok > 0)
   - Apakah anggota belum mencapai batas maksimal (5 buku)

### Contoh Output

```
==================================================
               BORROW SUCCESSFUL
==================================================
Transaction ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
Member: Alice Johnson
Book: Python Programming
Borrow Date: 2026-07-03 14:30
Due Date: 2026-07-10 14:30
Remaining Stock: 4
==================================================
```

### Business Rules

- Stok buku otomatis berkurang setelah peminjaman
- Jatuh tempo: 7 hari dari tanggal pinjam
- Anggota maksimal meminjam 5 buku
- Buku dengan stok 0 tidak dapat dipinjam
- Buku yang sudah dipinjam anggota tidak dapat dipinjam sampai dikembalikan

---

## Return Book

### Flow

1. Dari menu utama, pilih **4. Return Book**
2. Sistem akan menampilkan daftar peminjaman aktif
3. Masukkan Loan ID lengkap dari transaksi yang akan dikembalikan

### Contoh Output

```
Active Loans:
+-----------+-----------+----------+-----------+
| Loan ID   | Member    | Book     | Due Date  |
+-----------+-----------+----------+-----------+
| a1b2c3d4… | Alice J.  | Python…  | 2026-07-10|
+-----------+-----------+----------+-----------+

Loan ID to return: a1b2c3d4-e5f6-7890-abcd-ef1234567890

==================================================
               RETURN SUCCESSFUL
==================================================
Member: Alice J.
Book: Python Programming
Return Date: 2026-07-03 14:35
Late Days: 0
Fine: Rp 0
==================================================
```

### Fine Calculation

Jika pengembalian melebihi jatuh tempo, denda dihitung otomatis:

```
Late Days: 3
Fine: Rp 6,000
```

Rumus denda: `jumlah_hari_terlambat × Rp 2.000`

---

## Reports

### Menu

```
==================================================
                 REPORTS
==================================================
1. All Books
2. Available Books
3. Borrowed Books
4. Members
5. Transactions
6. Fines
7. Statistics
0. Back to Main Menu
-------------------------------------------------
Choose option:
```

### 1. All Books

Menampilkan semua buku dengan status ketersediaan.

| id | judul | penulis | penerbit | tahun | kategori | stok | status |
|---|---|---|---|---|---|---|---|
| B001 | Python Programming | John Doe | Tech Pub | 2023 | Programming | 5 | Tersedia |

### 2. Available Books

Hanya buku dengan stok > 0.

### 3. Borrowed Books

Buku yang sedang dipinjam beserta jumlah peminjaman aktif.

### 4. Members

Semua anggota dengan jumlah pinjaman aktif.

### 5. Transactions

Terdapat sub-menu untuk filter:

1. All Transactions
2. Active Loans
3. Completed Transactions

### 6. Fines

Laporan denda lengkap dengan total nominal.

### 7. Statistics

Ringkasan statistik perpustakaan:

```
==================================================
Total Books: 10
Total Stock: 45
Total Members: 3
Active Loans: 2
Completed Transactions: 5
Total Transactions: 7
Total Fines: Rp 12,000
==================================================
```

---

## Logout

Pilih **6. Logout** dari menu utama untuk keluar dari sesi. Anda akan kembali ke menu login.

## Exit

Pilih **7. Exit** untuk menutup aplikasi sepenuhnya.

---

## Tips

- Gunakan ID yang konsisten dan mudah diingat (contoh: `B001`, `A001`, `P001`)
- Periksa stok buku sebelum melakukan peminjaman
- Gunakan fitur search untuk mencari buku/anggota jika jumlahnya sudah banyak
- Cek laporan fine secara rutin untuk memonitor anggota yang terlambat
