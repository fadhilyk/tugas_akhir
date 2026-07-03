"""
Custom exceptions untuk Library Management System.

Module ini mendefinisikan exception hierarchy untuk error handling yang lebih baik.
"""


class LibraryError(Exception):
    """
    Base exception untuk semua error dalam library system.
    
    Args:
        message: Pesan error yang menjelaskan masalah
    """
    
    def __init__(self, message: str) -> None:
        """Initialize LibraryError dengan message."""
        self.message = message
        super().__init__(self.message)


class AuthenticationError(LibraryError):
    """
    Exception untuk error autentikasi dan otorisasi.
    
    Raised when:
        - Login gagal (username tidak ditemukan atau password salah)
        - Tidak ada user yang login saat mengakses fitur
        - Username sudah digunakan
    """
    pass


class BookNotFoundError(LibraryError):
    """
    Exception ketika buku tidak ditemukan.
    
    Raised when:
        - Mencari buku dengan ID yang tidak ada
        - Mengakses buku yang sudah dihapus
    """
    pass


class MemberNotFoundError(LibraryError):
    """
    Exception ketika anggota tidak ditemukan.
    
    Raised when:
        - Mencari anggota dengan ID yang tidak ada
        - Mengakses anggota yang sudah dihapus
    """
    pass


class LoanNotFoundError(LibraryError):
    """
    Exception ketika transaksi peminjaman tidak ditemukan.
    
    Raised when:
        - Mencari peminjaman dengan ID yang tidak ada
        - Mengakses transaksi yang tidak valid
    """
    pass


class BookUnavailableError(LibraryError):
    """
    Exception ketika buku tidak tersedia untuk dipinjam.
    
    Raised when:
        - Stok buku habis (stok = 0)
        - Buku sedang dalam maintenance
    """
    pass


class DuplicateIDError(LibraryError):
    """
    Exception ketika ID sudah digunakan.
    
    Raised when:
        - Menambah buku dengan ID yang sudah ada
        - Menambah anggota dengan ID yang sudah ada
        - Menambah petugas dengan ID yang sudah ada
        - Username sudah digunakan
    """
    pass


class MaximumLoanReachedError(LibraryError):
    """
    Exception ketika anggota mencapai batas maksimal peminjaman.
    
    Raised when:
        - Anggota sudah meminjam 5 buku (MAX_PINJAMAN)
        - Mencoba meminjam buku saat sudah mencapai limit
    """
    pass


class InvalidInputError(LibraryError):
    """
    Exception untuk input yang tidak valid.
    
    Raised when:
        - Data kosong/null yang tidak diizinkan
        - Format data tidak sesuai (contoh: tahun bukan integer)
        - Nilai negatif untuk field yang harus positif
        - Password terlalu pendek
    """
    pass


class DatabaseError(LibraryError):
    """
    Exception untuk error database/storage.
    
    Raised when:
        - File JSON corrupt
        - Gagal membaca file
        - Gagal menulis file
        - Permission denied
    """
    pass
