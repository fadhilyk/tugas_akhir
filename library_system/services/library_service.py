"""
Module untuk LibraryService.

Service ini menangani operasi perpustakaan seperti CRUD buku, anggota, dan transaksi.
"""

from typing import Optional
from datetime import datetime
import uuid
from ..models import Buku, Anggota, Peminjaman, MAX_PINJAMAN


class LibraryService:
    """
    Service untuk menangani operasi perpustakaan.
    
    Attributes:
        _buku_list: List buku dalam perpustakaan
        _anggota_list: List anggota perpustakaan
        _peminjaman_list: List transaksi peminjaman
    """
    
    def __init__(self) -> None:
        """Inisialisasi LibraryService dengan data kosong."""
        self._buku_list: list[Buku] = []
        self._anggota_list: list[Anggota] = []
        self._peminjaman_list: list[Peminjaman] = []
    
    def _find_buku_by_id(self, buku_id: str) -> Optional[Buku]:
        """
        Mencari buku berdasarkan ID.
        
        Args:
            buku_id: ID buku
            
        Returns:
            Object Buku jika ditemukan, None jika tidak
        """
        for buku in self._buku_list:
            if buku.id == buku_id:
                return buku
        return None
    
    def _find_anggota_by_id(self, anggota_id: str) -> Optional[Anggota]:
        """
        Mencari anggota berdasarkan ID.
        
        Args:
            anggota_id: ID anggota
            
        Returns:
            Object Anggota jika ditemukan, None jika tidak
        """
        for anggota in self._anggota_list:
            if anggota.id == anggota_id:
                return anggota
        return None
    
    def _find_peminjaman_by_id(self, peminjaman_id: str) -> Optional[Peminjaman]:
        """
        Mencari peminjaman berdasarkan ID.
        
        Args:
            peminjaman_id: ID peminjaman
            
        Returns:
            Object Peminjaman jika ditemukan, None jika tidak
        """
        for peminjaman in self._peminjaman_list:
            if peminjaman.id == peminjaman_id:
                return peminjaman
        return None
    
    def tambah_buku(self, id: str, judul: str, penulis: str, penerbit: str,
                    tahun: int, kategori: str, stok: int) -> Buku:
        """
        Menambahkan buku baru ke perpustakaan.
        
        Args:
            id: Unique identifier untuk buku
            judul: Judul buku
            penulis: Nama penulis
            penerbit: Nama penerbit
            tahun: Tahun terbit
            kategori: Kategori buku
            stok: Jumlah stok
            
        Returns:
            Object Buku yang baru dibuat
            
        Raises:
            ValueError: Jika ID buku sudah ada
        """
        if self._find_buku_by_id(id):
            raise ValueError(f"Buku dengan ID '{id}' sudah ada")
        
        buku = Buku(
            id=id,
            judul=judul,
            penulis=penulis,
            penerbit=penerbit,
            tahun=tahun,
            kategori=kategori,
            stok=stok
        )
        
        self._buku_list.append(buku)
        return buku
    
    def edit_buku(self, id: str, judul: Optional[str] = None, 
                  penulis: Optional[str] = None, penerbit: Optional[str] = None,
                  tahun: Optional[int] = None, kategori: Optional[str] = None,
                  stok: Optional[int] = None) -> Buku:
        """
        Mengedit informasi buku.
        
        Args:
            id: ID buku yang akan diedit
            judul: Judul baru (optional)
            penulis: Penulis baru (optional)
            penerbit: Penerbit baru (optional)
            tahun: Tahun baru (optional)
            kategori: Kategori baru (optional)
            stok: Stok baru (optional)
            
        Returns:
            Object Buku yang sudah diedit
            
        Raises:
            ValueError: Jika buku tidak ditemukan atau data invalid
        """
        buku = self._find_buku_by_id(id)
        
        if not buku:
            raise ValueError(f"Buku dengan ID '{id}' tidak ditemukan")
        
        if judul is not None:
            if not judul.strip():
                raise ValueError("Judul tidak boleh kosong")
            buku.judul = judul
        
        if penulis is not None:
            if not penulis.strip():
                raise ValueError("Penulis tidak boleh kosong")
            buku.penulis = penulis
        
        if penerbit is not None:
            buku.penerbit = penerbit
        
        if tahun is not None:
            if not isinstance(tahun, int):
                raise ValueError("Tahun harus berupa integer")
            buku.tahun = tahun
        
        if kategori is not None:
            buku.kategori = kategori
        
        if stok is not None:
            if stok < 0:
                raise ValueError("Stok tidak boleh negatif")
            buku.stok = stok
        
        return buku
    
    def hapus_buku(self, id: str) -> None:
        """
        Menghapus buku dari perpustakaan.
        
        Args:
            id: ID buku yang akan dihapus
            
        Raises:
            ValueError: Jika buku tidak ditemukan atau masih dipinjam
        """
        buku = self._find_buku_by_id(id)
        
        if not buku:
            raise ValueError(f"Buku dengan ID '{id}' tidak ditemukan")
        
        for peminjaman in self._peminjaman_list:
            if peminjaman.buku_id == id and peminjaman.status == "aktif":
                raise ValueError("Buku masih dipinjam, tidak dapat dihapus")
        
        self._buku_list.remove(buku)
    
    def cari_buku(self, keyword: str) -> list[Buku]:
        """
        Mencari buku berdasarkan keyword (judul, penulis, atau kategori).
        
        Args:
            keyword: Kata kunci pencarian
            
        Returns:
            List buku yang cocok dengan keyword
        """
        keyword_lower = keyword.lower()
        hasil = []
        
        for buku in self._buku_list:
            if (keyword_lower in buku.judul.lower() or
                keyword_lower in buku.penulis.lower() or
                keyword_lower in buku.kategori.lower()):
                hasil.append(buku)
        
        return hasil
    
    def daftar_buku(self) -> list[Buku]:
        """
        Mendapatkan semua buku dalam perpustakaan.
        
        Returns:
            List semua buku
        """
        return self._buku_list.copy()
    
    def tambah_anggota(self, id: str, nama: str, kontak: str, 
                       alamat: str = "") -> Anggota:
        """
        Menambahkan anggota baru ke perpustakaan.
        
        Args:
            id: Unique identifier untuk anggota
            nama: Nama lengkap anggota
            kontak: Informasi kontak
            alamat: Alamat lengkap (optional)
            
        Returns:
            Object Anggota yang baru dibuat
            
        Raises:
            ValueError: Jika ID anggota sudah ada
        """
        if self._find_anggota_by_id(id):
            raise ValueError(f"Anggota dengan ID '{id}' sudah ada")
        
        anggota = Anggota(
            id=id,
            nama=nama,
            kontak=kontak,
            alamat=alamat
        )
        
        self._anggota_list.append(anggota)
        return anggota
    
    def edit_anggota(self, id: str, nama: Optional[str] = None,
                     kontak: Optional[str] = None, alamat: Optional[str] = None) -> Anggota:
        """
        Mengedit informasi anggota.
        
        Args:
            id: ID anggota yang akan diedit
            nama: Nama baru (optional)
            kontak: Kontak baru (optional)
            alamat: Alamat baru (optional)
            
        Returns:
            Object Anggota yang sudah diedit
            
        Raises:
            ValueError: Jika anggota tidak ditemukan atau data invalid
        """
        anggota = self._find_anggota_by_id(id)
        
        if not anggota:
            raise ValueError(f"Anggota dengan ID '{id}' tidak ditemukan")
        
        if nama is not None:
            if not nama.strip():
                raise ValueError("Nama tidak boleh kosong")
            anggota.nama = nama
        
        if kontak is not None:
            if not kontak.strip():
                raise ValueError("Kontak tidak boleh kosong")
            anggota.kontak = kontak
        
        if alamat is not None:
            anggota.alamat = alamat
        
        return anggota
    
    def hapus_anggota(self, id: str) -> None:
        """
        Menghapus anggota dari perpustakaan.
        
        Args:
            id: ID anggota yang akan dihapus
            
        Raises:
            ValueError: Jika anggota tidak ditemukan atau masih memiliki pinjaman aktif
        """
        anggota = self._find_anggota_by_id(id)
        
        if not anggota:
            raise ValueError(f"Anggota dengan ID '{id}' tidak ditemukan")
        
        if anggota.jumlah_pinjaman() > 0:
            raise ValueError("Anggota masih memiliki pinjaman aktif, tidak dapat dihapus")
        
        self._anggota_list.remove(anggota)
    
    def cari_anggota(self, keyword: str) -> list[Anggota]:
        """
        Mencari anggota berdasarkan keyword (nama atau kontak).
        
        Args:
            keyword: Kata kunci pencarian
            
        Returns:
            List anggota yang cocok dengan keyword
        """
        keyword_lower = keyword.lower()
        hasil = []
        
        for anggota in self._anggota_list:
            if (keyword_lower in anggota.nama.lower() or
                keyword_lower in anggota.kontak.lower()):
                hasil.append(anggota)
        
        return hasil
    
    def daftar_anggota(self) -> list[Anggota]:
        """
        Mendapatkan semua anggota perpustakaan.
        
        Returns:
            List semua anggota
        """
        return self._anggota_list.copy()
    
    def pinjam_buku(self, anggota_id: str, buku_id: str) -> Peminjaman:
        """
        Memproses peminjaman buku oleh anggota.
        
        Args:
            anggota_id: ID anggota yang meminjam
            buku_id: ID buku yang dipinjam
            
        Returns:
            Object Peminjaman yang baru dibuat
            
        Raises:
            ValueError: Jika anggota/buku tidak ditemukan, stok habis, 
                       atau anggota melebihi batas pinjaman
        """
        anggota = self._find_anggota_by_id(anggota_id)
        if not anggota:
            raise ValueError(f"Anggota dengan ID '{anggota_id}' tidak ditemukan")
        
        buku = self._find_buku_by_id(buku_id)
        if not buku:
            raise ValueError(f"Buku dengan ID '{buku_id}' tidak ditemukan")
        
        if not buku.tersedia():
            raise ValueError(f"Buku '{buku.judul}' tidak tersedia (stok habis)")
        
        if anggota.jumlah_pinjaman() >= MAX_PINJAMAN:
            raise ValueError(f"Anggota sudah mencapai batas maksimal peminjaman ({MAX_PINJAMAN} buku)")
        
        peminjaman_id = str(uuid.uuid4())
        peminjaman = Peminjaman.buat_peminjaman(
            id=peminjaman_id,
            anggota_id=anggota_id,
            buku_id=buku_id
        )
        
        buku.kurangi_stok()
        anggota.pinjam(peminjaman_id)
        self._peminjaman_list.append(peminjaman)
        
        return peminjaman
    
    def kembalikan_buku(self, peminjaman_id: str) -> Peminjaman:
        """
        Memproses pengembalian buku.
        
        Args:
            peminjaman_id: ID transaksi peminjaman
            
        Returns:
            Object Peminjaman yang sudah dikembalikan
            
        Raises:
            ValueError: Jika peminjaman tidak ditemukan atau sudah selesai
        """
        peminjaman = self._find_peminjaman_by_id(peminjaman_id)
        if not peminjaman:
            raise ValueError(f"Peminjaman dengan ID '{peminjaman_id}' tidak ditemukan")
        
        if peminjaman.status == "selesai":
            raise ValueError("Peminjaman sudah selesai")
        
        anggota = self._find_anggota_by_id(peminjaman.anggota_id)
        if not anggota:
            raise ValueError(f"Anggota dengan ID '{peminjaman.anggota_id}' tidak ditemukan")
        
        buku = self._find_buku_by_id(peminjaman.buku_id)
        if not buku:
            raise ValueError(f"Buku dengan ID '{peminjaman.buku_id}' tidak ditemukan")
        
        peminjaman.tandai_dikembalikan()
        buku.tambah_stok()
        anggota.kembali(peminjaman_id)
        
        return peminjaman
    
    def daftar_peminjaman(self, status: Optional[str] = None) -> list[Peminjaman]:
        """
        Mendapatkan daftar peminjaman dengan filter status optional.
        
        Args:
            status: Filter berdasarkan status ('aktif' atau 'selesai'), None untuk semua
            
        Returns:
            List peminjaman sesuai filter
        """
        if status is None:
            return self._peminjaman_list.copy()
        
        return [p for p in self._peminjaman_list if p.status == status]
    
    def get_peminjaman_by_anggota(self, anggota_id: str) -> list[Peminjaman]:
        """
        Mendapatkan semua peminjaman dari anggota tertentu.
        
        Args:
            anggota_id: ID anggota
            
        Returns:
            List peminjaman dari anggota
        """
        return [p for p in self._peminjaman_list if p.anggota_id == anggota_id]
    
    def get_peminjaman_by_buku(self, buku_id: str) -> list[Peminjaman]:
        """
        Mendapatkan semua peminjaman untuk buku tertentu.
        
        Args:
            buku_id: ID buku
            
        Returns:
            List peminjaman untuk buku
        """
        return [p for p in self._peminjaman_list if p.buku_id == buku_id]
