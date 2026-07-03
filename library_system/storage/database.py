"""
Module untuk Database.

Module ini menangani operasi read/write ke JSON storage.
"""

import json
import shutil
from pathlib import Path
from typing import Any
from datetime import datetime
from ..models import Buku, Anggota, Petugas, Peminjaman, Denda
from ..exceptions import DatabaseError
from ..utils.logger import setup_logger, log_action, log_error


class Database:
    """
    Class untuk menangani persistent storage menggunakan JSON.
    
    Attributes:
        data_dir: Path ke direktori data
        buku_file: Path ke file buku.json
        anggota_file: Path ke file anggota.json
        petugas_file: Path ke file petugas.json
        transaksi_file: Path ke file transaksi.json
    """
    
    def __init__(self, data_dir: str = "library_system/data") -> None:
        """
        Inisialisasi Database dengan path ke direktori data.
        
        Args:
            data_dir: Path ke direktori data (default: library_system/data)
        """
        self.data_dir = Path(data_dir)
        self.buku_file = self.data_dir / "buku.json"
        self.anggota_file = self.data_dir / "anggota.json"
        self.petugas_file = self.data_dir / "petugas.json"
        self.transaksi_file = self.data_dir / "transaksi.json"
        self._logger = setup_logger()
        
        self._ensure_data_directory()
        self._ensure_data_files()
    
    def _ensure_data_directory(self) -> None:
        """Memastikan direktori data exists."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _ensure_data_files(self) -> None:
        """Memastikan semua file JSON exists dengan default empty array."""
        for file_path in [self.buku_file, self.anggota_file, 
                          self.petugas_file, self.transaksi_file]:
            if not file_path.exists():
                self._write_json(file_path, [])
    
    def _read_json(self, file_path: Path) -> list[dict[str, Any]]:
        """
        Membaca file JSON.
        
        Args:
            file_path: Path ke file JSON
            
        Returns:
            List dictionary dari file JSON
            
        Raises:
            DatabaseError: Jika file corrupt atau invalid
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                if not isinstance(data, list):
                    raise DatabaseError(f"File {file_path.name} harus berisi array JSON")
                return data
        except json.JSONDecodeError as e:
            raise DatabaseError(f"File {file_path.name} corrupt: {e}")
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Error membaca {file_path.name}: {e}")
    
    def _write_json(self, file_path: Path, data: list[dict[str, Any]]) -> None:
        """
        Menulis data ke file JSON.
        
        Args:
            file_path: Path ke file JSON
            data: List dictionary yang akan ditulis
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _serialize_buku(self, buku: Buku) -> dict[str, Any]:
        """
        Serialize object Buku ke dictionary.
        
        Args:
            buku: Object Buku
            
        Returns:
            Dictionary representation
        """
        return {
            "id": buku.id,
            "judul": buku.judul,
            "penulis": buku.penulis,
            "penerbit": buku.penerbit,
            "tahun": buku.tahun,
            "kategori": buku.kategori,
            "stok": buku.stok
        }
    
    def _deserialize_buku(self, data: dict[str, Any]) -> Buku:
        """
        Deserialize dictionary ke object Buku.
        
        Args:
            data: Dictionary representation
            
        Returns:
            Object Buku
        """
        return Buku(
            id=data["id"],
            judul=data["judul"],
            penulis=data["penulis"],
            penerbit=data["penerbit"],
            tahun=data["tahun"],
            kategori=data["kategori"],
            stok=data["stok"]
        )
    
    def _serialize_anggota(self, anggota: Anggota) -> dict[str, Any]:
        """
        Serialize object Anggota ke dictionary.
        
        Args:
            anggota: Object Anggota
            
        Returns:
            Dictionary representation
        """
        return {
            "id": anggota.id,
            "nama": anggota.nama,
            "kontak": anggota.kontak,
            "alamat": anggota.alamat,
            "daftar_pinjaman": anggota.daftar_pinjaman
        }
    
    def _deserialize_anggota(self, data: dict[str, Any]) -> Anggota:
        """
        Deserialize dictionary ke object Anggota.
        
        Args:
            data: Dictionary representation
            
        Returns:
            Object Anggota
        """
        return Anggota(
            id=data["id"],
            nama=data["nama"],
            kontak=data["kontak"],
            alamat=data.get("alamat", ""),
            daftar_pinjaman=data.get("daftar_pinjaman", [])
        )
    
    def _serialize_petugas(self, petugas: Petugas) -> dict[str, Any]:
        """
        Serialize object Petugas ke dictionary.
        
        Args:
            petugas: Object Petugas
            
        Returns:
            Dictionary representation
        """
        return {
            "id": petugas.id,
            "nama": petugas.nama,
            "kontak": petugas.kontak,
            "username": petugas.username,
            "password_hash": petugas.password_hash
        }
    
    def _deserialize_petugas(self, data: dict[str, Any]) -> Petugas:
        """
        Deserialize dictionary ke object Petugas.
        
        Args:
            data: Dictionary representation
            
        Returns:
            Object Petugas
        """
        return Petugas(
            id=data["id"],
            nama=data["nama"],
            kontak=data["kontak"],
            username=data["username"],
            password_hash=data.get("password_hash", "")
        )
    
    def _serialize_denda(self, denda: Denda) -> dict[str, Any]:
        """
        Serialize object Denda ke dictionary.
        
        Args:
            denda: Object Denda
            
        Returns:
            Dictionary representation
        """
        return {
            "nominal": denda.nominal,
            "status_pembayaran": denda.status_pembayaran
        }
    
    def _deserialize_denda(self, data: dict[str, Any]) -> Denda:
        """
        Deserialize dictionary ke object Denda.
        
        Args:
            data: Dictionary representation
            
        Returns:
            Object Denda
        """
        return Denda(
            nominal=data.get("nominal", 0),
            status_pembayaran=data.get("status_pembayaran", False)
        )
    
    def _serialize_peminjaman(self, peminjaman: Peminjaman) -> dict[str, Any]:
        """
        Serialize object Peminjaman ke dictionary.
        
        Args:
            peminjaman: Object Peminjaman
            
        Returns:
            Dictionary representation
        """
        return {
            "id": peminjaman.id,
            "anggota_id": peminjaman.anggota_id,
            "buku_id": peminjaman.buku_id,
            "tanggal_pinjam": peminjaman.tanggal_pinjam.isoformat(),
            "jatuh_tempo": peminjaman.jatuh_tempo.isoformat(),
            "tanggal_kembali": peminjaman.tanggal_kembali.isoformat() if peminjaman.tanggal_kembali else None,
            "status": peminjaman.status,
            "denda": self._serialize_denda(peminjaman.denda)
        }
    
    def _deserialize_peminjaman(self, data: dict[str, Any]) -> Peminjaman:
        """
        Deserialize dictionary ke object Peminjaman.
        
        Args:
            data: Dictionary representation
            
        Returns:
            Object Peminjaman
        """
        tanggal_kembali = None
        if data.get("tanggal_kembali"):
            tanggal_kembali = datetime.fromisoformat(data["tanggal_kembali"])
        
        denda = self._deserialize_denda(data.get("denda", {}))
        
        return Peminjaman(
            id=data["id"],
            anggota_id=data["anggota_id"],
            buku_id=data["buku_id"],
            tanggal_pinjam=datetime.fromisoformat(data["tanggal_pinjam"]),
            jatuh_tempo=datetime.fromisoformat(data["jatuh_tempo"]),
            tanggal_kembali=tanggal_kembali,
            status=data.get("status", "aktif"),
            denda=denda
        )
    
    def load_buku(self) -> list[Buku]:
        """
        Load semua buku dari file JSON.
        
        Returns:
            List object Buku
        """
        try:
            data = self._read_json(self.buku_file)
            books = [self._deserialize_buku(item) for item in data]
            log_action(self._logger, "LOAD_DATA", f"Loaded {len(books)} books from database")
            return books
        except Exception as e:
            log_error(self._logger, e, "load_buku")
            return []
    
    def save_buku(self, buku_list: list[Buku]) -> None:
        """
        Save semua buku ke file JSON.
        
        Args:
            buku_list: List object Buku
        """
        try:
            data = [self._serialize_buku(buku) for buku in buku_list]
            self._write_json(self.buku_file, data)
            log_action(self._logger, "SAVE_DATA", f"Saved {len(buku_list)} books to database")
        except Exception as e:
            log_error(self._logger, e, "save_buku")
            raise DatabaseError(f"Failed to save books: {e}")
    
    def load_anggota(self) -> list[Anggota]:
        """
        Load semua anggota dari file JSON.
        
        Returns:
            List object Anggota
        """
        try:
            data = self._read_json(self.anggota_file)
            members = [self._deserialize_anggota(item) for item in data]
            log_action(self._logger, "LOAD_DATA", f"Loaded {len(members)} members from database")
            return members
        except Exception as e:
            log_error(self._logger, e, "load_anggota")
            return []
    
    def save_anggota(self, anggota_list: list[Anggota]) -> None:
        """
        Save semua anggota ke file JSON.
        
        Args:
            anggota_list: List object Anggota
        """
        try:
            data = [self._serialize_anggota(anggota) for anggota in anggota_list]
            self._write_json(self.anggota_file, data)
            log_action(self._logger, "SAVE_DATA", f"Saved {len(anggota_list)} members to database")
        except Exception as e:
            log_error(self._logger, e, "save_anggota")
            raise DatabaseError(f"Failed to save members: {e}")
    
    def load_petugas(self) -> list[Petugas]:
        """
        Load semua petugas dari file JSON.
        
        Returns:
            List object Petugas
        """
        try:
            data = self._read_json(self.petugas_file)
            staff = [self._deserialize_petugas(item) for item in data]
            log_action(self._logger, "LOAD_DATA", f"Loaded {len(staff)} staff from database")
            return staff
        except Exception as e:
            log_error(self._logger, e, "load_petugas")
            return []
    
    def save_petugas(self, petugas_list: list[Petugas]) -> None:
        """
        Save semua petugas ke file JSON.
        
        Args:
            petugas_list: List object Petugas
        """
        try:
            data = [self._serialize_petugas(petugas) for petugas in petugas_list]
            self._write_json(self.petugas_file, data)
            log_action(self._logger, "SAVE_DATA", f"Saved {len(petugas_list)} staff to database")
        except Exception as e:
            log_error(self._logger, e, "save_petugas")
            raise DatabaseError(f"Failed to save staff: {e}")
    
    def load_transaksi(self) -> list[Peminjaman]:
        """
        Load semua transaksi peminjaman dari file JSON.
        
        Returns:
            List object Peminjaman
        """
        try:
            data = self._read_json(self.transaksi_file)
            transactions = [self._deserialize_peminjaman(item) for item in data]
            log_action(self._logger, "LOAD_DATA", f"Loaded {len(transactions)} transactions from database")
            return transactions
        except Exception as e:
            log_error(self._logger, e, "load_transaksi")
            return []
    
    def save_transaksi(self, transaksi_list: list[Peminjaman]) -> None:
        """
        Save semua transaksi peminjaman ke file JSON.
        
        Args:
            transaksi_list: List object Peminjaman
        """
        try:
            data = [self._serialize_peminjaman(peminjaman) for peminjaman in transaksi_list]
            self._write_json(self.transaksi_file, data)
            log_action(self._logger, "SAVE_DATA", f"Saved {len(transaksi_list)} transactions to database")
        except Exception as e:
            log_error(self._logger, e, "save_transaksi")
            raise DatabaseError(f"Failed to save transactions: {e}")
    
    def backup(self, backup_suffix: str = None) -> None:
        """
        Membuat backup dari semua file JSON.
        
        Args:
            backup_suffix: Suffix untuk file backup (default: timestamp)
        """
        if backup_suffix is None:
            backup_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        backup_dir = self.data_dir / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        for file_path in [self.buku_file, self.anggota_file, 
                          self.petugas_file, self.transaksi_file]:
            if file_path.exists():
                backup_path = backup_dir / f"{file_path.stem}_{backup_suffix}.json"
                shutil.copy2(file_path, backup_path)
