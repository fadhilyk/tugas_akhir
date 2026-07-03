# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 1.0.x | ✅ Active |
| < 1.0 | ❌ Not supported |

## Reporting a Vulnerability

Kami sangat menghargai kontribusi komunitas dalam menjaga keamanan proyek ini.

**Mohon jangan melaporkan kerentanan keamanan melalui public GitHub Issues.**

### Responsible Disclosure Process

1. **Laporkan** kerentanan dengan membuka issue di repository GitHub dengan label `security`
2. **Sertakan** deskripsi lengkap, langkah reproduksi, dan dampak potensial
3. **Tunggu** konfirmasi dari maintainer (biasanya dalam 48 jam)
4. **Kolaborasi** untuk memperbaiki kerentanan sebelum dipublikasikan

## Security Measures

### Password Storage

- Password pengguna tidak pernah disimpan dalam plaintext
- Menggunakan **SHA256 hashing** dengan `hashlib`
- Setiap password di-hash sebelum disimpan ke file JSON

### Data Storage

- Data disimpan dalam format **JSON** di direktori `library_system/data/`
- File JSON menggunakan **UTF-8 encoding**
- Tidak ada data sensitif yang disimpan tanpa proteksi

### Input Validation

- Semua input dari pengguna divalidasi sebelum diproses
- Validasi dilakukan di:
  - **Presentation Layer**: Tipe data dasar (string, integer)
  - **Service Layer**: Business rules (stok, limit, duplikasi)
  - **Model Layer**: Data invariants (`__post_init__`)

### Error Handling

- Tidak ada stack trace yang ditampilkan ke pengguna
- Semua error dicatat dalam log (`logs/library.log`)
- Custom exceptions memisahkan error bisnis dari system error

### File Security

- Direktori `logs/` dan `data/` ditambahkan ke `.gitignore`
- Riwayat transaksi dan data anggota aman dari commit tidak sengaja

## Best Practices untuk Pengguna

1. Gunakan **password yang kuat** (minimal 8 karakter, kombinasi huruf dan angka)
2. **Logout** setelah selesai menggunakan aplikasi
3. **Backup** file JSON secara berkala
4. Jangan membagikan file `petugas.json` yang berisi password hash
5. Update ke versi terbaru untuk mendapatkan patch keamanan

## Dependency Security

- Hanya menggunakan library dari Python Standard Library
- Library opsional (`tabulate`, `rich`, `colorama`) hanya untuk formatting CLI
- Tidak ada dependency eksternal yang memproses data sensitif

## Questions?

Jika Anda memiliki pertanyaan terkait keamanan, silakan buka issue di repository.
