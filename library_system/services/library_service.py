"""
Module untuk LibraryService dengan custom exceptions dan logging.

Service ini menangani operasi perpustakaan seperti CRUD buku, anggota, dan transaksi.
"""

from typing import Optional
import uuid
from ..models import Buku, Anggota, Peminjaman, MAX_PINJAMAN
from ..storage.database import Database
from ..exceptions import (
    BookNotFoundError,
    MemberNotFoundError,
    LoanNotFoundError,
    BookUnavailableError,
    DuplicateIDError,
    MaximumLoanReachedError,
    InvalidInputError
)
from ..utils.validator import (
    validate_non_empty_string,
    validate_positive_integer,
    validate_integer_type
)
from ..utils.logger import setup_logger, log_action, log_error


class LibraryService:
    """
    Service untuk menangani operasi perpustakaan.
    
    Attributes:
        _buku_list: List buku dalam perpustakaan
        _anggota_list: List anggota perpustakaan
        _peminjaman_list: List transaksi peminjaman
        _database: Instance Database untuk persistent storage
        _logger: Logger instance untuk logging
    """
    
    def __init__(self, database: Database = None) -> None:
        """
        Inisialisasi LibraryService dengan data dari database.
        
        Args:
            database: Instance Database (default: new Database instance)
        """
        self._database = database if database else Database()
        self._buku_list: list[Buku] = self._database.load_buku()
        self._anggota_list: list[Anggota] = self._database.load_anggota()
        self._peminjaman_list: list[Peminjaman] = self._database.load_transaksi()
        self._logger = setup_logger()
    
    def _find_buku_by_id(self, buku_id: str) -> Optional[Buku]:
        """Mencari buku berdasarkan ID."""
        for buku in self._buku_list:
            if buku.id == buku_id:
                return buku
        return None
    
    def _find_anggota_by_id(self, anggota_id: str) -> Optional[Anggota]:
        """Mencari anggota berdasarkan ID."""
        for anggota in self._anggota_list:
            if anggota.id == anggota_id:
                return anggota
        return None
    
    def _find_peminjaman_by_id(self, peminjaman_id: str) -> Optional[Peminjaman]:
        """Mencari peminjaman berdasarkan ID."""
        for peminjaman in self._peminjaman_list:
            if peminjaman.id == peminjaman_id:
                return peminjaman
        return None
    
    def _get_buku_or_raise(self, buku_id: str) -> Buku:
        """Get buku by ID atau raise exception."""
        buku = self._find_buku_by_id(buku_id)
        if not buku:
            raise BookNotFoundError(f"Buku dengan ID '{buku_id}' tidak ditemukan")
        return buku
    
    def _get_anggota_or_raise(self, anggota_id: str) -> Anggota:
        """Get anggota by ID atau raise exception."""
        anggota = self._find_anggota_by_id(anggota_id)
        if not anggota:
            raise MemberNotFoundError(f"Anggota dengan ID '{anggota_id}' tidak ditemukan")
        return anggota
    
    def _get_peminjaman_or_raise(self, peminjaman_id: str) -> Peminjaman:
        """Get peminjaman by ID atau raise exception."""
        peminjaman = self._find_peminjaman_by_id(peminjaman_id)
        if not peminjaman:
            raise LoanNotFoundError(f"Peminjaman dengan ID '{peminjaman_id}' tidak ditemukan")
        return peminjaman
    
    def tambah_buku(self, id: str, judul: str, penulis: str, penerbit: str,
                    tahun: int, kategori: str, stok: int) -> Buku:
        """Menambahkan buku baru ke perpustakaan."""
        try:
            if self._find_buku_by_id(id):
                raise DuplicateIDError(f"Buku dengan ID '{id}' sudah ada")
            
            buku = Buku(id=id, judul=judul, penulis=penulis, penerbit=penerbit,
                       tahun=tahun, kategori=kategori, stok=stok)
            
            self._buku_list.append(buku)
            self._database.save_buku(self._buku_list)
            
            log_action(self._logger, "ADD_BOOK", f"Book added: {judul} (ID: {id})")
            
            return buku
        except Exception as e:
            log_error(self._logger, e, "tambah_buku")
            raise
    
    def edit_buku(self, id: str, judul: Optional[str] = None, 
                  penulis: Optional[str] = None, penerbit: Optional[str] = None,
                  tahun: Optional[int] = None, kategori: Optional[str] = None,
                  stok: Optional[int] = None) -> Buku:
        """Mengedit informasi buku."""
        try:
            buku = self._get_buku_or_raise(id)
            
            if judul is not None:
                validate_non_empty_string(judul, "Judul")
                buku.judul = judul
            
            if penulis is not None:
                validate_non_empty_string(penulis, "Penulis")
                buku.penulis = penulis
            
            if penerbit is not None:
                buku.penerbit = penerbit
            
            if tahun is not None:
                validate_integer_type(tahun, "Tahun")
                buku.tahun = tahun
            
            if kategori is not None:
                buku.kategori = kategori
            
            if stok is not None:
                validate_positive_integer(stok, "Stok")
                buku.stok = stok
            
            self._database.save_buku(self._buku_list)
            
            log_action(self._logger, "EDIT_BOOK", f"Book edited: {buku.judul} (ID: {id})")
            
            return buku
        except Exception as e:
            log_error(self._logger, e, "edit_buku")
            raise
    
    def hapus_buku(self, id: str) -> None:
        """Menghapus buku dari perpustakaan."""
        try:
            buku = self._get_buku_or_raise(id)
            
            for peminjaman in self._peminjaman_list:
                if peminjaman.buku_id == id and peminjaman.status == "aktif":
                    raise InvalidInputError("Buku masih dipinjam, tidak dapat dihapus")
            
            self._buku_list.remove(buku)
            self._database.save_buku(self._buku_list)
            
            log_action(self._logger, "DELETE_BOOK", f"Book deleted: {buku.judul} (ID: {id})")
            
        except Exception as e:
            log_error(self._logger, e, "hapus_buku")
            raise
    
    def cari_buku(self, keyword: str) -> list[Buku]:
        """Mencari buku berdasarkan keyword."""
        keyword_lower = keyword.lower()
        return [buku for buku in self._buku_list 
                if keyword_lower in buku.judul.lower() or
                   keyword_lower in buku.penulis.lower() or
                   keyword_lower in buku.kategori.lower()]
    
    def daftar_buku(self) -> list[Buku]:
        """Mendapatkan semua buku dalam perpustakaan."""
        return self._buku_list.copy()
    
    def tambah_anggota(self, id: str, nama: str, kontak: str, alamat: str = "") -> Anggota:
        """Menambahkan anggota baru ke perpustakaan."""
        try:
            if self._find_anggota_by_id(id):
                raise DuplicateIDError(f"Anggota dengan ID '{id}' sudah ada")
            
            anggota = Anggota(id=id, nama=nama, kontak=kontak, alamat=alamat)
            
            self._anggota_list.append(anggota)
            self._database.save_anggota(self._anggota_list)
            
            log_action(self._logger, "ADD_MEMBER", f"Member added: {nama} (ID: {id})")
            
            return anggota
        except Exception as e:
            log_error(self._logger, e, "tambah_anggota")
            raise
    
    def edit_anggota(self, id: str, nama: Optional[str] = None,
                     kontak: Optional[str] = None, alamat: Optional[str] = None) -> Anggota:
        """Mengedit informasi anggota."""
        try:
            anggota = self._get_anggota_or_raise(id)
            
            if nama is not None:
                validate_non_empty_string(nama, "Nama")
                anggota.nama = nama
            
            if kontak is not None:
                validate_non_empty_string(kontak, "Kontak")
                anggota.kontak = kontak
            
            if alamat is not None:
                anggota.alamat = alamat
            
            self._database.save_anggota(self._anggota_list)
            
            log_action(self._logger, "EDIT_MEMBER", f"Member edited: {anggota.nama} (ID: {id})")
            
            return anggota
        except Exception as e:
            log_error(self._logger, e, "edit_anggota")
            raise
    
    def hapus_anggota(self, id: str) -> None:
        """Menghapus anggota dari perpustakaan."""
        try:
            anggota = self._get_anggota_or_raise(id)
            
            if anggota.jumlah_pinjaman() > 0:
                raise InvalidInputError("Anggota masih memiliki pinjaman aktif, tidak dapat dihapus")
            
            self._anggota_list.remove(anggota)
            self._database.save_anggota(self._anggota_list)
            
            log_action(self._logger, "DELETE_MEMBER", f"Member deleted: {anggota.nama} (ID: {id})")
            
        except Exception as e:
            log_error(self._logger, e, "hapus_anggota")
            raise
    
    def cari_anggota(self, keyword: str) -> list[Anggota]:
        """Mencari anggota berdasarkan keyword."""
        keyword_lower = keyword.lower()
        return [anggota for anggota in self._anggota_list
                if keyword_lower in anggota.nama.lower() or
                   keyword_lower in anggota.kontak.lower()]
    
    def daftar_anggota(self) -> list[Anggota]:
        """Mendapatkan semua anggota perpustakaan."""
        return self._anggota_list.copy()
    
    def pinjam_buku(self, anggota_id: str, buku_id: str) -> Peminjaman:
        """Memproses peminjaman buku oleh anggota."""
        try:
            anggota = self._get_anggota_or_raise(anggota_id)
            buku = self._get_buku_or_raise(buku_id)
            
            if not buku.tersedia():
                raise BookUnavailableError(f"Buku '{buku.judul}' tidak tersedia (stok habis)")
            
            if anggota.jumlah_pinjaman() >= MAX_PINJAMAN:
                raise MaximumLoanReachedError(
                    f"Anggota sudah mencapai batas maksimal peminjaman ({MAX_PINJAMAN} buku)"
                )
            
            peminjaman_id = str(uuid.uuid4())
            peminjaman = Peminjaman.buat_peminjaman(id=peminjaman_id, anggota_id=anggota_id, buku_id=buku_id)
            
            buku.kurangi_stok()
            anggota.pinjam(peminjaman_id)
            self._peminjaman_list.append(peminjaman)
            
            self._database.save_buku(self._buku_list)
            self._database.save_anggota(self._anggota_list)
            self._database.save_transaksi(self._peminjaman_list)
            
            log_action(self._logger, "BORROW_BOOK", 
                      f"Member {anggota.nama} borrowed '{buku.judul}' (Loan ID: {peminjaman_id})")
            
            return peminjaman
        except Exception as e:
            log_error(self._logger, e, "pinjam_buku")
            raise
    
    def kembalikan_buku(self, peminjaman_id: str) -> Peminjaman:
        """Memproses pengembalian buku."""
        try:
            peminjaman = self._get_peminjaman_or_raise(peminjaman_id)
            
            if peminjaman.status == "selesai":
                raise InvalidInputError("Peminjaman sudah selesai")
            
            anggota = self._get_anggota_or_raise(peminjaman.anggota_id)
            buku = self._get_buku_or_raise(peminjaman.buku_id)
            
            peminjaman.tandai_dikembalikan()
            buku.tambah_stok()
            anggota.kembali(peminjaman_id)
            
            self._database.save_buku(self._buku_list)
            self._database.save_anggota(self._anggota_list)
            self._database.save_transaksi(self._peminjaman_list)
            
            log_action(self._logger, "RETURN_BOOK",
                      f"Member {anggota.nama} returned '{buku.judul}' (Fine: Rp {peminjaman.denda.nominal})")
            
            return peminjaman
        except Exception as e:
            log_error(self._logger, e, "kembalikan_buku")
            raise
    
    def daftar_peminjaman(self, status: Optional[str] = None) -> list[Peminjaman]:
        """Mendapatkan daftar peminjaman dengan filter status optional."""
        if status is None:
            return self._peminjaman_list.copy()
        return [p for p in self._peminjaman_list if p.status == status]
    
    def get_peminjaman_by_anggota(self, anggota_id: str) -> list[Peminjaman]:
        """Mendapatkan semua peminjaman dari anggota tertentu."""
        return [p for p in self._peminjaman_list if p.anggota_id == anggota_id]
    
    def get_peminjaman_by_buku(self, buku_id: str) -> list[Peminjaman]:
        """Mendapatkan semua peminjaman untuk buku tertentu."""
        return [p for p in self._peminjaman_list if p.buku_id == buku_id]
