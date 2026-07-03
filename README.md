# Sistem Manajemen Perpustakaan Digital

Aplikasi berbasis Python untuk mengelola seluruh aktivitas perpustakaan secara digital menggunakan prinsip Object-Oriented Programming.

## Features

- **Manajemen Buku**: Tambah, edit, hapus, dan cari buku
- **Manajemen Anggota**: Kelola data anggota perpustakaan
- **Transaksi Peminjaman**: Proses peminjaman buku dengan tracking stok otomatis
- **Pengembalian Buku**: Proses pengembalian dengan perhitungan denda otomatis
- **Laporan**: Generate berbagai laporan (buku, anggota, transaksi, denda)
- **Autentikasi**: Sistem login untuk petugas dengan password ter-hash
- **Validasi Input**: Validasi komprehensif untuk semua input pengguna
- **JSON Storage**: Penyimpanan data persisten menggunakan JSON

## Installation

### Prerequisites

- Python 3.12 atau lebih tinggi
- pip (Python package manager)

### Setup

1. Clone atau download repository ini

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi:
```bash
python library_system/main.py
```

## Project Structure

```
library_system/
├── main.py                    # Entry point aplikasi
├── models/                    # Model classes
│   ├── __init__.py
│   ├── pengguna.py           # Abstract base class
│   ├── anggota.py            # Class untuk anggota perpustakaan
│   ├── petugas.py            # Class untuk petugas
│   ├── buku.py               # Class untuk buku
│   ├── peminjaman.py         # Class untuk transaksi peminjaman
│   └── denda.py              # Class untuk denda
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── library_service.py    # Service untuk operasi perpustakaan
│   ├── auth_service.py       # Service untuk autentikasi
│   └── report_service.py     # Service untuk laporan
├── storage/                   # Data persistence layer
│   ├── __init__.py
│   └── database.py           # JSON database handler
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── validator.py          # Input validation
│   └── helper.py             # Helper functions
└── data/                      # JSON data files
    ├── buku.json             # Data buku
    ├── anggota.json          # Data anggota
    ├── transaksi.json        # Data transaksi
    └── petugas.json          # Data petugas
```

## Architecture

Aplikasi ini menggunakan layered architecture:

```
Presentation Layer (CLI)
         ↓
Service Layer (Business Logic)
         ↓
Repository/Data Layer
         ↓
JSON Storage
```

## Business Rules

- Buku dapat dipinjam jika stok > 0
- Anggota maksimal meminjam 5 buku
- Durasi peminjaman: 7 hari
- Denda keterlambatan: Rp 2.000/hari
- Buku yang belum dikembali tidak dapat dipinjam kembali

## Development

### Coding Standards

- Mengikuti PEP 8
- Type hints untuk semua fungsi
- Docstrings untuk semua class dan method
- SOLID principles
- Separation of concerns

### Recommended Libraries

- Standard Library: `datetime`, `json`, `pathlib`, `hashlib`, `uuid`, `abc`, `typing`, `dataclasses`
- Optional: `rich`, `tabulate`, `colorama`

## License

Academic Project - For Educational Purposes
