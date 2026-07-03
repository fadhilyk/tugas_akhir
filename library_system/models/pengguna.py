"""
Module untuk abstract class Pengguna.

Class ini merupakan base class untuk Anggota dan Petugas.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Pengguna(ABC):
    """
    Abstract base class untuk pengguna sistem perpustakaan.
    
    Attributes:
        id: Unique identifier untuk pengguna
        nama: Nama lengkap pengguna
        kontak: Informasi kontak (nomor telepon/email)
    """
    
    id: str
    nama: str
    kontak: str
    
    def __post_init__(self) -> None:
        """
        Validasi data setelah inisialisasi.
        
        Raises:
            ValueError: Jika nama kosong atau kontak kosong
        """
        if not self.nama or not self.nama.strip():
            raise ValueError("Nama tidak boleh kosong")
        if not self.kontak or not self.kontak.strip():
            raise ValueError("Kontak tidak boleh kosong")
    
    @abstractmethod
    def tampilkan_info(self) -> dict[str, str]:
        """
        Menampilkan informasi pengguna.
        
        Returns:
            Dictionary berisi informasi pengguna
        """
        pass
