"""
Module untuk class Anggota.

Class ini merepresentasikan anggota perpustakaan.
"""

from dataclasses import dataclass, field
from .pengguna import Pengguna

MAX_PINJAMAN = 5


@dataclass
class Anggota(Pengguna):
    """
    Class untuk anggota perpustakaan.
    
    Attributes:
        id: Unique identifier untuk anggota
        nama: Nama lengkap anggota
        kontak: Informasi kontak anggota
        alamat: Alamat lengkap anggota
        daftar_pinjaman: List ID peminjaman yang sedang aktif
    """
    
    alamat: str = ""
    daftar_pinjaman: list[str] = field(default_factory=list)
    
    def tampilkan_info(self) -> dict[str, str]:
        """
        Menampilkan informasi anggota.
        
        Returns:
            Dictionary berisi informasi anggota
        """
        return {
            "id": self.id,
            "nama": self.nama,
            "kontak": self.kontak,
            "alamat": self.alamat,
            "jumlah_pinjaman": str(len(self.daftar_pinjaman))
        }
    
    def pinjam(self, peminjaman_id: str) -> None:
        """
        Menambahkan peminjaman ke daftar pinjaman anggota.
        
        Args:
            peminjaman_id: ID transaksi peminjaman
            
        Raises:
            ValueError: Jika anggota sudah mencapai batas maksimal peminjaman
        """
        if len(self.daftar_pinjaman) >= MAX_PINJAMAN:
            raise ValueError(f"Anggota tidak dapat meminjam lebih dari {MAX_PINJAMAN} buku")
        
        if peminjaman_id not in self.daftar_pinjaman:
            self.daftar_pinjaman.append(peminjaman_id)
    
    def kembali(self, peminjaman_id: str) -> None:
        """
        Menghapus peminjaman dari daftar pinjaman anggota.
        
        Args:
            peminjaman_id: ID transaksi peminjaman
            
        Raises:
            ValueError: Jika peminjaman tidak ditemukan
        """
        if peminjaman_id not in self.daftar_pinjaman:
            raise ValueError("Peminjaman tidak ditemukan dalam daftar pinjaman anggota")
        
        self.daftar_pinjaman.remove(peminjaman_id)
    
    def jumlah_pinjaman(self) -> int:
        """
        Mendapatkan jumlah buku yang sedang dipinjam.
        
        Returns:
            Jumlah buku yang sedang dipinjam
        """
        return len(self.daftar_pinjaman)
