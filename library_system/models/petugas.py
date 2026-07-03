"""
Module untuk class Petugas.

Class ini merepresentasikan petugas perpustakaan.
"""

from dataclasses import dataclass
from .pengguna import Pengguna


@dataclass
class Petugas(Pengguna):
    """
    Class untuk petugas perpustakaan.
    
    Attributes:
        id: Unique identifier untuk petugas
        nama: Nama lengkap petugas
        kontak: Informasi kontak petugas
        username: Username untuk login
        password_hash: Hash password untuk autentikasi
    """
    
    username: str = ""
    password_hash: str = ""
    
    def __post_init__(self) -> None:
        """
        Validasi data setelah inisialisasi.
        
        Raises:
            ValueError: Jika username kosong
        """
        super().__post_init__()
        
        if not self.username or not self.username.strip():
            raise ValueError("Username tidak boleh kosong")
    
    def tampilkan_info(self) -> dict[str, str]:
        """
        Menampilkan informasi petugas.
        
        Returns:
            Dictionary berisi informasi petugas
        """
        return {
            "id": self.id,
            "nama": self.nama,
            "kontak": self.kontak,
            "username": self.username
        }
