"""
Module untuk AuthService.

Service ini menangani autentikasi dan otorisasi pengguna.
"""

import hashlib
from typing import Optional
from ..models import Petugas


class AuthService:
    """
    Service untuk menangani autentikasi dan otorisasi petugas.
    
    Attributes:
        _petugas_list: List petugas yang terdaftar
        _current_user: Petugas yang sedang login
    """
    
    def __init__(self) -> None:
        """Inisialisasi AuthService dengan data kosong."""
        self._petugas_list: list[Petugas] = []
        self._current_user: Optional[Petugas] = None
    
    def _hash_password(self, password: str) -> str:
        """
        Melakukan hashing password menggunakan SHA256.
        
        Args:
            password: Password plaintext
            
        Returns:
            Hash password dalam format hexadecimal
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _validate_password(self, password: str) -> None:
        """
        Validasi password sesuai requirements.
        
        Args:
            password: Password yang akan divalidasi
            
        Raises:
            ValueError: Jika password tidak memenuhi requirements
        """
        if len(password) < 8:
            raise ValueError("Password minimal 8 karakter")
    
    def _find_petugas_by_username(self, username: str) -> Optional[Petugas]:
        """
        Mencari petugas berdasarkan username.
        
        Args:
            username: Username petugas
            
        Returns:
            Object Petugas jika ditemukan, None jika tidak
        """
        for petugas in self._petugas_list:
            if petugas.username == username:
                return petugas
        return None
    
    def _find_petugas_by_id(self, petugas_id: str) -> Optional[Petugas]:
        """
        Mencari petugas berdasarkan ID.
        
        Args:
            petugas_id: ID petugas
            
        Returns:
            Object Petugas jika ditemukan, None jika tidak
        """
        for petugas in self._petugas_list:
            if petugas.id == petugas_id:
                return petugas
        return None
    
    def register_petugas(self, id: str, nama: str, kontak: str, 
                        username: str, password: str) -> Petugas:
        """
        Mendaftarkan petugas baru ke sistem.
        
        Args:
            id: Unique identifier untuk petugas
            nama: Nama lengkap petugas
            kontak: Informasi kontak petugas
            username: Username untuk login
            password: Password plaintext
            
        Returns:
            Object Petugas yang baru dibuat
            
        Raises:
            ValueError: Jika ID atau username duplikat, atau password invalid
        """
        if self._find_petugas_by_id(id):
            raise ValueError(f"ID petugas '{id}' sudah terdaftar")
        
        if self._find_petugas_by_username(username):
            raise ValueError(f"Username '{username}' sudah digunakan")
        
        self._validate_password(password)
        
        password_hash = self._hash_password(password)
        
        petugas = Petugas(
            id=id,
            nama=nama,
            kontak=kontak,
            username=username,
            password_hash=password_hash
        )
        
        self._petugas_list.append(petugas)
        return petugas
    
    def login(self, username: str, password: str) -> Petugas:
        """
        Login petugas ke sistem.
        
        Args:
            username: Username petugas
            password: Password plaintext
            
        Returns:
            Object Petugas yang berhasil login
            
        Raises:
            ValueError: Jika username tidak ditemukan atau password salah
        """
        petugas = self._find_petugas_by_username(username)
        
        if not petugas:
            raise ValueError("Username tidak ditemukan")
        
        password_hash = self._hash_password(password)
        
        if petugas.password_hash != password_hash:
            raise ValueError("Password salah")
        
        self._current_user = petugas
        return petugas
    
    def logout(self) -> None:
        """
        Logout petugas dari sistem.
        
        Raises:
            ValueError: Jika tidak ada user yang sedang login
        """
        if not self._current_user:
            raise ValueError("Tidak ada user yang sedang login")
        
        self._current_user = None
    
    def get_current_user(self) -> Optional[Petugas]:
        """
        Mendapatkan petugas yang sedang login.
        
        Returns:
            Object Petugas jika ada yang login, None jika tidak
        """
        return self._current_user
    
    def is_logged_in(self) -> bool:
        """
        Mengecek apakah ada petugas yang sedang login.
        
        Returns:
            True jika ada yang login, False jika tidak
        """
        return self._current_user is not None
    
    def get_all_petugas(self) -> list[Petugas]:
        """
        Mendapatkan semua petugas yang terdaftar.
        
        Returns:
            List semua petugas
        """
        return self._petugas_list.copy()
