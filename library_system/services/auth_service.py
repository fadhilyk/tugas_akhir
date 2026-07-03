"""
Module untuk AuthService.

Service ini menangani autentikasi dan otorisasi pengguna.
"""

import hashlib
from typing import Optional
from ..models import Petugas
from ..storage.database import Database
from ..exceptions import (
    AuthenticationError,
    DuplicateIDError,
    InvalidInputError
)
from ..utils.validator import validate_password, validate_non_empty_string
from ..utils.logger import setup_logger, log_action, log_error


class AuthService:
    """
    Service untuk menangani autentikasi dan otorisasi petugas.
    
    Attributes:
        _petugas_list: List petugas yang terdaftar
        _current_user: Petugas yang sedang login
        _database: Instance Database untuk persistent storage
        _logger: Logger instance untuk logging
    """
    
    def __init__(self, database: Database = None) -> None:
        """
        Inisialisasi AuthService dengan data dari database.
        
        Args:
            database: Instance Database (default: new Database instance)
        """
        self._database = database if database else Database()
        self._petugas_list: list[Petugas] = self._database.load_petugas()
        self._current_user: Optional[Petugas] = None
        self._logger = setup_logger()
    
    def _hash_password(self, password: str) -> str:
        """
        Melakukan hashing password menggunakan SHA256.
        
        Args:
            password: Password plaintext
            
        Returns:
            Hash password dalam format hexadecimal
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
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
            DuplicateIDError: Jika ID atau username sudah digunakan
            InvalidInputError: Jika password tidak memenuhi requirements
        """
        try:
            if self._find_petugas_by_id(id):
                raise DuplicateIDError(f"ID petugas '{id}' sudah terdaftar")
            
            if self._find_petugas_by_username(username):
                raise DuplicateIDError(f"Username '{username}' sudah digunakan")
            
            validate_password(password)
            
            password_hash = self._hash_password(password)
            
            petugas = Petugas(
                id=id,
                nama=nama,
                kontak=kontak,
                username=username,
                password_hash=password_hash
            )
            
            self._petugas_list.append(petugas)
            self._database.save_petugas(self._petugas_list)
            
            log_action(self._logger, "REGISTER_STAFF", f"Staff registered: {nama} (username: {username})")
            
            return petugas
        except Exception as e:
            log_error(self._logger, e, "register_petugas")
            raise
    
    def login(self, username: str, password: str) -> Petugas:
        """
        Login petugas ke sistem.
        
        Args:
            username: Username petugas
            password: Password plaintext
            
        Returns:
            Object Petugas yang berhasil login
            
        Raises:
            AuthenticationError: Jika username tidak ditemukan atau password salah
        """
        try:
            validate_non_empty_string(username, "Username")
            validate_non_empty_string(password, "Password")
            
            petugas = self._find_petugas_by_username(username)
            
            if not petugas:
                raise AuthenticationError("Username tidak ditemukan")
            
            password_hash = self._hash_password(password)
            
            if petugas.password_hash != password_hash:
                raise AuthenticationError("Password salah")
            
            self._current_user = petugas
            
            log_action(self._logger, "LOGIN", f"Login successful", user=username)
            
            return petugas
        except Exception as e:
            log_error(self._logger, e, f"login attempt for username: {username}")
            raise
    
    def logout(self) -> None:
        """
        Logout petugas dari sistem.
        
        Raises:
            AuthenticationError: Jika tidak ada user yang sedang login
        """
        if not self._current_user:
            raise AuthenticationError("Tidak ada user yang sedang login")
        
        username = self._current_user.username
        self._current_user = None
        
        log_action(self._logger, "LOGOUT", f"Logout successful", user=username)
    
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
